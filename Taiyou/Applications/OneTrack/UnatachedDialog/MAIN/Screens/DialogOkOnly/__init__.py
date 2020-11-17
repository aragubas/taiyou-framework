#!/usr/bin/python3.7
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
import Core
import pygame
from OneTrack.MAIN import UI
from Core import Utils


class Screen:
    def __init__(self, pRoot_Process):
        self.RootProcess = pRoot_Process

        self.Args = self.RootProcess.INIT_ARGS[2].split(';')
        self.DialogTitle = self.Args[0]
        self.DialogText = self.Args[1]
        self.DialogIcon = None
        self.DialogIconDimensions = (128, 128)

        self.RootProcess.TITLEBAR_TEXT = self.DialogTitle

        if not self.RootProcess.OptionalParameters == None:
            SplitedParameters = self.RootProcess.OptionalParameters.split(",")

            for parameter in SplitedParameters:
                print(parameter)
                ParameterSplit = parameter.split(":")

                if ParameterSplit[0] == "icon":
                    self.DialogIcon = ParameterSplit[1]
                    print("DialogIcon set to: " + self.DialogIcon)
                    continue

        if self.DialogIcon == "none":
            self.DialogIcon = None

        self.DialogSize = (self.RootProcess.DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, self.DialogText) + 10, self.RootProcess.DefaultContents.GetFont_height("/Ubuntu_Bold.ttf", 14, self.DialogText) + 5)
        self.DialogSize = list(self.DialogSize)

        if not self.DialogIcon == None:
            self.DialogSize = (self.RootProcess.DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, self.DialogText) + 10 + self.DialogIconDimensions[0] + 2, self.RootProcess.DefaultContents.GetFont_height("/Ubuntu_Bold.ttf", 14, self.DialogText) + 5)
            self.DialogSize = list(self.DialogSize)

            if self.DialogSize[0] < self.DialogIconDimensions[0]:
                self.DialogSize[0] += self.DialogIconDimensions[0]

            if self.DialogSize[1] < self.DialogIconDimensions[1]:
                self.DialogSize[1] += self.DialogIconDimensions[1]

        print(self.DialogSize)

        # Set the Minimal Size
        if self.DialogSize[0] < 120:
            self.DialogSize = (120, self.DialogSize[1])

        if self.DialogSize[1] < 110:
            self.DialogSize = (self.DialogSize[0], 110)

        self.RootProcess.DISPLAY = pygame.Surface(self.DialogSize)

    def Draw(self, DISPLAY):
        TextX = 5

        if self.DialogIcon is not None:
            TextX = self.DialogIconDimensions[0] + 10
            self.RootProcess.DefaultContents.ImageRender(DISPLAY, "/{0}.png".format(self.DialogIcon), 5, 5, 128, 128, SmoothScaling=True)

        self.RootProcess.DefaultContents.FontRender(DISPLAY, "/Ubuntu.ttf", 14, self.DialogText, (240, 240, 240), TextX, 5)

    def Update(self):
        pass

    def EventUpdate(self, event):
        pass
