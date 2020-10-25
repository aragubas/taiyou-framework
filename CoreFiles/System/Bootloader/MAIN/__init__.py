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

## Required Variables ##
PROCESS_PID = 0
PROCESS_NAME = 0
IS_GRAPHICAL = True
FULLSCREEN = True
POSITION = (0, 0)
DISPLAY = pygame.Surface((800, 600))
APPLICATION_HAS_FOCUS = True

DefaultContent = Core.cntMng.ContentManager

Progress = 0
ProgressAddDelay = 0
ProgressProgression = True
ProgressMax = 100
LoadingComplete = False

def Initialize():
    global DefaultContent
    DefaultContent = Core.cntMng.ContentManager()

    DefaultContent.SetSourceFolder("CoreFiles/System/Bootloader/")
    DefaultContent.LoadRegKeysInFolder("Data/reg")
    DefaultContent.LoadImagesInFolder("Data/img")
    DefaultContent.SetFontPath("Data/fonts")


def EventUpdate(event):
    pass

def Draw():
    global DISPLAY

    ## Fill Write Screen
    DISPLAY.fill((18, 10, 38))

    DrawProgressBar(DISPLAY)

    # Draw the Logo
    LogoPos = (DISPLAY.get_width() / 2 - 231 / 2, DISPLAY.get_height() / 2 - 242, 231, 242)

    DefaultContent.ImageRender(DISPLAY, "/logo.png", LogoPos[0], LogoPos[1], LogoPos[2], LogoPos[3])

    return DISPLAY

def DrawProgressBar(DISPLAY):
    LoadingBarPos = (DISPLAY.get_width() / 2 - 250 / 2, DISPLAY.get_height() / 2 + 10 / 2, 250, 10)
    LoadingBarProgress = (LoadingBarPos[0], LoadingBarPos[1], Core.utils.Get_Percentage(Progress, LoadingBarPos[2], ProgressMax), 10)

    Core.shape.Shape_Rectangle(DISPLAY, (20, 20, 58), LoadingBarPos, 0, LoadingBarPos[3])
    Core.shape.Shape_Rectangle(DISPLAY, (94, 114, 219), LoadingBarProgress, 0, LoadingBarPos[3])


def Update():
    global ProgressProgression
    global Progress
    global ProgressAddDelay
    global LoadingComplete

    if ProgressProgression and not LoadingComplete:
        ProgressAddDelay += 1

        if ProgressAddDelay == 5:
            ProgressAddDelay = 0
            Progress += 1

        if ProgressAddDelay == 2:
            LoadingSteps(Progress)

        if Progress >= ProgressMax and not LoadingComplete:
            LoadingComplete = True

            print("Bootloader : Loading Complete")

            # Finish the Bootloader
            Core.MAIN.KillProcessByPID(PROCESS_PID)

def LoadingSteps(CurrentProgres):
    global LoadingComplete

    if CurrentProgres == 0:
        # Start the SystemUI
        Core.MAIN.CreateProcess("CoreFiles/System/TaiyouUI", "system_ui")

    if CurrentProgres == 1:
        pass
        # Start the Default Application
        Core.MAIN.CreateProcess(Core.GetUserSelectedApplication(), "default")

        # Finish the Loading
        FinishLoadingScreen()

def FinishLoadingScreen():
    global Progress
    global ProgressMax

    ProgressMax = Progress + 5






