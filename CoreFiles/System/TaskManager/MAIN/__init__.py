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
from CoreFiles.System.TaiyouUI.MAIN import UI
from Core.MAIN import DISPLAY as DISPLAY

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((250, 300))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = False
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "Task Manager"
        self.WindowDragEnable = False

    def Initialize(self):
        self.DefaultContent = Core.CntMng.ContentManager()
        self.DefaultContent.SetSourceFolder("CoreFiles/System/TaskManager/")
        self.DefaultContent.LoadRegKeysInFolder("Data/reg")
        self.DefaultContent.LoadImagesInFolder("Data/img")
        self.DefaultContent.SetFontPath("Data/fonts")

        self.WindowManagerSignal(0)

        self.WindowDragEnable = False

        self.ExploitTestStatus = "Waiting..."
        self.ProcessFound = False

    def EventUpdate(self, event):
        pass

    def Draw(self):
        self.DISPLAY.fill((120, 120, 120))

        self.DefaultContent.FontRender(self.DISPLAY, "/Ubuntu_Bold.ttf", 14, self.ExploitTestStatus, (240, 240, 240), 5, 5)

        self.LAST_SURFACE = self.DISPLAY.copy()
        return self.DISPLAY

    def Update(self):
        pass

    def WindowManagerSignal(self, Signal):
        # Gain Focus
        OriginalDragValue = self.WindowDragEnable
        if Signal == 0:
            for process in Core.MAIN.ProcessList:
                process.APPLICATION_HAS_FOCUS = False
                process.WINDOW_DRAG_ENABLED = False

            # Make this application focused again
            self.APPLICATION_HAS_FOCUS = True
            self.WindowDragEnable = OriginalDragValue
