import tkinter as tk
import numpy as np

from src.tooth import Tooth


class ManualModelPlacementContainer(tk.Frame):

    def __init__(self, parent, frameFactory, toothModels):
        tk.Frame.__init__(self, parent)
        #self.pack(side="left", fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameFactory = frameFactory

        self.meanModels = list()
        for model in toothModels:
            self.meanModels.append(model.getMeanModel(deepCopy=True))
        self.meanModels = np.array(self.meanModels)

        self.currentMeanModel = 0
        self.modelCenters = np.zeros((8,2))
        self.modelRotations = np.zeros((8,))
        self.currentRadiograph = 0
        self.radioImages = self.frameFactory.createRadiographFrames(self, drawLandmarks=False)
        self.show()
        self.bindFrames(parent)

    def key(self, event=None):
        print("pressed", repr(event.char))

    def drawModelOnFrame(self, event=None):
        
        # print("Event.Widget = " + str(event.widget))

        for child in self.winfo_children():
            for child_2 in child.winfo_children():
                if event.widget == child_2:
                    
                    # print("Self = " + str(self))
                    print("Drawing model on frame! X = " + str(event.x) + ", Y = " + str(event.y))
                    self.modelCenters[self.currentMeanModel] = [event.x, event.y]
                    self.radioImages[self.currentRadiograph] =\
                        self.frameFactory.drawToothModelOnFrame(self,
                                                                self.currentRadiograph,
                                                                self.meanModels,
                                                                self.currentMeanModel,
                                                                self.modelCenters,
                                                                self.modelRotations)[0]
                    self.show()

    def drawRotatedModelOnFrame(self, rotation):
        self.modelRotations[self.currentMeanModel] = rotation      
        self.radioImages[self.currentRadiograph] =\
            self.frameFactory.drawToothModelOnFrame(self,
                                                    self.currentRadiograph,
                                                    self.meanModels,
                                                    self.currentMeanModel,
                                                    self.modelCenters,
                                                    self.modelRotations)[0]
        self.show()

    def manualRotation(self, rotation):
        self.drawRotatedModelOnFrame(rotation=rotation)

    def getChosenRadiograph(self):
        return self.currentRadiograph

    def getChosenModelPositions(self):
        return self.modelCenters

    def getChosenModelRotations(self):
        return self.modelRotations

    def bindFrames(self, parent):
        for frame in self.radioImages:
            parent.bind("<Key>", self.key)
            parent.bind("<Button-1>", self.drawModelOnFrame)
            parent.bind("<2>", lambda event: frame.focus_set())

    def showNext(self):
        if self.currentRadiograph < len(self.radioImages) - 1:
            self.currentRadiograph += 1
        else: 
            self.currentRadiograph = 0

        self.show()

    def nextMeanModel(self):
        if self.currentMeanModel < len(self.meanModels) - 1:
            self.currentMeanModel += 1
        else:
            self.currentMeanModel = 0

    def showPrevious(self):
        if self.currentRadiograph > 0:
            self.currentRadiograph -= 1
        else: 
            self.currentRadiograph = len(self.radioImages) - 1

        self.show()

    def show(self):
        frame = self.radioImages[self.currentRadiograph]
        frame.tkraise()
