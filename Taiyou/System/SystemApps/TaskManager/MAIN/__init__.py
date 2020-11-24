#!/usr/bin/python3.8
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
import System.Core as Core
import pygame
from System.SystemApps.TaiyouUI.MAIN import UI
from System.Core.MAIN import DISPLAY as DISPLAY

class Process(Core.Process):
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
