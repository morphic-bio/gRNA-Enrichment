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

class OWMAGeCK_countcombine(OWBwBWidget):
    name = "MAGeCK_countcombine"
    description = "Combine mageck counts outputs by sample names"
    priority = 10
    icon = getIconName(__file__,"python3.png")
    want_main_area = False
    docker_image_name = "mageck-countcombine"
    docker_image_tag = "latest"
    inputs = [("Trigger",str,"handleInputsTrigger"),("inputDir",str,"handleInputsinputDir"),("outputFile",str,"handleInputsoutputFile"),("sampleNames",str,"handleInputssampleNames")]
    outputs = [("outputFile",str),("sampleNames",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputDir=pset(None)
    outputFile=pset(None)
    sampleNames=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"MAGeCK_countcombine")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssampleNames(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sampleNames", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
        outputValue=None
        if hasattr(self,"sampleNames"):
            outputValue=getattr(self,"sampleNames")
        self.send("sampleNames", outputValue)
