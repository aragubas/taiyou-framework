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

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = True

    def Initialize(self):
        pygame.mouse.set_visible(False)
        self.DefaultContent = Core.cntMng.ContentManager()

        self.DefaultContent.SetSourceFolder("CoreFiles/System/TaiyouUI/")
        self.DefaultContent.LoadRegKeysInFolder("Data/reg")
        self.DefaultContent.LoadImagesInFolder("Data/img")
        self.DefaultContent.SetFontPath("Data/fonts")

        self.TaskbarEnabled = False
        self.TaskbarDisableToggle = False
        self.TaskbarAnimation = Core.utils.AnimationController(2.5, multiplierRestart=True)



    def EventUpdate(self):
        pygame.fastevent.pump()

        # -- Update Event -- #
        for event in pygame.fastevent.get():
            # -- Closes Everthing when clicking on the X button
            if event.type == pygame.QUIT:
                Core.MAIN.Destroy()
                return

            # UI Hotkeys
            if event.type == pygame.KEYUP:
                # -- Open Taskbar -- #
                if event.key == pygame.K_F12:
                    Core.MAIN.CreateProcess(self.DefaultContent.Get_RegKey("/task_manager"), "task_manager")
                    return

                # -- Toggle Taskbar -- #
                if event.key == pygame.K_F11:
                    if not self.TaskbarEnabled:
                        self.TaskbarEnabled = True
                        self.TaskbarAnimation.Enabled = True
                        print("In Animation Toggle")

                    else:
                        print("Out Animation Toggle")

                        self.TaskbarDisableToggle = True
                        self.TaskbarAnimation.Enabled = True

            for process in Core.MAIN.ProcessList:
                # Check if current process is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                # Check if is window, and update it
                if process.IS_GRAPHICAL and process.APPLICATION_HAS_FOCUS and not self.TaskbarEnabled:
                    if not process.FULLSCREEN: self.UpdateProcessWindowDrag(event, process)
                    process.EventUpdate(event)

    def UpdateProcessWindowDrag(self, event, process):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            MouseColisionRectangle = pygame.Rect(pos[0], pos[1], 2, 2)

            if MouseColisionRectangle.colliderect(process.TITLEBAR_RECTANGLE):
                process.WindowDragEnable = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if process.WindowDragEnable:
                process.WindowDragEnable = False

        if process.WindowDragEnable:
            pos = pygame.mouse.get_pos()

            process.POSITION = (pos[0] - process.TITLEBAR_RECTANGLE[2] / 2, pos[1] - process.TITLEBAR_RECTANGLE[3] / 2)

    def Update(self):
        DISPLAY.fill((0, 0, 0))
        ## Draw the Applications Window
        for process in Core.MAIN.ProcessList:
            # Skip Non-Graphical Process
            if not process.IS_GRAPHICAL:
                continue

            # Check if current process is not TaiyouUI itself
            if process.PID == self.PID:
                continue

            # If is fullscreen process, just draw at max resolution at 0, 0
            if process.FULLSCREEN:
                # If application has focus, draw again it's content
                if process.APPLICATION_HAS_FOCUS:
                    Surface = process.Draw()

                    # Check if Application Surface has maximum size
                    if Surface.get_width() != DISPLAY.get_width() or Surface.get_height() != DISPLAY.get_height():
                        Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
                        process.DISPLAY = Surface

                    DISPLAY.blit(Surface, (0, 0))
                    continue
                # If not, just draw a copy of its screen
                DISPLAY.blit(process.LAST_SURFACE, (0, 0))
                continue

            # If not, draw window decoration
            DISPLAY.blit(self.DrawWindow(process.Draw(), process), (process.POSITION[0], process.POSITION[1]))

        # Draw and update the Taskbar UI
        self.UpdateTaskbar()

        # Draw the Cursor
        self.DefaultContent.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        pygame.display.flip()

        # Update Applications Events
        self.EventUpdate()

    def UpdateTaskbar(self):
        if not self.TaskbarEnabled: return
        self.TaskbarAnimation.Update()

        # Check if wax is being disabled
        if self.TaskbarDisableToggle and not self.TaskbarAnimation.Enabled and self.TaskbarAnimation.Value == self.TaskbarAnimation.MinValue:
            self.TaskbarDisableToggle = False
            self.TaskbarEnabled = False

        # Draw the Blurred Background
        Core.fx.BlurredRectangle(DISPLAY, (0, 0, DISPLAY.get_width(), DISPLAY.get_height()), self.TaskbarAnimation.Value, self.TaskbarAnimation.Value - 50)

    def DrawWindow(self, pSurface, process):
        WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width(), process.DISPLAY.get_height()]
        Surface = pygame.Surface((WindowGeometry[2], WindowGeometry[2] + process.TITLEBAR_RECTANGLE[3]))

        # Draw the title bar
        TitleBarColor = (94, 114, 219)
        TextColor = (240, 240, 240)
        if not process.APPLICATION_HAS_FOCUS:
            TitleBarColor = (39, 54, 159)
            TextColor = (200, 200, 200)

        Core.shape.Shape_Rectangle(Surface, TitleBarColor, (0, 0, process.TITLEBAR_RECTANGLE[2], process.TITLEBAR_RECTANGLE[3]))

        # Draw Title Bar Text
        TitleBarText = process.TITLEBAR_TEXT
        FontSize = 12
        Font = "/Ubuntu.ttf"
        self.DefaultContent.FontRender(Surface, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)

        # Draw the Window Contents
        Surface.blit(pSurface, (0, process.TITLEBAR_RECTANGLE[3]))

        return Surface
