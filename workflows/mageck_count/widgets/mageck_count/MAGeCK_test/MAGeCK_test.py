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

class OWMAGeCK_test(OWBwBWidget):
    name = "MAGeCK_test"
    description = "MAGeCK test, sgRNA and gene ranking"
    priority = 10
    icon = getIconName(__file__,"mageckgithub.png")
    want_main_area = False
    docker_image_name = "brycenofu/mageck"
    docker_image_tag = "0.5.9.5_debian13"
    inputs = [("outputDir",str,"handleInputsoutputDir"),("countTable",str,"handleInputscountTable"),("treatmentId",str,"handleInputstreatmentId"),("day0Label",str,"handleInputsday0Label"),("outputPrefix",str,"handleInputsoutputPrefix")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    outputDir=pset(None)
    countTable=pset(None)
    treatmentId=pset([])
    day0Label=pset(None)
    controlId=pset([])
    paired=pset(False)
    normMethod=pset(None)
    geneTestFdrThreshold=pset(0.25)
    adjustMethod=pset(None)
    varianceEstimationSamples=pset(None)
    sortCriteria=pset("neg")
    removeZero=pset("both")
    removeZeroThreshold=pset(0)
    pdfReport=pset(False)
    geneLfcMethod=pset("median")
    outputPrefix=pset(['sample1'])
    controlSgrna=pset(None)
    controlGene=pset(None)
    normCountsToFile=pset(False)
    skipGene=pset(None)
    keepTmp=pset(False)
    additionalRraParameters=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"MAGeCK_test")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscountTable(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("countTable", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstreatmentId(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("treatmentId", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsday0Label(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("day0Label", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputPrefix(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputPrefix", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
