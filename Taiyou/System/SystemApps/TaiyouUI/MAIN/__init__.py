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
import time, pygame, traceback, math
from System.SystemApps.TaiyouUI.MAIN import UI
from System.Core.MAIN import DISPLAY
from System.SystemApps.TaiyouUI.MAIN import TaskBar
from System.Core import Utils
from System.Core import Fx

class Process(Core.Process):
    def Initialize(self):
        print("Initializing TaiyouUI...")
        # Set Invisible Mouse
        pygame.mouse.set_visible(False)

        self.Timer = pygame.time.Clock()

        # Initialize Content Manager
        self.DefaultContent = Core.CntMng.ContentManager()

        self.DefaultContent.SetSourceFolder("", True)
        self.DefaultContent.SetFontPath("fonts")
        self.DefaultContent.SetImageFolder("img")
        self.DefaultContent.SetRegKeysPath("reg/UI")
        self.DefaultContent.SetSoundPath("sound")
        self.DefaultContent.SetFontPath("fonts")

        self.ImagesResLoaded = False

        self.DefaultContent.InitSoundSystem()
        self.DefaultContent.LoadRegKeysInFolder()
        self.DefaultContent.LoadSoundsInFolder()

        # Load the default Theme File
        UI.ThemesManager_LoadTheme(self.DefaultContent, self.DefaultContent.Get_RegKey("/selected_theme"))

        self.SomeWindowIsBeingMoved = False
        self.SomeWindowIsBeingMoved_PID = -1

        self.FocusedProcess = None

        self.PlayNotifySound = False

        self.TaskBarSystemFault = False

        self.GUI_ALLOW_TASKMANAGER = True

        self.Zoomlevel = 1.0
        self.ZoomlevelMod = 1.0

        self.ZoomEnabled = False

        # Set this process as the WindowManager Process
        Core.wmm.TaskBarUIProcessID = self.PID

        self.TaskBarInstance = TaskBar.TaskBarInstance(self.DefaultContent, self)

    def EventUpdate(self):
        if not pygame.fastevent.get_init():
            return
        pygame.fastevent.pump()

        # -- Update Event -- #
        for event in pygame.fastevent.get():
            LastModKey = pygame.key.get_mods()
            # -- Closes Everthing when clicking on the X button
            if event.type == pygame.QUIT:
                Core.MAIN.Destroy()
                print("Destroy")

            # UI Hotkeys
            if event.type == pygame.KEYUP:
                # -- Increase Zoom -- #
                if LastModKey & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_F11:
                        self.ZoomlevelMod += self.DefaultContent.Get_RegKey("/options/zoom_adjust_ammount", float)

                        if self.ZoomlevelMod >= 10:
                            self.ZoomlevelMod = 10
                        continue

                    if event.key == pygame.K_F12:
                        # -- Toggle Enable Zoom -- #
                        if not self.ZoomEnabled:
                            self.ZoomEnabled = True
                            self.Zoomlevel = 1
                            self.ZoomlevelMod = 1
                        else:
                            self.ZoomEnabled = False
                            self.Zoomlevel = 1
                            self.ZoomlevelMod = 1
                        continue

                if LastModKey & pygame.KMOD_CTRL:
                    # -- Decrease Zoom -- #
                    if event.key == pygame.K_F11:
                        self.ZoomlevelMod -= self.DefaultContent.Get_RegKey("/options/zoom_adjust_ammount", float)

                        if self.ZoomlevelMod <= 1.0:
                            self.ZoomlevelMod = 1.0
                        continue

                if event.key == pygame.K_F11:
                    self.UI_Call_Request()

            if not self.TaskBarInstance.Enabled:
                for process in Core.ProcessAccess:
                    # Check if current process is not TaiyouUI itself
                    if process.PID == self.PID:
                        continue

                    # Check if is window, and update it
                    if process.IS_GRAPHICAL and not self.TaskBarInstance.Enabled:
                        if not process.FULLSCREEN:
                            self.UpdateProcessWindowDrag(event, process)

                        ProcessGeometry = pygame.Rect(process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height())
                        CursorColision = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

                        # Process EventUpdate for the process
                        if process.APPLICATION_HAS_FOCUS and ProcessGeometry.colliderect(CursorColision) and not process.WINDOW_DRAG_ENABLED:
                            try:
                                process.EventUpdate(event)

                            except:
                                print("TaiyouUI.ApplicationError at (EventUpdate)")
                                print(traceback.format_exc())

                        # Play beep sound when clicking on Inactive Window
                        if self.FocusedProcess is not None:
                            FocusedProcessGeometry = pygame.Rect(self.FocusedProcess.POSITION[0], self.FocusedProcess.POSITION[1], self.FocusedProcess.DISPLAY.get_width() + 1, self.FocusedProcess.DISPLAY.get_height())

                            # Play beep sound when clicking on inactive window
                            if event.type == pygame.MOUSEBUTTONUP and ProcessGeometry.colliderect(CursorColision) and not FocusedProcessGeometry.colliderect(CursorColision):
                                self.PlayNotifySound = True

            else:
                # Update TaskBar Input Handling
                self.TaskBarInstance.EventUpdate(event)

    def SingleInstanceFocus(self):
        if len(Core.MAIN.ProcessList) == 2:
            for process in Core.ProcessAccess:
                if process.PID != self.PID:
                    process.APPLICATION_HAS_FOCUS = True
                    process.PRIORITY = -1

    def UI_Call_Request(self):
        # Ignore request if GUI_TASKMANAGER is not allowed
        if not self.GUI_ALLOW_TASKMANAGER:
            print("GUI is not allowed, skipping request...")
            return

        self.TaskBarInstance.Toggle()

    def UpdateProcessWindowDrag(self, event, process):
        try:
            if self.FocusedProcess.FULLSCREEN:
                return
        except AttributeError:
            return

        if self.SomeWindowIsBeingMoved:
            if self.SomeWindowIsBeingMoved_PID != process.PID:
                return

        FocusedProcessColisor = pygame.Rect(self.FocusedProcess.POSITION[0], self.FocusedProcess.POSITION[1], self.FocusedProcess.DISPLAY.get_width(), self.FocusedProcess.DISPLAY.get_height())

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if process != self.FocusedProcess and FocusedProcessColisor.collidepoint(pygame.mouse.get_pos()):
                return

            pos = pygame.mouse.get_pos()

            if process.TITLEBAR_RECTANGLE.collidepoint(pos):
                process.WINDOW_DRAG_ENABLED = True
                self.SomeWindowIsBeingMoved = True
                self.SomeWindowIsBeingMoved_PID = process.PID
                process.WINDOW_DRAG_SP = (process.TITLEBAR_RECTANGLE[0] - pos[0], process.TITLEBAR_RECTANGLE[1] - pos[1])

                Core.wmm.WindowManagerSignal(process, 0)

        elif event.type == pygame.MOUSEBUTTONUP:
            if process.WINDOW_DRAG_ENABLED:
                process.WINDOW_DRAG_ENABLED = False
                self.SomeWindowIsBeingMoved = False
                self.SomeWindowIsBeingMoved_PID = -1

        if process.WINDOW_DRAG_ENABLED and process.APPLICATION_HAS_FOCUS and self.SomeWindowIsBeingMoved_PID == process.PID:
            pos = pygame.mouse.get_pos()

            self.SomeWindowIsBeingMoved = True
            self.SomeWindowIsBeingMoved_PID = process.PID

            process.POSITION = (process.WINDOW_DRAG_SP[0] + pos[0], process.WINDOW_DRAG_SP[1] + pos[1])

    def Update(self):
        while self.Running:
            self.Timer.tick(100)

            if not self.ImagesResLoaded:
                self.ImagesResLoaded = True
                self.DefaultContent.LoadImagesInFolder()

            # Check if SystemFault has been occurred
            if Core.MAIN.SystemFault_Trigger:
                Core.MAIN.SystemFault_Trigger = False
                self.TaskBarInstance.SetMode(1)
                self.UI_Call_Request()

            # Update Applications Events
            self.EventUpdate()

            Core.MAIN.DrawingCode = self.DrawScreen

            # Single-Instance Application Focus
            self.SingleInstanceFocus()

            # Play Notify Sound
            if self.PlayNotifySound:
                self.PlayNotifySound = False
                self.DefaultContent.PlaySound("/notify.wav")

    def DrawScreen(self):
        # Draw the Applications Window
        if not self.TaskBarInstance.Enabled and not self.TaskBarSystemFault:
            # Draw the Unfocused Process
            for process in Core.ProcessAccess:
                # Skip Non-Graphical Process
                if not process.IS_GRAPHICAL:
                    continue

                # Check if current process is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                # Set Process Titlebar
                if not process.FULLSCREEN:
                    process.TITLEBAR_RECTANGLE = pygame.Rect(process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width(), 15)

                if process.APPLICATION_HAS_FOCUS:
                    self.FocusedProcess = process
                    continue

                try:
                    self.DrawProcess(process)
                except:
                    print("TaiyouUI.ApplicationError at (Non-Active application rendering).")
                    print(traceback.format_exc())

            # Draw the focused process
            try:
                if not self.FocusedProcess == None:
                    ProcessExists = Core.ProcessAccess_PID.index(self.FocusedProcess.PID)

                    self.DrawProcess(self.FocusedProcess)

            except Exception:
                print("TaiyouUI.ApplicationError at (Active application rendering).")
                print(traceback.format_exc())
                self.FocusedProcess = None

            self.TaskBarInstance.Set_LastDisplayFrame(DISPLAY)

        # Draw and update the Taskbar UI
        self.TaskBarInstance.Update()
        self.TaskBarInstance.Draw(DISPLAY)

        self.DrawCursor()

        if self.ZoomEnabled:
            if self.Zoomlevel > self.ZoomlevelMod:
                self.Zoomlevel -= abs(self.Zoomlevel - self.ZoomlevelMod) / self.DefaultContent.Get_RegKey("/options/zoom_animation_scale", int)

            if self.Zoomlevel < self.ZoomlevelMod:
                self.Zoomlevel += abs(self.Zoomlevel - self.ZoomlevelMod) / self.DefaultContent.Get_RegKey("/options/zoom_animation_scale", int)

            if self.Zoomlevel < 1:
                self.Zoomlevel = 1

            WaxResult = pygame.Surface((Core.MAIN.ScreenWidth / self.Zoomlevel, Core.MAIN.ScreenHeight / self.Zoomlevel))
            WaxResult.blit(DISPLAY, (0, 0), (pygame.mouse.get_pos()[0] - WaxResult.get_width() / 2, pygame.mouse.get_pos()[1] - WaxResult.get_height() / 2, WaxResult.get_width(), WaxResult.get_height()))
            DISPLAY.blit(pygame.transform.scale(WaxResult, (800, 600)), (0, 0))

    def DrawCursor(self):
        # Draw the Cursor
        self.DefaultContent.ImageRender(DISPLAY, "/pointer.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def DrawProcess(self, process):
        if process is None:
            return

        try:
            # If is fullscreen process, just draw at max resolution at 0, 0
            if process.FULLSCREEN:
                # If application has focus, draw again it's content
                if process.APPLICATION_HAS_FOCUS:
                    try:
                        Surface = process.Draw()

                        # Check if Application Surface has maximum size
                        if Surface.get_width() != DISPLAY.get_width() or Surface.get_height() != DISPLAY.get_height():
                            Surface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
                            process.DISPLAY = Surface

                        DISPLAY.blit(Surface, (0, 0))
                        return

                    except:
                        return

                # If not, just draw a copy of its screen
                DISPLAY.blit(process.LAST_SURFACE, (0, 0))
                if not process.APPLICATION_HAS_FOCUS:
                    WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height()]
                    process.TITLEBAR_RECTANGLE = pygame.Rect(WindowGeometry[0], WindowGeometry[1], WindowGeometry[2], 15)

                    # Draw the title bar
                    TitleBarColor = (39, 54, 159)
                    TextColor = (200, 200, 200)

                    Core.Shape.Shape_Rectangle(DISPLAY, TitleBarColor, (0, 0, process.TITLEBAR_RECTANGLE[2] + 1, process.TITLEBAR_RECTANGLE[3]))

                    # Draw Title Bar Text
                    TitleBarText = process.TITLEBAR_TEXT
                    FontSize = 12
                    Font = "/Ubuntu.ttf"

                    self.DefaultContent.FontRender(DISPLAY, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)
                return

            # If not, draw window decoration
            DISPLAY.blit(self.DrawWindow(process.Draw(), process), (process.POSITION[0], process.POSITION[1]))

        except:
            Core.MAIN.SystemFault_Trigger = True
            Core.MAIN.SystemFault_Traceback = traceback.format_exc()
            Core.MAIN.SystemFault_ProcessObject = process
            self.FocusedProcess = None
            self.TaskBarInstance.SetMode(1)
            Core.wmm.WindowManagerSignal(None, 4)
            self.UI_Call_Request()
            print("TaiyouApplicationDrawLoop : Process Error Detected\nin Process PID({0})".format(process.PID))
            print("Traceback:\n" + Core.MAIN.SystemFault_Traceback)

            # Kill the Process
            try:
                Core.MAIN.KillProcessByPID(process.PID)
            except:
                print("Error while killing process")

            # Generate the Crash Log
            Core.MAIN.GenerateCrashLog()
            return

    def DrawWindow(self, pSurface, process):
        WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height()]
        Surface = pygame.Surface((WindowGeometry[2] + 1, WindowGeometry[3] + process.TITLEBAR_RECTANGLE[3] + 1))
        process.TITLEBAR_RECTANGLE = pygame.Rect(WindowGeometry[0], WindowGeometry[1], WindowGeometry[2], 15)

        # Draw the title bar
        TitleBarColor = UI.ThemesManager_GetProperty("WM_TitlebarActiveColor")
        WindowBorderColor = UI.ThemesManager_GetProperty("WM_BorderActiveColor")
        TextColor = UI.ThemesManager_GetProperty("WM_TitlebarTextActiveColor")
        if not process.APPLICATION_HAS_FOCUS:
            TitleBarColor = UI.ThemesManager_GetProperty("WM_TitlebarInactiveColor")
            TextColor = UI.ThemesManager_GetProperty("WM_TitlebarTextInactiveColor")
            WindowBorderColor = UI.ThemesManager_GetProperty("WM_BorderInactiveColor")

        # Draw window titlebar
        Surface.fill(TitleBarColor)

        # Draw Title Bar Text
        TitleBarText = process.TITLEBAR_TEXT
        FontSize = UI.ThemesManager_GetProperty("WM_WINDOWDRAG_TITLEBAR_FONTSIZE")
        Font = UI.ThemesManager_GetProperty("WM_WINDOWDRAG_TITLEBAR_FONTFILE")
        if process.WINDOW_DRAG_ENABLED:
            TitleBarText = UI.ThemesManager_GetProperty("WM_WINDOWDRAG_TITLEBAR")
            self.DefaultContent.FontRender(Surface, Font, FontSize, TitleBarText, (TextColor[0] - 100, TextColor[1] - 100, TextColor[2] - 100), WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2 - 1, -1)

        # Draw Titlebar Text
        self.DefaultContent.FontRender(Surface, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)

        # Draw the Window Borders
        Core.Shape.Shape_Rectangle(Surface, WindowBorderColor, (0, 0, Surface.get_width(), Surface.get_height()), 1)

        # Draw the Window Contents
        Surface.blit(pSurface, (1, process.TITLEBAR_RECTANGLE[3]))

        return Surface
