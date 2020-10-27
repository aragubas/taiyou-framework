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

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.DISPLAY = pygame.Surface((800, 600))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = True
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), self.DISPLAY.get_height())
        self.TITLEBAR_TEXT = "Bootloader"

    def Initialize(self):
        self.DefaultContent = Core.cntMng.ContentManager()

        self.DefaultContent.SetSourceFolder("CoreFiles/System/Bootloader/")
        self.DefaultContent.LoadRegKeysInFolder("Data/reg")
        self.DefaultContent.LoadImagesInFolder("Data/img")
        self.DefaultContent.SetFontPath("Data/fonts")

        self.Progress = 0
        self.ProgressAddDelay = 0
        self.ProgressProgression = True
        self.ProgressMax = 100
        self.LoadingComplete = False

    def Update(self):
        if self.ProgressProgression and not self.LoadingComplete:
            self.ProgressAddDelay += 1

            if self.ProgressAddDelay == 5:
                self.ProgressAddDelay = 0
                self.Progress += 1

            if self.ProgressAddDelay == 2:
                self.LoadingSteps(self.Progress)

            if self.Progress >= self.ProgressMax and not self.LoadingComplete:
                self.LoadingComplete = True

                print("Bootloader : Loading Complete")

                # Finish the Bootloader
                Core.MAIN.KillProcessByPID(self.PID)

    def Draw(self):
        ## Fill Write Screen
        self.DISPLAY.fill((18, 10, 38))

        self.DrawProgressBar(self.DISPLAY)

        # Draw the Logo
        LogoPos = (self.DISPLAY.get_width() / 2 - 231 / 2, self.DISPLAY.get_height() / 2 - 242, 231, 242)

        self.DefaultContent.ImageRender(self.DISPLAY, "/logo.png", LogoPos[0], LogoPos[1], LogoPos[2], LogoPos[3])

        self.LAST_SURFACE = self.DISPLAY.copy()
        return self.DISPLAY

    def DrawProgressBar(self, DISPLAY):
        self.LoadingBarPos = (DISPLAY.get_width() / 2 - 250 / 2, DISPLAY.get_height() / 2 + 10 / 2, 250, 10)
        self.LoadingBarProgress = (self.LoadingBarPos[0], self.LoadingBarPos[1], Core.utils.Get_Percentage(self.Progress, self.LoadingBarPos[2], self.ProgressMax), 10)

        Core.shape.Shape_Rectangle(DISPLAY, (20, 20, 58), self.LoadingBarPos, 0, self.LoadingBarPos[3])
        Core.shape.Shape_Rectangle(DISPLAY, (94, 114, 219), self.LoadingBarProgress, 0, self.LoadingBarPos[3])

    def EventUpdate(self, event):
        return

    def FinishLoadingScreen(self):
        self.ProgressMax = self.Progress + 5

    def LoadingSteps(self, CurrentProgres):
        if CurrentProgres == 0:
            # Start the SystemUI
            Core.MAIN.CreateProcess("CoreFiles/System/TaiyouUI", "system_ui")

        if CurrentProgres == 1:
            # Start the Default Application
            Core.MAIN.CreateProcess(Core.GetUserSelectedApplication(), Core.GetUserSelectedApplication())

            # Finish the Loading
            self.FinishLoadingScreen()