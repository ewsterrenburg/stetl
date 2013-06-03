#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Output to File classes.
#
# Author: Just van den Broecke
#
from ..output import Output
from ..util import Util
from ..packet import FORMAT
import os

log = Util.get_log('fileoutput')

# Pretty print XML to file
class FileOutput(Output):
    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.etree_doc)
        log.info("working dir %s" % os.getcwd())

    def write(self, packet):
        if packet.data is None:
            return packet

        file_path = self.cfg.get('file_path')
        return self.write_file(packet, file_path)

    def write_file(self, packet, file_path):
        log.info('writing to file %s' % file_path)
        out_file = open(file_path, 'w')
        out_file.writelines(self.to_string(packet.data))
        out_file.close()
        log.info("written to %s" % file_path)
        return packet

# Pretty print XML to multiple files
class MultiFileOutput(FileOutput):
    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.etree_doc)
        self.file_num = 1

    def write(self, packet):
        if packet.data is None:
            return packet

        # file_path can be of the form: gmlcities-%03d.gml
        file_path = self.cfg.get('file_path')
        file_path = file_path % self.file_num
        self.file_num += 1
        return self.write_file(packet, file_path)

