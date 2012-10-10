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

        # get the demo section from the config
        try:
            data = config_parser.get('Custom', 'demo')

            # log it
            self.logger.info('Got this data from config file: "%s".' % data)

        except ConfigParser.Error:
            self.logger.exception('Parsing config file failed.')
            return False

        return True

    def fedoraMessage(self, message, obj, client):
        # Take a look at what content model we are dealing with
        # do some fun stuff based on this
        pp = pprint.PrettyPrinter(indent=4)
        if 'si:fieldbookCModel' in message['content_models'] and (message['dsid'] == 'OBJ' or message['method'] == 'ingest'):
            if obj['OBJ'].mimeType == 'application/pdf':
                DSC.create_swf(obj, 'OBJ', 'OBJ.swf', ['-T 9', '-f', '-t', '-s', 'storeallcharacters', '-G', '-s', 'subpixels=1.5'])
                DSC.create_thumbnail(obj, 'OBJ', 'TN')
        if 'si:imageCModel' in message['content_models'] and (message['dsid'] == 'IMAGE' or message['method'] == 'ingest'):
            DSC.create_thumbnail(obj, 'IMAGE', 'TN')
            DSC.create_fits(obj, 'IMAGE')
        if 'si:generalImageCModel' in message['content_models'] and (message['dsid'] == 'IMAGE' or message['method'] == 'ingest'):
            DSC.create_thumbnail(obj, 'IMAGE', 'TN')
            DSC.create_fits(obj, 'IMAGE')
        if 'si:datasetCModel' in message['content_models'] and (message['dsid'] == 'OBJ' or message['method'] == 'ingest'):
            if obj['OBJ'].mimeType == 'application/vnd.ms-excel':
                DSC.create_csv(obj, 'OBJ', 'CSV')
            elif obj['OBJ'].mimeType == 'text/csv':
                directory, file = get_datastream_as_file(obj, 'OBJ', "document")
                update_datastream(obj, 'CSV', directory + '/' + file, label='CSV Generated Metadata', mimeType='text/csv')

    def islandoraMessage(self, method, message, client):
        #print it and log it
        print method
        self.logger.info(method)

        #print it and log it
        print message
        self.logger.info(message)
        print ""

