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
from CoreFiles.System.TaiyouUI.MAIN import UI

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
        self.DefaultContent.InitSoundSystem()
        self.DefaultContent.LoadRegKeysInFolder("Data/reg")
        self.DefaultContent.LoadImagesInFolder("Data/img")
        self.DefaultContent.LoadSoundsInFolder("Data/sound")
        self.DefaultContent.SetFontPath("Data/fonts")

        self.TaskbarEnabled = False
        self.TaskbarDisableToggle = False
        self.TaskbarAnimation = Core.utils.AnimationController(5.5, multiplierRestart=True)
        self.TaskbarTools = pygame.Rect(0, 0, 300, 25)
        self.WindowList = UI.VerticalListWithDescription(pygame.Rect(0, 0, 300, 400), self.DefaultContent)
        self.LastDisplayFrame = DISPLAY.copy()

        self.TaskbarTools_WidgetController = UI.Widget.Widget_Controller(self.DefaultContent, self.TaskbarTools)

        self.TaskbarTools_WidgetController.Append(UI.Widget.Widget_Button(self.DefaultContent, "End Task", 17, 3, 3, 0))
        self.TaskbarTools_WidgetController.Append(UI.Widget.Widget_Button(self.DefaultContent, "Switch", 17, 90, 3, 1))

        self.SomeWindowIsBeingMoved = False
        self.SomeWindowIsBeingMoved_PID = -1

        self.WelcomeScreenAppered = False

    def EventUpdate(self):
        pygame.fastevent.pump()

        # -- Update Event -- #
        for event in pygame.fastevent.get():
            # -- Closes Everthing when clicking on the X button
            if event.type == pygame.QUIT:
                Core.MAIN.Destroy()
                print("Destroy")

            # UI Hotkeys
            if event.type == pygame.KEYUP:
                # -- Open Taskbar -- #
                if event.key == pygame.K_F12:
                    Core.MAIN.CreateProcess(self.DefaultContent.Get_RegKey("/task_manager"), "task_manager")

                # -- Toggle Taskbar -- #
                if event.key == pygame.K_F11:
                    self.ToggleTaskbar()

                # -- Close selected process in TaskbarUI -- #
                if event.key == pygame.K_DELETE:
                    if self.TaskbarEnabled:
                        self.UpdateTaskbar_CloseSelectedProcess()

            if self.TaskbarEnabled:
                self.UpdateTaskbarEvents(event)

            else:
                for process in Core.MAIN.ProcessList:
                    # Check if current process is not TaiyouUI itself
                    if process.PID == self.PID:
                        continue

                    # Check if is window, and update it
                    if process.IS_GRAPHICAL and not self.TaskbarEnabled:
                        if not process.FULLSCREEN:
                            self.UpdateProcessWindowDrag(event, process)

                        if process.APPLICATION_HAS_FOCUS:
                            process.EventUpdate(event)

    def ToggleTaskbar(self):
        self.UpdateTaskbarProcessList()

        if not self.TaskbarEnabled:
            self.TaskbarEnabled = True
            self.TaskbarAnimation.Enabled = True
            if not self.WelcomeScreenAppered:
                self.DefaultContent.PlaySound("/intro_2.wav")
            else:
                self.DefaultContent.PlaySound("/in.wav")

        else:
            print("Out Animation Toggle")
            self.DefaultContent.PlaySound("/out.wav")
            self.TaskbarDisableToggle = True
            self.TaskbarAnimation.Enabled = True

    def UpdateProcessWindowDrag(self, event, process):
        if self.SomeWindowIsBeingMoved:
            if self.SomeWindowIsBeingMoved_PID != process.PID:
                return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            MouseColisionRectangle = pygame.Rect(pos[0], pos[1], 2, 2)

            if MouseColisionRectangle.colliderect(process.TITLEBAR_RECTANGLE):
                process.WindowDragEnable = True
                self.SomeWindowIsBeingMoved = True
                self.SomeWindowIsBeingMoved_PID = process.PID
                process.WindowManagerSignal(0)

        elif event.type == pygame.MOUSEBUTTONUP:
            if process.WindowDragEnable:
                process.WindowDragEnable = False
                self.SomeWindowIsBeingMoved = False
                self.SomeWindowIsBeingMoved_PID = -1

        if process.WindowDragEnable and process.APPLICATION_HAS_FOCUS and self.SomeWindowIsBeingMoved_PID == process.PID:
            pos = pygame.mouse.get_pos()

            self.SomeWindowIsBeingMoved = True
            self.SomeWindowIsBeingMoved_PID = process.PID

            process.POSITION = (pos[0] - process.TITLEBAR_RECTANGLE[2] / 2, pos[1] - process.TITLEBAR_RECTANGLE[3] / 2)

    def Update(self):
        DISPLAY.fill((0, 0, 0))
        ## Draw the Applications Window
        FocusedProcess = None

        if not self.TaskbarEnabled:
            # Draw the Unfocused Process
            for process in Core.MAIN.ProcessList:
                # Skip Non-Graphical Process
                if not process.IS_GRAPHICAL:
                    continue

                if not process.FULLSCREEN:
                    process.TITLEBAR_RECTANGLE = pygame.Rect(process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width(), 15)

                # Check if current process is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                if process.APPLICATION_HAS_FOCUS:
                    FocusedProcess = process
                    continue

                self.DrawProcess(process)

            # Draw the focused process
            self.DrawProcess(FocusedProcess)

        if not self.TaskbarEnabled:
            self.LastDisplayFrame = DISPLAY.copy()

        # Draw and update the Taskbar UI
        self.UpdateTaskbar()

        # Draw the Cursor
        self.DefaultContent.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        pygame.display.flip()

        # Update Applications Events
        self.EventUpdate()

    def DrawProcess(self, process):
        if process is None:
            return

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
                return

            # If not, just draw a copy of its screen
            DISPLAY.blit(process.LAST_SURFACE, (0, 0))
            if not process.APPLICATION_HAS_FOCUS:
                WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height()]

                # Draw the title bar
                TitleBarColor = (39, 54, 159)
                TextColor = (200, 200, 200)

                Core.shape.Shape_Rectangle(DISPLAY, TitleBarColor, (0, 0, process.TITLEBAR_RECTANGLE[2] + 1, process.TITLEBAR_RECTANGLE[3]))

                # Draw Title Bar Text
                TitleBarText = process.TITLEBAR_TEXT
                FontSize = 12
                Font = "/Ubuntu.ttf"

                self.DefaultContent.FontRender(DISPLAY, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)

            return

        # If not, draw window decoration
        DISPLAY.blit(self.DrawWindow(process.Draw(), process), (process.POSITION[0], process.POSITION[1]))

    def UpdateTaskbar(self):
        if not self.TaskbarEnabled: return
        self.TaskbarAnimation.Update()

        # Check if wax is being disabled
        if self.TaskbarDisableToggle and not self.TaskbarAnimation.Enabled and self.TaskbarAnimation.Value == self.TaskbarAnimation.MinValue:
            self.TaskbarDisableToggle = False
            self.TaskbarEnabled = False
            self.WelcomeScreenAppered = True

        # Draw the Blurred Background
        DISPLAY.blit(Core.fx.Surface_Blur(self.LastDisplayFrame, self.TaskbarAnimation.Value - 25), (0, 0))

        # Contents Surface
        ContentsSurface = pygame.Surface((self.LastDisplayFrame.get_width(), self.LastDisplayFrame.get_height()), pygame.SRCALPHA)
        ContentsSurface.set_alpha(self.TaskbarAnimation.Value)

        TitleText = "Current Activity"
        if not self.WelcomeScreenAppered:
            TitleText = "Welcome"
        TitleFontSize = 58
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), DISPLAY.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

        self.WindowList.Render(ContentsSurface)

        # Render TaskbarTools Background
        Core.shape.Shape_Rectangle(ContentsSurface, (20, 20, 60), self.TaskbarTools)
        Core.shape.Shape_Rectangle(ContentsSurface, (94, 114, 219), (self.TaskbarTools[0] - 2, self.TaskbarTools[1] - 2, self.TaskbarTools[2] + 4, self.TaskbarTools[3] + 4), BorderWidth=2)

        # Render Close Button
        self.TaskbarTools_WidgetController.Draw(ContentsSurface)

        DISPLAY.blit(ContentsSurface, (0, 0))

        # Center Window list
        self.WindowList.Set_X(DISPLAY.get_width() / 2 - self.WindowList.Rectangle[2] / 2)
        self.WindowList.Set_Y(DISPLAY.get_height() / 2 - self.WindowList.Rectangle[3] / 2)

        # Set TaskbarTools Cordinate
        self.TaskbarTools[0] = self.WindowList.Rectangle[0]
        self.TaskbarTools[1] = self.WindowList.Rectangle.bottom

        # WindowList Buttons
        self.TaskbarTools_WidgetController.Rectangle = self.TaskbarTools

        self.TaskbarTools_WidgetController.Update()

        if self.TaskbarTools_WidgetController.LastInteractionID == 0 and self.TaskbarTools_WidgetController.LastInteractionType:
            self.UpdateTaskbar_CloseSelectedProcess()

        if self.TaskbarTools_WidgetController.LastInteractionID == 1 and self.TaskbarTools_WidgetController.LastInteractionType:
            self.UpdateTaskbar_SwitchToSelectedProcess()


    def UpdateTaskbar_SwitchToSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
            Process = Core.MAIN.ProcessList[Core.MAIN.GetProcessIndexByPID(ProcessPID)]

            Process.WindowManagerSignal(0)

            self.ToggleTaskbar()


    def UpdateTaskbar_CloseSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
            Core.MAIN.KillProcessByPID(ProcessPID)
            self.UpdateTaskbarProcessList()

    def UpdateTaskbarProcessList(self):
        # Update WindowList Contents
        self.WindowList.ClearItems()
        self.WindowList.ResetSelectedItem()

        for process in Core.MAIN.ProcessList:
            if process.PID == self.PID:
                continue
            self.WindowList.AddItem(process.NAME, "PID: " + str(process.PID), ItemProperties=process.PID)

    def UpdateTaskbarEvents(self, event):
        self.WindowList.Update(event)

        self.TaskbarTools_WidgetController.EventUpdate(event)

    def DrawWindow(self, pSurface, process):
        WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height()]
        Surface = pygame.Surface((WindowGeometry[2] + 1, WindowGeometry[3] + process.TITLEBAR_RECTANGLE[3] + 1))

        # Draw the title bar
        TitleBarColor = (20, 20, 58)
        WindowBorderColor = (94, 114, 219)
        TextColor = (240, 240, 240)
        if not process.APPLICATION_HAS_FOCUS:
            TitleBarColor = (39, 54, 159)
            TextColor = (200, 200, 200)
            WindowBorderColor = (20, 20, 58)
            pSurface = Core.fx.Surface_Blur(pSurface, 1.2)

        Core.shape.Shape_Rectangle(Surface, TitleBarColor, (0, 0, process.TITLEBAR_RECTANGLE[2] + 1, process.TITLEBAR_RECTANGLE[3]))

        # Draw Title Bar Text
        TitleBarText = process.TITLEBAR_TEXT
        FontSize = 12
        Font = "/Ubuntu.ttf"
        if process.WindowDragEnable:
            TitleBarText = "||||||||||"
            self.DefaultContent.FontRender(Surface, Font, FontSize, TitleBarText, (TextColor[0] - 100, TextColor[1] - 100, TextColor[2] - 100), WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2 - 1, -1)

        self.DefaultContent.FontRender(Surface, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)

        # Draw the Window Borders
        Core.shape.Shape_Rectangle(Surface, WindowBorderColor, (0, 0, Surface.get_width(), Surface.get_height()), 1)

        # Draw the Window Contents
        Surface.blit(pSurface, (1, process.TITLEBAR_RECTANGLE[3]))

        return Surface
