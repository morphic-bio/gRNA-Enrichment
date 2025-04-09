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

class OWmin_pval_fdr_volcano(OWBwBWidget):
    name = "min_pval_fdr_volcano"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"python3.png")
    want_main_area = False
    docker_image_name = "brycenofu/mageck-minpvalfdrvolcano"
    docker_image_tag = "latest"
    inputs = [("inputDir",str,"handleInputsinputDir"),("outputDir",str,"handleInputsoutputDir"),("screen",str,"handleInputsscreen")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputDir=pset(None)
    outputDir=pset(None)
    screen=pset([])
    volcano=pset(False)
    yAxisThreshold=pset(0.05)
    xAxisThreshold=pset(1.0)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"min_pval_fdr_volcano")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsscreen(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("screen", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
