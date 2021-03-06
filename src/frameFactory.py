import cv2
import numpy as np
from copy import deepcopy
import math

from gui.radiographFrame import RadiographFrame
from gui.singleToothFrame import SingleToothFrame
from gui.teethSetFrame import TeethSetFrame
from gui.meanModelFrame import MeanModelFrame

from src.tooth import Tooth
from src.PCA import PCA
from src.filter import Filter



class FrameFactory:

    def __init__(self, dataHandler):
        self.dataHandler = dataHandler

    def createProcrustesAlignedTeethImages(self, parent, alignedTeeth):
        teeth = deepcopy(alignedTeeth)
        teethImages = list()
        height = 720
        width = 1280
        for tooth in teeth:
            img = np.zeros((height,width,3), np.uint8)
            tooth.scale(height)
            tooth.translate([width/2, height/2])
            img = self._drawToothOnImage(tooth, img)

            teethImages.append(SingleToothFrame(parent, img))
        
        return teethImages

    def createMeanModelFrame(self, parent, meanModel, col, row):
        height = 360
        width = 320
        img = np.zeros((height,width,3), np.uint8)
        meanTooth = Tooth(deepcopy(meanModel))
        meanTooth.scale(height)
        meanTooth.translate([width/2, height/2])
        img = self._drawToothOnImage(meanTooth, img)
        frame = MeanModelFrame(parent, img, row, col)
        return frame

    def createProcrustesAlignedTeethSetImages(self, parent, alignedTeethSets):
        teethSets = deepcopy(alignedTeethSets)
        teethImages = list()
        height = 720
        width = 1280
        for teethSet in teethSets:
            img = np.zeros((height,width,3), np.uint8)
            teethSet.scale(height*5)
            teethSet.translate([width/2, height/2])
            img = self._drawTootSethOnImage(teethSet, img)

            teethImages.append(TeethSetFrame(parent, img))
        
        return teethImages

    def createLefOutRadiographFrame(self, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0

        radiograph = self.dataHandler.getLeftOutRadiograph(deepCopy=True)
        img = radiograph.getImage()

        if drawLandmarks:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            teeth = radiograph.getTeeth()
            for tooth in teeth:
                img = self._drawToothOnImage(tooth, img)

        if meanModels is not None:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            for model in meanModels[i]:
                img = self._drawToothOnImage(model, img)

        radioImages.append(RadiographFrame(parent, img))

        return radioImages

    def createRadiographFrames(self, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0
        for radiograph in self.dataHandler.getRadiographs(deepCopy=True):
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            if meanModels is not None:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                for model in meanModels[i]:
                    img = self._drawToothOnImage(model, img)

            radioImages.append(RadiographFrame(parent, img))
            i += 1

        return radioImages

    def createRadiographFramesFromRadiographs(self, radiographs, parent, meanModels=None, drawLandmarks=False):
        radioImages = list()
        i = 0
        for radiograph in radiographs:
            img = radiograph.getImage()

            if drawLandmarks:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                teeth = radiograph.getTeeth()
                for tooth in teeth:
                   img = self._drawToothOnImage(tooth, img)

            if meanModels is not None:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                for model in meanModels[i]:
                    img = self._drawToothOnImage(model, img)

            radioImages.append(RadiographFrame(parent, img))
            i += 1

        return radioImages

    def drawToothModelOnFrame(self, parent, radiograph_index, meanModels, model_index, modelLocations, rotations):
        img = self.dataHandler.getRadiographs(deepCopy=True)[radiograph_index].getImage()
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        for i in range(model_index+1):
            model = deepcopy(meanModels[i])
            model = Tooth(model)
            rotation = rotations[i]
            theta = rotation*(math.pi/180)
            model.rotate(theta)
            model.scale(200)
            model.translate(modelLocations[i])
            img = self._drawToothOnImage(model, img)

        return RadiographFrame(parent, img), 

    def _drawTootSethOnImage(self, teethSet, img):
        for i in range(8):
            start = i*40
            end = start + 40
            tooth = Tooth(teethSet.landmarks[start:end])
            img = self._drawToothOnImage(tooth, img)
        
        return img

    def _drawToothOnImage(self, tooth, img, landmarkColor=(0,255,0), lineColor=(255,0,0), centerColor=(0,0,255)):
        for i in range(40):
            # Draw Circles
            x = int(tooth.getLandmarks()[i][0])
            y = int(tooth.getLandmarks()[i][1])
            cv2.circle(img, (x, y), 1, landmarkColor, 1)

            # Draw line connecting the circles
            if i < 39:
                x_2 = int(tooth.getLandmarks()[i+1][0])
                y_2 = int(tooth.getLandmarks()[i+1][1])
            else: 
                x_2 = int(tooth.getLandmarks()[0][0])
                y_2 = int(tooth.getLandmarks()[0][1])
            
            cv2.line(img, (x ,y), (x_2, y_2), lineColor)

        # Draw center
        center = tooth.getCenter()
        cv2.circle(img, (int(center[0]), int(center[1])), 5, centerColor, 2)
        return img

    def _drawToothContourOnImage(self, tooth, img, lineColor=(255,0,0), thickness = 3):
        for i in range(40):
            # Draw Circles
            x = int(tooth.getLandmarks()[i][0])
            y = int(tooth.getLandmarks()[i][1])
            # cv2.circle(img, (x, y), 1, landmarkColor, 1)

            # Draw line connecting the circles
            if i < 39:
                x_2 = int(tooth.getLandmarks()[i+1][0])
                y_2 = int(tooth.getLandmarks()[i+1][1])
            else: 
                x_2 = int(tooth.getLandmarks()[0][0])
                y_2 = int(tooth.getLandmarks()[0][1])
            
            cv2.line(img, (x ,y), (x_2, y_2), lineColor, thickness)
        return img

    def createMeanModelPresentationImages(self, statisticalModel):
        toothModels = statisticalModel.getAllToothModels(deepCopy=True)

        pca = PCA()

        for i in range(8):
            height = 3840
            width = 2160
            img = np.zeros((height,width,3), np.uint8)
            meanModel = toothModels[i].getMeanModel(deepCopy=True)
            flatModel = meanModel.flatten()
            eigenvalues = toothModels[i].getEigenvalues(deepCopy=True)
            eigenvectors = toothModels[i].getEigenvectors(deepCopy=True)

            meanTooth = Tooth(deepcopy(meanModel))
            meanTooth.scale(height)
            meanTooth.translate([width/2, height/2])

            for j in range(len(eigenvalues)):
                
                img_2 = deepcopy(img)

                maxChangeVector = np.zeros(np.array(eigenvalues).shape)
                maxChangeVector[j] = 100*eigenvalues[j]*(5*j+1)
                maxChange = pca.reconstruct(maxChangeVector, eigenvectors, deepcopy(flatModel))
                maxChange = maxChange.reshape((maxChange.shape[0] // 2, 2))
                maxChangeTooth = Tooth(maxChange)
                maxChangeTooth.scale(height)
                maxChangeTooth.translate([width/2, height/2])

                minChangeVector = np.zeros(np.array(eigenvalues).shape)
                minChangeVector[j] = -100*(eigenvalues[j])*(5*j+1)
                minChange = pca.reconstruct(minChangeVector, eigenvectors, deepcopy(flatModel))
                minChange = minChange.reshape((minChange.shape[0] // 2, 2))
                minChangeTooth = Tooth(minChange)
                minChangeTooth.scale(height)
                minChangeTooth.translate([width/2, height/2])

                # img_2 = self._drawToothContourOnImage(meanTooth, img_2, lineColor=(255,255,255))
                img_2 = self._drawToothContourOnImage(maxChangeTooth, img_2, lineColor=(255,255,255))
                img_2 = self._drawToothContourOnImage(minChangeTooth, img_2, lineColor=(255,255,255))

                height = img_2.shape[0]
                width = img_2.shape[1]
                img_2 = cv2.resize(img_2, (int(width*0.1), int(height*0.1)), interpolation = cv2.INTER_AREA)

                # img_2 = Filter.process_image(img_2)

                filename = "Results/mean_model_modes_adjusted/tooth_{0}_mode_{1}.jpg".format(i,j)
                cv2.imwrite(filename, img_2)

                cv2.imshow("Mean Model", img_2)

    def createFittingErrorPresentationImages(self, fittedModels, radiograph):
        
        img = radiograph.getImage()
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        teeth = radiograph.getTeeth()
        for i in range(8):

            totalError = 0.0
            numberOfGoodPixels = 0

            tooth = teeth[i]
            model = fittedModels[i]
            img = self._drawToothContourOnImage(tooth, img, lineColor=(0,255,0), thickness=1)
            img = self._drawToothContourOnImage(model, img, lineColor=(255,0,0), thickness=1)
            
            for j in range(40):
                p1 = tooth.getLandmarks()[j]
                p2 = model.getLandmarks()[j]
                x1 = int(p1[0])
                y1 = int(p1[1])
                x2 = int(p2[0])
                y2 = int(p2[1])
                img = cv2.line(img, (x1,y1), (x2,y2), (0,0,255))
                totalError += math.sqrt((x1-x2)**2 + (y1-y2)**2)

                if abs(x1+x2) + abs(y1-y2) <= 2:
                    numberOfGoodPixels += 1

            print("Average pixel position error for tooth " + str(i) + " is: " + str(totalError/40))
            print("Number of good pixels: " + str(numberOfGoodPixels))

        cv2.imshow("test", img)

        return img




