from islandoraUtils.fedoraLib import get_datastream_as_file, update_datastream
from islandoraUtils import DSConverter as DSC
from plugin_manager import IslandoraListenerPlugin
import pprint
import ConfigParser

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
        if 'si:fieldbookCModel' in message['content_models'] and message['dsid'] == 'OBJ' and obj['OBJ'].mimeType == 'application/pdf':
            DSC.create_swf(obj, 'OBJ', 'OBJ.swf', ['-T 9', '-f', '-t', '-s', 'storeallcharacters', '-G', '-s', 'subpixels=1.5'])
            DSC.create_thumbnail(obj, 'OBJ', 'TN')
        if ('si:imageCModel' in message['content_models'] or 'si:generalImageCModel' in message['content_models']) and message['dsid'] == 'IMAGE':
            DSC.create_thumbnail(obj, 'IMAGE', 'TN')
            DSC.create_fits(obj, 'IMAGE')
        if 'si:datasetCModel' in message['content_models'] and message['dsid'] == 'OBJ':
            if obj['OBJ'].mimeType == 'application/vnd.ms-excel':
                DSC.create_csv(obj, 'OBJ', 'CSV')
            elif obj['OBJ'].mimeType == 'text/csv':
                directory, file = get_datastream_as_file(obj, 'OBJ', "document")
                update_datastream(obj, 'CSV', directory + '/' + file, label='CSV', mimeType='text/csv')
                rmtree(directory, ignore_errors=True)

    def islandoraMessage(self, method, message, client):
        #print it and log it
        print method
        self.logger.info(method)

        #print it and log it
        print message
        self.logger.info(message)
        print ""
