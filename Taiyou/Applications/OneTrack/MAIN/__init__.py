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
import pygame, os, pickle, io, time, traceback
import Core
from Core import CntMng
from Core import MAIN
from Core import AppData
import Core as tge
from OneTrack.MAIN.Screens import Editor
from OneTrack.MAIN import LagIndicator
from OneTrack.MAIN import UI
from OneTrack.MAIN.Screens.Editor import InstanceVar as var

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = True
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "OneTrack"
        self.WindowDragEnable = False
        self.DeleteInstanceOnFirstCycle = False
        self.DialogPID = -1
        self.DefaultContents = CntMng.ContentManager()

    def CheckForAnotherInstances(self):
        # Check if there is not another instance of OneTrack
        for process in Core.MAIN.ProcessList:
            if process.PID != self.PID:
                if process.IS_GRAPHICAL and process.FULLSCREEN == self.FULLSCREEN:
                    if process.EXECUTABLE_PATH == self.EXECUTABLE_PATH:
                        # Another instance detected
                        self.DialogPID = self.GreyDialog("Multiple instance detection", "OneTrack does not support multiple instances.\n\nOnly 1 instance of OneTrack is allowed.", "warn")
                        self.DeleteInstanceOnFirstCycle = True
                        return True
        return False

    def Initialize(self):
        var.ProcessReference = self

        print("Initializing {0}...".format(self.TITLEBAR_TEXT))

        # Initialize Variables
        self.CurrentScreenToUpdate = Editor

        # Initialize Content Manager
        self.DefaultContents.SetSourceFolder("OneTrack/")
        self.DefaultContents.SetFontPath("fonts")
        self.DefaultContents.SetImageFolder("img")
        self.DefaultContents.SetRegKeysPath("reg")

        self.DefaultContents.LoadRegKeysInFolder()
        self.DefaultContents.LoadImagesInFolder()

        self.DefaultContents.InitSoundSystem()

        if self.CheckForAnotherInstances():
            return


        # Set the default content manager for the UI
        UI.ContentManager = self.DefaultContents
        var.DefaultContent = self.DefaultContents

        # Load UI Theme
        try:
            UI.ThemesManager_LoadTheme(self.DefaultContents.Get_RegKey("/selected_theme"))
        except:
            print("Error while loading selected theme\nUsing fallback theme")
            self.DefaultContents.Write_RegKey("/selected_theme", "default")

            UI.ThemesManager_LoadTheme(self.DefaultContents.Get_RegKey("/selected_theme"))

        MAIN.ReceiveCommand(0, 60)

        self.TITLEBAR_TEXT = "OneTrack v{0}".format(self.DefaultContents.Get_RegKey("/version"))

        var.LoadDefaultValues()
        Editor.Initialize()
        LagIndicator.Initialize()

    def GreyDialog(self, Title, Text, Icon="none"):
        var.AwaysUpdate = False
        return Core.MAIN.CreateProcess("OneTrack/UnatachedDialog", "OneTrack Dialog", (var.ProcessReference, "DIALOG_OK", "{0};{1}".format(Title, Text), "icon:{0},".format(Icon)))

    def Draw(self):
        self.CurrentScreenToUpdate.GameDraw(self.DISPLAY)

        LagIndicator.Draw(self.DISPLAY)

        self.LAST_SURFACE = self.DISPLAY.copy()
        return self.DISPLAY

    def Update(self):
        if self.DeleteInstanceOnFirstCycle and not self.DialogPID in Core.MAIN.ProcessList_PID:
            Core.MAIN.KillProcessByPID(self.PID)

        if not self.APPLICATION_HAS_FOCUS and var.AwaysUpdate is False:
            return

        self.CurrentScreenToUpdate.Update()

        LagIndicator.Update()

    def EventUpdate(self, event):
        self.CurrentScreenToUpdate.EventUpdate(event)

        if event.type == pygame.KEYUP:
            if event.key == 1073741895:
                print("Theme & RegKeys reloaded")
                UI.ContentManager.ReloadRegistry()
                UI.ThemesManager_LoadTheme(self.DefaultContents.Get_RegKey("/selected_theme"))

