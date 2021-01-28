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
import pygame, os, pickle, io, time, traceback, threading
import System.Core as Core
from System.Core import CntMng
from System.Core import MAIN
from System.Core import AppData
import System.Core as tge
from Library import UI

class Process(Core.Process):
    def Initialize(self):
        self.DefaultContent = Core.CntMng.ContentManager()

        self.DefaultContent.SetSourceFolder("", True)
        self.DefaultContent.SetFontPath("fonts")
        self.DefaultContent.SetImageFolder("img")
        self.DefaultContent.SetRegKeysPath("reg/CRASH_DIALOG")
        self.DefaultContent.SetSoundPath("sound")
        self.DefaultContent.SetFontPath("fonts")

        self.DefaultContent.LoadImagesInFolder()
        self.DefaultContent.LoadRegKeysInFolder()
        self.DefaultContent.LoadSoundsInFolder()
        self.CrashSoundPlayed = False

        self.SetVideoMode(False, (420, 140))
        self.CenterWindow()
        self.CrashedProcess_TitlebarName = str(self.INIT_ARGS[0])
        self.CrashedProcess_ProcessName = str(self.INIT_ARGS[1])
        self.CrashedProcess_PID = str(self.INIT_ARGS[2])

        self.SetTitle("{0} has crashed.".format(self.CrashedProcess_TitlebarName))
        self.ICON = self.DefaultContent.GetImage("/error.png")

    def EventUpdate(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.KillProcess()

    def Update(self):
        if not self.CrashSoundPlayed:
            self.CrashSoundPlayed = True
            self.DefaultContent.PlaySound("/error.wav")

    def Draw(self):
        self.DISPLAY.fill((20, 27, 30))
        CrashText = "The process {0}\nhas stopped working.\n\nPID: {1}\nProcessName:{2}\n\nPress ESC to exit".format(self.CrashedProcess_TitlebarName, self.CrashedProcess_PID, self.CrashedProcess_ProcessName)

        self.DefaultContent.ImageRender(self.DISPLAY, "/error.png", 5, 5, 128, 128, SmoothScaling=True)
        self.DefaultContent.FontRender(self.DISPLAY, "/Ubuntu_Bold.ttf", 14, CrashText, (215, 224, 223), 145, 5)

        self.LAST_SURFACE = self.DISPLAY.copy()