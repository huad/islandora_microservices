from islandoraUtils.fedoraLib import get_datastream_as_file, update_datastream
from shutil import rmtree
from islandoraUtils import DSConverter as DSC
from plugin_manager import IslandoraListenerPlugin
import pprint
import ConfigParser
import subprocess
import logging

class smithsonian_plugin(IslandoraListenerPlugin):

    def initialize(self, config_parser):
        # call the parent function (this just prints an init message to the logs
        # this is a good practice
        IslandoraListenerPlugin.initialize(self, config_parser)
        # setup a prettyprint object
        self.pp = pprint.PrettyPrinter(indent=4)

        return True

    def fedoraMessage(self, message, obj, client):
        # On the Smithsonian site we upload the file datastreams after ingest, only responds to adding or modification purging shouldn't enter this block.
        pp = pprint.PrettyPrinter(indent=4)
        logger = logging.getLogger('smithsonian')
        if 'si:fieldbookCModel' in message['content_models'] and message['dsid'] == 'OBJ' and obj['OBJ'].mimeType == 'application/pdf':
            DSC.create_swf(obj, 'OBJ', 'OBJ.swf', ['-T 9', '-f', '-t', '-s', 'storeallcharacters', '-G', '-s', 'subpixels=1.5'])
            DSC.create_thumbnail(obj, 'OBJ', 'TN')
        if ('si:imageCModel' in message['content_models'] or 'si:generalImageCModel' in message['content_models']) and message['dsid'] == 'OBJ':
            DSC.create_fits(obj, 'OBJ')
            if obj['OBJ'].mimeType == 'image/tiff' or obj['OBJ'].mimeType == 'image/tif':
                directory, file = get_datastream_as_file(obj, 'OBJ', 'tiff')
                r = subprocess.call(["convert", directory+'/'+file, directory+'/out.jpg'])
                if r == 0:
                    update_datastream(obj, 'IMAGE', directory+'/out.jpg', 'IMAGE', 'image/jpg')
                else:
                    logger.warning('PID:%s DSID:%s JPG creation failed (convert return code:%d).' % (obj.pid, dsid, r))
                rmtree(directory, ignore_errors=True)
            elif  obj['OBJ'].mimeType == 'image/jp2':
                directory, file = get_datastream_as_file(obj, 'OBJ', 'jp2')
                r = subprocess.call(["convert", directory+'/'+file, directory+'/out.jpg'])
                if r == 0:
                    update_datastream(obj, 'IMAGE', directory+'/out.jpg', 'IMAGE', 'image/jpg')
                else:
                    logger.warning('PID:%s DSID:%s JPG creation failed (convert return code:%d).' % (obj.pid, dsid, r))
                rmtree(directory, ignore_errors=True)
            else:
            	directory, file = get_datastream_as_file(obj, 'OBJ', "document")
                update_datastream(obj, 'IMAGE', directory + '/' + file, 'IMAGE', obj['OBJ'].mimeType)
                rmtree(directory, ignore_errors=True)            
            DSC.create_thumbnail(obj, 'IMAGE', 'TN')
        if 'si:datasetCModel' in message['content_models'] and message['dsid'] == 'OBJ':
            if obj['OBJ'].mimeType == 'application/vnd.ms-excel':
                DSC.create_csv(obj, 'OBJ', 'CSV')
            elif obj['OBJ'].mimeType == 'text/csv':
                directory, file = get_datastream_as_file(obj, 'OBJ', "document")
                update_datastream(obj, 'CSV', directory + '/' + file, label='CSV', mimeType='text/csv')
                rmtree(directory, ignore_errors=True)
        if 'si:generalImageCModel' in message['content_models'] and message['dsid'] == 'NAGIOS':
            DSC.create_thumbnail(obj, 'NAGIOS', 'TN')

    def islandoraMessage(self, method, message, client):
        #print it and log it
        print method
        self.logger.info(method)

        #print it and log it
        print message
        self.logger.info(message)
        print ""
