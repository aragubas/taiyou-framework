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
from Core.MAIN import DISPLAY as DISPLAY

DefaultContent = Core.cntMng.ContentManager

## Required Variables ##
PROCESS_PID = 0
PROCESS_NAME = 0
IS_GRAPHICAL = True
FULLSCREEN = False
POSITION = (50, 50)
DISPLAY = pygame.Surface((150, 200))
APPLICATION_HAS_FOCUS = True
TITLEBAR_RECTANGLE = (POSITION[0], POSITION[1], DISPLAY.get_width(), 15)


def Initialize():
    global DefaultContent
    pygame.mouse.set_visible(False)
    DefaultContent = Core.cntMng.ContentManager()

    DefaultContent.SetSourceFolder("CoreFiles/System/TaskManager/")
    DefaultContent.LoadRegKeysInFolder("Data/reg")
    DefaultContent.LoadImagesInFolder("Data/img")
    DefaultContent.SetFontPath("Data/fonts")


def EventUpdate(event):
    return

def Draw():
    global DISPLAY
    DISPLAY.fill((120, 120, 120))

    return DISPLAY

def Update():
    global TITLEBAR_RECTANGLE

    ## Update the Titlebar
    TITLEBAR_RECTANGLE = (POSITION[0], POSITION[1] - 15, DISPLAY.get_width(), 15)

