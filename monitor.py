#!/usr/bin/python
#-*- coding: UTF-8 -*-
import os
import string

class Monitor(object):
    def __init__(self,media):
        self._media=media
        
    def get_max_position(self):
        with open(self._media) as fd:
            fd.seek(0,2)
            last_pos=fd.tell()
        return last_pos
    
    def follow(self,last_pos):
        with open(self._media) as fd:
            fd.seek(last_pos)
            while 1:
                line=fd.readline()
                if line:
                    last_pos=fd.tell()
                    if line not in ['\r','\n','\r\n']:
                        yield line,last_pos
                else:
                    break            
                
    def tail(self,line_count,keyword):
        br=BackwardsReader(open(self._media))
        for i in xrange(line_count):
            line = br.readline().decode('utf8')
            if not line:
                break
            if not keyword or line.find(keyword)!=-1:
                yield line     
    

# Copyright (c) Peter Astrand <astrand@cendio.se>
class BackwardsReader:
    """Read a file line by line, backwards"""
    BLKSIZE = 4096

    def readline(self):
        while 1:
            newline_pos = string.rfind(self.buf, "\n")
            pos = self.file.tell()
            if newline_pos != -1:
                # Found a newline
                line = self.buf[newline_pos+1:]
                self.buf = self.buf[:newline_pos]
                if pos != 0 or newline_pos != 0 or self.trailing_newline:
                    line += "\n"
                return line
            else:
                if pos == 0:
                    # Start-of-file
                    return ""
                else:
                    # Need to fill buffer
                    toread = min(self.BLKSIZE, pos)
                    self.file.seek(-toread, 1)
                    self.buf = self.file.read(toread) + self.buf
                    self.file.seek(-toread, 1)
                    if pos - toread == 0:
                        self.buf = "\n" + self.buf

    def __init__(self, file):
        self.file = file
        self.buf = ""
        self.file.seek(-1, 2)
        self.trailing_newline = 0
        lastchar = self.file.read(1)
        if lastchar == "\n":
            self.trailing_newline = 1
            self.file.seek(-1, 2)
