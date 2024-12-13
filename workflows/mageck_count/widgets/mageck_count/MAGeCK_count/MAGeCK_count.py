import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWMAGeCK_count(OWBwBWidget):
    name = "MAGeCK_count"
    description = "MAGeCK count, collect read counts from fastq files"
    priority = 10
    icon = getIconName(__file__,"mageckgithub.png")
    want_main_area = False
    docker_image_name = "brycenofu/mageck"
    docker_image_tag = "0.5.9.5_debian13"
    inputs = [("listSeq",str,"handleInputslistSeq"),("fastq",str,"handleInputsfastq"),("countTable",str,"handleInputscountTable"),("fastq2",str,"handleInputsfastq2"),("outputDir",str,"handleInputsoutputDir")]
    outputs = [("File",str),("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    listSeq=pset(None)
    fastq=pset([])
    outputDir=pset(None)
    countTable=pset(None)
    normMethod=pset(None)
    controlSgrna=pset(None)
    controlGene=pset(None)
    sampleLabel=pset([])
    outputPrefix=pset(['sample1'])
    unmappedToFile=pset(False)
    keepTmp=pset(False)
    fastq2=pset(None)
    countPair=pset("False")
    trim5=pset(None)
    sgrnaLen=pset(20)
    countN=pset(False)
    reverseComplement=pset(False)
    pdfReport=pset(False)
    day0Label=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"MAGeCK_count")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputslistSeq(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("listSeq", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfastq(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("fastq", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscountTable(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("countTable", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfastq2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("fastq2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"File"):
            outputValue=getattr(self,"File")
        self.send("File", outputValue)
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
