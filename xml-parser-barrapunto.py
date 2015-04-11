#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.salida = ""
        self.codeHtml = open("rssCode.html",'w')

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':

                self.salida = ("<p><u>Title: "+ self.theContent + "</u></p>")
                self.codeHtml.write(self.salida.encode('utf8'))

                line = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                print line.encode('utf-8') 
                self.inContent = False
                self.theContent = ""

            elif name == 'link':
                print " Link: " + self.theContent + "."
                self.salida = ("<a href=" + self.theContent + ">" +
                self.theContent + "</a>")
                self.codeHtml.write(self.salida.encode('utf8'))

                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)
print "Parse complete"
