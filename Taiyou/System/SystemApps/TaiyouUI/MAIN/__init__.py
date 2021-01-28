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
import pygame, traceback
from random import randint
from datetime import date
from datetime import datetime
from Library import UI
from System.Core.MAIN import DISPLAY
from System.SystemApps.TaiyouUI.MAIN import TaskBar
from Library import CoreEffects
from Library import CorePrimitives as Shape

class Process(Core.Process):
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs, pProcessIndex):
        self.SomeWindowIsBeingMoved = False
        self.SomeWindowIsBeingMoved_PID = -1
        self.FocusedProcess = None
        self.PlayNotifySound = False
        self.TaskBarSystemFault = False
        self.GUI_ALLOW_TASKMANAGER = True
        self.Zoomlevel = 1.0
        self.ZoomlevelMod = 1.0
        self.ZoomEnabled = False
        self.Timer = pygame.time.Clock()
        self.ImagesResLoaded = False
        self.DefaultContent = Core.CntMng.ContentManager()
        self.TaskBarInstance = TaskBar.TaskBarInstance
        self.DoubleBuffer = None
        self.EnableBackground = False
        self.CurrentCursor = 0
        self.TaskbarActiveCursorReseted = False

        super(Process, self).__init__(pPID, pProcessName, pROOT_MODULE, pInitArgs, pProcessIndex)

        Core.wmm.TaskBarUIProcessID = self.PID

    def Initialize(self):
        print("Initializing TaiyouUI...")
        # Set Invisible Mouse
        pygame.mouse.set_visible(False)

        # -- Default Content --
        self.DefaultContent = Core.CntMng.ContentManager()
        self.DefaultContent.SetSourceFolder("", True)
        self.DefaultContent.SetFontPath("fonts")
        self.DefaultContent.SetImageFolder("img")
        self.DefaultContent.SetRegKeysPath("reg/UI")
        self.DefaultContent.SetSoundPath("sound")
        self.DefaultContent.SetFontPath("fonts")

        self.DefaultContent.InitSoundSystem()
        self.DefaultContent.LoadRegKeysInFolder()
        self.DefaultContent.LoadSoundsInFolder()

        # Load the default Theme File
        UI.ThemesManager_LoadTheme(self.DefaultContent, self.DefaultContent.Get_RegKey("/selected_theme"))

        # Create TaskBar Instance
        self.TaskBarInstance = TaskBar.TaskBarInstance(self.DefaultContent, self)

        self.BGWaxUpdateTimer = 0
        self.BGWaxUpdateInterval = 5
        self.BGWaxSurface = pygame.Surface((5 * 70, 5 * 70))

    def EventUpdate(self):
        if not pygame.fastevent.get_init():
            return

        Core.WindowManagerShared_Event = None
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
                        self.ZoomlevelMod += float(self.DefaultContent.Get_RegKey("/options/zoom_adjust_ammount"))

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
                        self.ZoomlevelMod -= float(self.DefaultContent.Get_RegKey("/options/zoom_adjust_ammount"))

                        if self.ZoomlevelMod <= 1.0:
                            self.ZoomlevelMod = 1.0
                        continue

                if event.key == pygame.K_F11:
                    self.UI_Call_Request()

            if not self.TaskBarInstance.Enabled:
                # Do Focused Process Event Update
                try:
                    self.FocusedProcess.EventUpdate(event)
                    self.FocusedProcess.DRAW_STOP = False

                except:
                    if self.FocusedProcess is not None:
                        print("Application {0} has failed while Event Updating.".format(self.FocusedProcess.TITLEBAR_TEXT))
                        print(traceback.format_exc())

                        self.FocusedProcess.ProcessError()
                    self.FocusedProcess = None

                # Update Process Events
                for process in Core.ProcessAccess:
                    # Check if current procesas is not TaiyouUI itself
                    if process.PID == self.PID:
                        continue

                    # Check if is window, and update it
                    if process.IS_GRAPHICAL:
                        if not process.FULLSCREEN:
                            self.UpdateProcessWindowDrag(event, process)

                        # Stop Rendering Un-Focused Process
                        if process is not self.FocusedProcess:
                            process.DRAW_STOP = True

            else:
                # Update TaskBar Input Handling
                self.TaskBarInstance.EventUpdate(event)
                Core.WindowManagerShared_Event = None

    def SingleInstanceFocus(self):
        if len(Core.ProcessAccess) == 2:
            for process in Core.ProcessAccess:
                if process.PID != self.PID:
                    process.APPLICATION_HAS_FOCUS = True
                    self.FocusedProcess = process

    def UI_Call_Request(self):
        # Ignore request if GUI_TASKMANAGER is not allowed
        if not self.GUI_ALLOW_TASKMANAGER:
            print("GUI is not allowed, skipping request...")
            return

        self.TaskBarInstance.Toggle()

    def UpdateProcessWindowDrag(self, event, process):
        if self.FocusedProcess is None:
            return

        if self.FocusedProcess.FULLSCREEN or self.FocusedProcess.FRAMELESS:
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
        Clock = pygame.time.Clock()
        while self.Running:
            Clock.tick(60)

            if not self.ImagesResLoaded:
                self.ImagesResLoaded = True
                self.DefaultContent.LoadImagesInFolder()

            # Check if SystemFault has been occurred
            if Core.MAIN.SystemFault_Trigger:
                Core.MAIN.SystemFault_Trigger = False
                self.TaskBarInstance.SetMode(1)
                self.UI_Call_Request()

            Core.MAIN.DrawingCode = self.DrawScreen
            Core.MAIN.EventUpdateCode = self.EventUpdate

            # Single-Instance Application Focus
            self.SingleInstanceFocus()

            # Play Notify Sound
            if self.PlayNotifySound:
                self.PlayNotifySound = False
                self.DefaultContent.PlaySound("/notify.wav")

    def BackgroundGenerator(self):
        self.BGWaxUpdateTimer += 1

        if self.BGWaxUpdateTimer >= self.BGWaxUpdateInterval:
            self.BGWaxUpdateTimer = 0
            self.BGWaxUpdateInterval = randint(int(self.DefaultContent.Get_RegKey("/dynamic_bg/interval_min")), int(self.DefaultContent.Get_RegKey("/dynamic_bg/interval_max")))
            RenderEffect = pygame.Surface((5 * 70, 5 * 70))

            for x in range(0, 5):
                for y in range(0, 5):
                    Color = (
                        randint(int(self.DefaultContent.Get_RegKey("/dynamic_bg/min_value")), int(self.DefaultContent.Get_RegKey("/dynamic_bg/max_value"))),
                        randint(int(self.DefaultContent.Get_RegKey("/dynamic_bg/min_value")), int(self.DefaultContent.Get_RegKey("/dynamic_bg/max_value"))),
                        randint(int(self.DefaultContent.Get_RegKey("/dynamic_bg/min_value")), int(self.DefaultContent.Get_RegKey("/dynamic_bg/max_value")))
                    )

                    Shape.Shape_Rectangle(RenderEffect, Color, (x * 70, y * 70, 70, 70))

            self.BGWaxSurface = pygame.transform.scale(CoreEffects.Surface_Blur(RenderEffect, 150), (Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight))

        DISPLAY.blit(self.BGWaxSurface, (0, 0))

        today = date.today()
        DateText = "{0}".format(today.strftime(self.DefaultContent.Get_RegKey("/dynamic_bg/date_format")))
        now = datetime.now()
        TimeText = "{0}".format(now.strftime(self.DefaultContent.Get_RegKey("/dynamic_bg/hour_format")))

        self.DefaultContent.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 38, DateText, (50, 50, 50), 12, 12)
        self.DefaultContent.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 24, TimeText, (50, 50, 50), 12, 52)

        self.DefaultContent.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 24, TimeText, (150, 150, 150), 10, 50)
        self.DefaultContent.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 38, DateText, (150, 150, 150), 10, 10)

    def DrawScreen(self):
        # Draw the Applications Window

        if self.DefaultContent.Get_RegKey("/dynamic_bg/enabled").lower() == "true":
            if self.EnableBackground and not self.TaskBarInstance.Enabled:
                self.BackgroundGenerator()
        else:
            DISPLAY.fill(UI.ThemesManager_GetProperty("BackgroundFillColor"))

        self.EnableBackground = True
        if not self.TaskBarInstance.Enabled and not self.TaskBarSystemFault:
            # Restart cursor next time enters to TaskBar
            self.TaskbarActiveCursorReseted = False

            # Draw the Unfocused Process
            for process in Core.ProcessAccess:
                # Check if current process is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                # Skip Non-Graphical Process
                if not process.IS_GRAPHICAL:
                    continue

                if process.FULLSCREEN:
                    self.EnableBackground = False

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
                if not self.FocusedProcess is None:
                    try:
                        ProcessExists = Core.ProcessAccess_PID.index(self.FocusedProcess.PID)

                        self.DrawProcess(self.FocusedProcess)
                    except ValueError:
                        pass

                else:
                    if len(Core.ProcessAccess_PID) > 1:
                        self.FocusedProcess = Core.ProcessAccess[len(Core.ProcessAccess)]

            except Exception:
                print("TaiyouUI.ApplicationError at (Active application rendering).")
                print(traceback.format_exc())
                self.FocusedProcess = None
                self.CurrentCursor = 0

            self.TaskBarInstance.Set_LastDisplayFrame(DISPLAY)
            # WORKAROUND: Fix rendering bug
            # Update Process Events
            for process in Core.ProcessAccess:
                if self.FocusedProcess is None:
                    break

                # Check if current procesas is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                if process.PID != self.FocusedProcess.PID:
                    process.APPLICATION_HAS_FOCUS = False

        elif self.TaskBarInstance.Enabled and not self.TaskbarActiveCursorReseted:
            self.TaskbarActiveCursorReseted = True
            self.CurrentCursor = 0

            for process in Core.ProcessAccess:
                # Check if current process is not TaiyouUI itself
                if process.PID == self.PID:
                    continue

                # Skip Non-Graphical Process
                if not process.IS_GRAPHICAL:
                    continue

                process.DRAW_STOP = True

        # Draw and update the Taskbar UI
        self.TaskBarInstance.Update()
        self.TaskBarInstance.Draw(DISPLAY)

        self.DrawCursor()
        self.DrawZoom()

    def DrawZoom(self):
        if self.ZoomEnabled:
            if self.Zoomlevel > self.ZoomlevelMod:
                self.Zoomlevel -= abs(self.Zoomlevel - self.ZoomlevelMod) / int(self.DefaultContent.Get_RegKey("/options/zoom_animation_scale"))

            if self.Zoomlevel < self.ZoomlevelMod:
                self.Zoomlevel += abs(self.Zoomlevel - self.ZoomlevelMod) / int(self.DefaultContent.Get_RegKey("/options/zoom_animation_scale"))

            if self.Zoomlevel < 1:
                self.Zoomlevel = 1

            WaxResult = pygame.Surface((Core.MAIN.ScreenWidth / self.Zoomlevel, Core.MAIN.ScreenHeight / self.Zoomlevel))
            WaxResult.blit(DISPLAY, (0, 0), (pygame.mouse.get_pos()[0] - WaxResult.get_width() / 2, pygame.mouse.get_pos()[1] - WaxResult.get_height() / 2, WaxResult.get_width(), WaxResult.get_height()))
            DISPLAY.blit(pygame.transform.scale(WaxResult, (800, 600)), (0, 0))

    def DrawCursor(self):
        # Draw the Cursor
        CursorPath = "/cursor/{0}".format(self.CurrentCursor)
        if self.DefaultContent.KeyExists(CursorPath):
            self.DefaultContent.ImageRender(DISPLAY, self.DefaultContent.Get_RegKey(CursorPath), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        else:
            self.DefaultContent.ImageRender(DISPLAY, self.DefaultContent.Get_RegKey("/cursor/0"), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def DrawFullscreenProcess(self, process):
        try:
            if process.LAST_SURFACE.get_width() < DISPLAY.get_width() or process.LAST_SURFACE.get_height() < DISPLAY.get_height():
                pygame.transform.scale(process.LAST_SURFACE, (DISPLAY.get_width(), DISPLAY.get_height()), DISPLAY)
                return

            DISPLAY.blit(process.LAST_SURFACE, (0, 0))

        except:
            print("TaiyouUI.RenderingError : Error while rendering focused fullscreen application.")
            print(traceback.format_exc())

    def DrawProcess(self, process):
        if process is None:
            return

        try:
            # Set Cursor
            self.CurrentCursor = process.CURSOR

            # If is fullscreen process, just draw at max resolution at 0, 0
            if process.FULLSCREEN:
                # If application has focus, draw again it's content
                if process.APPLICATION_HAS_FOCUS:
                    self.DrawFullscreenProcess(process)

                # If not, just draw a copy of its screen
                self.DrawFullscreenProcess(process)

                if not process.APPLICATION_HAS_FOCUS:
                    WindowGeometry = [process.POSITION[0], process.POSITION[1], process.DISPLAY.get_width() + 1, process.DISPLAY.get_height()]
                    process.TITLEBAR_RECTANGLE = pygame.Rect(WindowGeometry[0], WindowGeometry[1], DISPLAY.get_width(), 15)

                    # Draw the title bar
                    TitleBarColor = UI.ThemesManager_GetProperty("WM_FullscreenWindowTitleBarColor")
                    TextColor = UI.ThemesManager_GetProperty("WM_FullscreenWindowTitleBarTextColor")

                    Shape.Shape_Rectangle(DISPLAY, TitleBarColor, (0, 0, process.TITLEBAR_RECTANGLE[2] + 1, process.TITLEBAR_RECTANGLE[3]))

                    # Draw Title Bar Text
                    TitleBarText = process.TITLEBAR_TEXT
                    FontSize = 12
                    Font = "/Ubuntu.ttf"

                    self.DefaultContent.FontRender(DISPLAY, Font, FontSize, TitleBarText, TextColor, DISPLAY.get_width() / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0)
                return

            # If not, draw window decoration
            if not process.FRAMELESS:
                DISPLAY.blit(self.DrawWindow(process.LAST_SURFACE, process), (process.POSITION[0], process.POSITION[1]))
            else:
                DISPLAY.blit(process.LAST_SURFACE, (process.POSITION[0], process.POSITION[1]))

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
        if process.WINDOW_SURFACE is None:
            process.WINDOW_SURFACE = pygame.Surface((WindowGeometry[2] + 1, WindowGeometry[3] + process.TITLEBAR_RECTANGLE[3] + 1))
        process.TITLEBAR_RECTANGLE = pygame.Rect(WindowGeometry[0], WindowGeometry[1], WindowGeometry[2], 15)

        # Draw the title bar
        TitleBarColor = UI.ThemesManager_GetProperty("WM_TitlebarActiveColor")
        WindowBorderColor = UI.ThemesManager_GetProperty("WM_BorderActiveColor")
        TextColor = UI.ThemesManager_GetProperty("WM_TitlebarTextActiveColor")
        FontSmoothEnabled = True

        if not process.APPLICATION_HAS_FOCUS:
            TitleBarColor = UI.ThemesManager_GetProperty("WM_TitlebarInactiveColor")
            TextColor = UI.ThemesManager_GetProperty("WM_TitlebarTextInactiveColor")
            WindowBorderColor = UI.ThemesManager_GetProperty("WM_BorderInactiveColor")
            FontSmoothEnabled = False

        # Draw window titlebar only when needded.
        if process.WINDOW_SURFACE_LAST_DRAG_STATE != process.WINDOW_DRAG_ENABLED or process.WINDOW_SURFACE_LAST_DRAG_STATE_LAST_GEOMETRY != WindowGeometry:
            process.WINDOW_SURFACE_LAST_DRAG_STATE_LAST_GEOMETRY = WindowGeometry
            process.WINDOW_SURFACE_LAST_DRAG_STATE = process.WINDOW_DRAG_ENABLED
            process.WINDOW_SURFACE.fill(TitleBarColor)

        # Draw the Window Borders
        Shape.Shape_Rectangle(process.WINDOW_SURFACE, WindowBorderColor, (0, 0, process.WINDOW_SURFACE.get_width(), process.WINDOW_SURFACE.get_height()), 1)

        # Draw titlebar background
        Shape.Shape_Rectangle(process.WINDOW_SURFACE, TitleBarColor, (1, 1, process.TITLEBAR_RECTANGLE[2] - 1, process.TITLEBAR_RECTANGLE[3] - 1))

        # Draw Title Bar Text
        TitleBarText = process.TITLEBAR_TEXT
        FontSize = UI.ThemesManager_GetProperty("WM_WINDOWDRAG_TITLEBAR_FONTSIZE")
        Font = UI.ThemesManager_GetProperty("WM_WINDOWDRAG_TITLEBAR_FONTFILE")
        process.LAST_TITLEBAR_TEXT = process.TITLEBAR_TEXT

        # Draw Titlebar Text
        self.DefaultContent.FontRender(process.WINDOW_SURFACE, Font, FontSize, TitleBarText, TextColor, WindowGeometry[2] / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 0, FontSmoothEnabled)

        # Draw the Window Contents
        process.WINDOW_SURFACE.blit(pSurface, (1, process.TITLEBAR_RECTANGLE[3]))

        return process.WINDOW_SURFACE