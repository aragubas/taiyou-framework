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
IS_GRAPHICAL = False

def Initialize():
    global DefaultContent
    pygame.mouse.set_visible(False)
    DefaultContent = Core.cntMng.ContentManager()

    DefaultContent.SetSourceFolder("CoreFiles/System/TaiyouUI/")
    DefaultContent.LoadRegKeysInFolder("Data/reg")
    DefaultContent.LoadImagesInFolder("Data/img")
    DefaultContent.SetFontPath("Data/fonts")


def EventUpdate():
    # -- Update Event -- #
    for event in pygame.fastevent.get():
        # -- Closes Everthing when clicking on the X button
        if event.type == pygame.QUIT:
            Core.MAIN.Destroy()
            return

        # UI Hotkeys
        if event.type == pygame.KEYUP and event.key == pygame.K_F12:
            Core.MAIN.CreateProcess(DefaultContent.Get_RegKey("/task_manager"), "task_manager")
            return

        for process in Core.MAIN.ProcessList:
            if process.IS_GRAPHICAL and process.APPLICATION_HAS_FOCUS:
                process.EventUpdate(event)

def Update():
    ## Draw the Applications Window
    for process in Core.MAIN.ProcessList:
        if process.IS_GRAPHICAL:
            RenderingPrimitives = DrawWindow(process.Draw(), process)

            DISPLAY.blit(RenderingPrimitives[0], (RenderingPrimitives[1][0], RenderingPrimitives[1][1]))

    ## Fill Write Screen
    DefaultContent.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    pygame.display.flip()

    ## Update Applications Events
    # -- Disable Engine Update when Minimized -- #
    pygame.fastevent.pump()

    EventUpdate()

def DrawWindow(pSurface, process):
    Surface = None
    WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width(), process.DISPLAY.get_height()]

    # If not fullscreen, just draw the surface
    if process.FULLSCREEN:
        # Set the surface to be drawn
        Surface = pSurface

        # Set window to draw at 0, 0 if is fullscreen one
        WindowGeometry[0] = 0
        WindowGeometry[1] = 0

        # Check if surface has maximum size
        if Surface.get_width() != DISPLAY.get_width() or Surface.get_height() != DISPLAY.get_height():
            Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
            process.DISPLAY = Surface
    else:
        Surface = DrawWindowDecoration(pSurface, WindowGeometry, process.TITLEBAR_RECTANGLE)

    return Surface, WindowGeometry

def DrawWindowDecoration(pDISPLAY, WindowGeometry, TitleBarRectangle):
    DISPLAY = pDISPLAY

    # Draw the title bar
    Core.shape.Shape_Rectangle(DISPLAY, (28, 13, 18), TitleBarRectangle)

    return DISPLAY