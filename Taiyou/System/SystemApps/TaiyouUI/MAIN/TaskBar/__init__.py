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
from Library import UI
from Library.UI import Widget
from System.SystemApps.Bootloader.MAIN import ListInstalledApplications
from Library import CoreUtils
from Library import CoreEffects
from Library import CorePrimitives as Shape
from Library import CoreWMControl as WmControl
from Library import CorePaths
from Library import CoreAccess

class TaskBarInstance():
    def __init__(self, pDefaultContent, pRootProcess):
        self.Enabled = False
        self.DisableToggle = False
        self.RootProcess = pRootProcess
        self.Animation = CoreUtils.AnimationController(3, multiplierRestart=True)
        self.CurrentMode = None
        self.GoToModeWhenReturning = None
        self.DefaultContent = pDefaultContent
        self.LastDisplayFrame = pygame.Surface((Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight), pygame.HWACCEL | pygame.HWSURFACE)
        self.Workaround_RenderLastFrame = False
        self.BluredBackgroundResult = pygame.Surface((0, 0), pygame.HWACCEL | pygame.HWSURFACE)

        self.SetMode(0)

    def SetMode(self, pModeID):
        if not self.CurrentMode is None:
            del self.CurrentMode

        if pModeID == 0:
            self.CurrentMode = ApplicationSelectorMode_Instace(self.DefaultContent, self)
            return

        elif pModeID == 1:
            self.CurrentMode = SystemFault_Instance(self.DefaultContent, self)
            return

        elif pModeID == 2:
            self.CurrentMode = ApplicationDashboard_Instace(self.DefaultContent, self)
            return
        else:
            raise Exception("The mode ID {0} is invalid.".format(pModeID))

    def Set_LastDisplayFrame(self, pDisplay):
        self.LastDisplayFrame = pDisplay.copy()

    def Toggle(self):
        if Core.MAIN.SystemFault_Trigger:
            self.Enabled = True

        if not self.Enabled:
            self.Enabled = True
            self.Animation.Enabled = True
            self.Workaround_RenderLastFrame = False

            # Play Error Sound when the UI opened on a System Fault
            if not Core.MAIN.SystemFault_Trigger:
                # Play Opening Sound
                self.CurrentMode.Toggle()
                self.DefaultContent.PlaySound("/in.wav", UI.SystemSoundsVolume)

            else:  # Play error sound when returning from System Fault
                self.DefaultContent.PlaySound("/error.wav", UI.SystemSoundsVolume)

        else:
            self.DisableToggle = True
            self.Animation.Enabled = True
            self.DefaultContent.PlaySound("/out.wav", UI.SystemSoundsVolume)

    def Update(self):
        # Check if wax is being disabled
        if self.DisableToggle and not self.Animation.Enabled and self.Animation.Value == self.Animation.MinValue:
            self.DisableToggle = False
            self.Enabled = False
            self.Welcome = True

        if not self.Enabled:
            return

        self.Animation.Update()

        if hasattr(self, "CurrentMode"):
            self.CurrentMode.Update()

    def Draw(self, DISPLAY):
        # Draw the Blurred Background
        if self.Animation.Value == 0 and not self.Animation.Enabled and not self.Workaround_RenderLastFrame:
            # Only blur the background wheen needed
            if self.Animation.Value != self.Animation.MaxValue:
                self.BluredBackgroundResult = CoreEffects.Surface_Blur(self.LastDisplayFrame, self.Animation.Value)

            DISPLAY.blit(self.BluredBackgroundResult, (0, 0))

        if not self.Enabled:
            self.Workaround_RenderLastFrame = True
            if self.GoToModeWhenReturning is not None:
                self.SetMode(self.GoToModeWhenReturning)
                self.GoToModeWhenReturning = None
            return

        # Only blur the background wheen needed
        if self.Animation.Value != self.Animation.MaxValue:
            self.BluredBackgroundResult = CoreEffects.Surface_Blur(self.LastDisplayFrame, self.Animation.Value)

        DISPLAY.blit(self.BluredBackgroundResult, (0, 0))
        self.BluredBackgroundResult = self.BluredBackgroundResult.copy()

        if hasattr(self, "CurrentMode"):
            # Contents Surface
            ContentsSurface = pygame.Surface((self.LastDisplayFrame.get_width(), self.LastDisplayFrame.get_height()), pygame.SRCALPHA | pygame.HWACCEL | pygame.HWSURFACE)
            ContentsSurface.set_alpha(self.Animation.Value)

            self.CurrentMode.Draw(ContentsSurface)

            DISPLAY.blit(ContentsSurface, (0, self.Animation.Value - 255))

    def EventUpdate(self, event):
        if not self.Enabled:
            return

        self.CurrentMode.EventUpdate(event)

class ApplicationSelectorMode_Instace:
    def __init__(self, pDefaultContent, pRootObj):
        self.DefaultContent = pDefaultContent
        self.RootObj = pRootObj
        self.Tools = pygame.Rect(0, 0, 300, 25)
        self.WindowList = UI.VerticalListWithDescription(pygame.Rect(0, 0, 300, 400), self.DefaultContent)

        self.Tools_WidgetController = UI.Widget.Widget_Controller(self.DefaultContent, self.Tools)

        self.Tools_WidgetController.Append(UI.Widget.Widget_Button(self.DefaultContent, "End Task", 17, 3, 3, 0))
        self.Tools_WidgetController.Append(UI.Widget.Widget_Button(self.DefaultContent, "Switch", 17, 90, 3, 1))

    def Update(self):
        self.UpdateProcessList()

        # Set TaskbarTools Cordinate
        self.Tools[0] = self.WindowList.Rectangle[0] + int(self.RootObj.Animation.Value - 255) / 30
        self.Tools[1] = self.WindowList.Rectangle.bottom

        # Set WindowList X
        self.WindowList.Rectangle[0] = self.WindowList.Rectangle[0] + int(self.RootObj.Animation.Value - 255) / 25

        # WindowList Buttons
        self.Tools_WidgetController.Rectangle = self.Tools

        self.Tools_WidgetController.Update()

        if self.Tools_WidgetController.LastInteractionID == 0 and self.Tools_WidgetController.LastInteractionType:
            self.CloseSelectedProcess()

        if self.Tools_WidgetController.LastInteractionID == 1 and self.Tools_WidgetController.LastInteractionType:
            self.SwitchToSelectedProcess()

    def Draw(self, ContentsSurface):
        self.RenderTitle(ContentsSurface)
        self.WindowList.Render(ContentsSurface)

        # Render TaskbarTools Background
        Shape.Shape_Rectangle(ContentsSurface, (20, 20, 60), self.Tools)
        Shape.Shape_Rectangle(ContentsSurface, (94, 114, 219), (self.Tools[0] - 2, self.Tools[1] - 2, self.Tools[2] + 4, self.Tools[3] + 4), BorderWidth=2)

        # Render Close Button
        self.Tools_WidgetController.Draw(ContentsSurface)

        self.RenderBottomText(ContentsSurface)
        self.RenderBottomInfosText(ContentsSurface)

        # Center Window list
        self.WindowList.Set_X(ContentsSurface.get_width() / 2 - self.WindowList.Rectangle[2] / 2)
        self.WindowList.Set_Y(ContentsSurface.get_height() / 2 - self.WindowList.Rectangle[3] / 2)

    def RenderTitle(self, ContentsSurface):
        TitleText = "Opened Tasks"
        TitleFontSize = 58
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), int(self.RootObj.Animation.Value - 255) / 10 + ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

    def RenderBottomText(self, ContentsSurface):
        # Draw Bottom Text
        TitleText = "[DELETE] Finish selected task, [SPACEBAR] Switch to selected task, [F12] Open TaskBar Dashboard"
        TitleFontSize = 14
        TextY = 35
        TitleFont = "/Ubuntu.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), int(self.RootObj.Animation.Value - 255) / 10 + ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, ContentsSurface.get_height() - self.DefaultContent.GetFont_height(TitleFont, TitleFontSize, TitleText) - TextY)

    def RenderBottomInfosText(self, ContentsSurface):
        # Draw Bottom Text
        TitleText = "TaskBar v" + Core.Get_TaiyouUIVersion()
        TextY = 15
        TitleFontSize = 12
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), int(self.RootObj.Animation.Value - 255) / 10 + ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, ContentsSurface.get_height() - self.DefaultContent.GetFont_height(TitleFont, TitleFontSize, TitleText) - TextY)

    def EventUpdate(self, event):
        self.WindowList.Update(event)

        self.Tools_WidgetController.EventUpdate(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_DELETE:
            self.CloseSelectedProcess()

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.SwitchToSelectedProcess()

        if event.type == pygame.KEYUP and event.key == pygame.K_F12:
            self.SwitchToDashboard()

    def UpdateProcessList(self):
        # Update WindowList Contents
        self.WindowList.ClearItems()

        for process in CoreAccess.ProcessAccess:
            if process.PID == self.RootObj.RootProcess.PID:
                continue
            # Skip non-graphical processes
            if not process.IS_GRAPHICAL:
                continue

            ProcessHasIcon = False
            ProcessIcon = None

            try:
                if process.ICON is not None:
                    ProcessHasIcon = True
                    ProcessIcon = process.ICON

            except AttributeError:
                ProcessHasIcon = False

            self.WindowList.AddItem(process.TITLEBAR_TEXT, "PID: " + str(process.PID), ItemProperties=process.PID, ItemSprite=ProcessIcon, ItemSpriteIsUnloaded=ProcessHasIcon)

    def CloseSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            try:
                ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
                CoreAccess.KillProcessByPID(ProcessPID)

                self.DefaultContent.PlaySound("/click.wav", UI.SystemSoundsVolume)

            except IndexError:
                self.WindowList.ResetSelectedItem()

            except Exception:
                Core.MAIN.SystemFault_Trigger = True
                Core.MAIN.SystemFault_Traceback = traceback.format_exc()
                Core.MAIN.SystemFault_ProcessObject = None
                WmControl.WindowManagerSignal(None, 4)

                print("AppSeletorModeInstance : Process Error Detected\nin Process PID(unknow)")
                print("Traceback:\n" + Core.MAIN.SystemFault_Traceback)

                # Generate the Crash Log
                Core.MAIN.GenerateCrashLog()
                self.RootObj.SetMode(1)
                self.RootObj.Toggle()

    def SwitchToSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            try:
                ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
                Process = CoreAccess.ProcessAccess[CoreAccess.ProcessAccess_PID.index(ProcessPID)]

                WmControl.WindowManagerSignal(Process, 0)

                self.RootObj.RootProcess.UI_Call_Request()

                self.DefaultContent.PlaySound("/click.wav", UI.SystemSoundsVolume)

            except IndexError:
                self.WindowList.ResetSelectedItem()

    def SwitchToDashboard(self):
        self.DefaultContent.PlaySound("/click.wav", UI.SystemSoundsVolume)

        self.RootObj.SetMode(2)

    def Toggle(self):
        pass

class SystemFault_Instance:
    def __init__(self, pDefaultContent, pRootObj):
        self.DefaultContent = pDefaultContent
        self.RootObj = pRootObj
        self.RootObj.Enabled = True
        self.RootObj.DisableToggle = False
        self.RootObj.Animation.Enabled = True
        self.RootObj.Animation.CurrentMode = True
        self.RootObj.Animation.Value = 0

    def Update(self):
        self.RootObj.GoToModeWhenReturning = 0

    def Draw(self, ContentsSurface):
        # Draw the title
        try:
            ProcessName = Core.MAIN.SystemFault_ProcessObject.NAME
        except:
            ProcessName = "Unknown"

        TitleText = "The process {0} has failed.".format(CoreUtils.ShortString(ProcessName, 40))
        TitleFontSize = 22
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

        # Draw the SystemFault message
        try:
            TitleText = "Title : {0}\nPID : {1}\nExecPath : {2}\n\nDetails about the crash has been saved on logs folder\nlocated in: <root>/logs/.".format(Core.CoreUtils.ShortString(Core.MAIN.SystemFault_ProcessObject.TITLEBAR_TEXT, 35), str(Core.MAIN.SystemFault_ProcessObject.PID), Core.CoreUtils.ShortString(Core.MAIN.SystemFault_ProcessObject.ROOT_MODULE, 35))
        except:
            TitleText = "Cannot obtain process information."
        TitleFontSize = 14
        TitleFont = "/Ubuntu.ttf"
        X = ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2
        Y = 55
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), X + 50, Y)

        # Draw the Warning Icon
        self.DefaultContent.ImageRender(ContentsSurface, "/warning.png", X - 97, Y, 95, 97, True)

        # Draw the Traceback Text
        self.DefaultContent.FontRender(ContentsSurface, "/Ubuntu.ttf", 12, Core.MAIN.SystemFault_Traceback, (240, 240, 240), 2, 175)

        # Draw Bottom Text
        TitleText = "Press [F11] to exit."
        TitleFontSize = 14
        TitleFont = "/Ubuntu_Lite.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, ContentsSurface.get_height() - self.DefaultContent.GetFont_height(TitleFont, TitleFontSize, TitleText) - 15)

    def Toggle(self):
        pass

    def EventUpdate(self, event):
        pass

class ApplicationDashboard_Instace:
    def __init__(self, pDefaultContent, pRootObj):
        self.DefaultContent = pDefaultContent
        self.RootObj = pRootObj

        self.ApplicationSelector = UI.ApplicationSelector(pDefaultContent, Core.MAIN.ScreenWidth / 2 - 550 / 2, Core.MAIN.ScreenHeight / 2 - 120 / 2)
        self.NoFoldersFound = False

        self.LoadApplicationsList()

        self.BottomButtonsList = Widget.Widget_Controller(pDefaultContent, (5, Core.MAIN.ScreenHeight - 50 - 5, Core.MAIN.ScreenWidth - 10, 50))
        VersionText = "Taiyou Framework v" + CoreUtils.FormatNumber(Core.TaiyouGeneralVersion) + \
                      "\nTaiyou UI/Taskbar v" + Core.Get_TaiyouUIVersion()

        self.BottomButtonsList.Append(Widget.Widget_Label(pDefaultContent, "/Ubuntu_Bold.ttf", VersionText, 14, (200, 200, 200), 5, 5, 0))

        self.ApplicationManagerBarAnimatorDisableToggle = True
        self.ApplicationManagerBarAnimator = CoreUtils.AnimationController(2)
        self.ApplicationManagerBarAnimator.Enabled = False
        self.ApplicationManagerBar = Widget.Widget_Controller(pDefaultContent, (5, 650, Core.MAIN.ScreenWidth - 10, 50))
        self.ApplicationManagerBar.Append(Widget.Widget_Button(pDefaultContent, "Open Application", 14, 5, 5, 0))
        self.ApplicationManagerEnabled = False

        self.TextsBaseX = 0
        self.DisableInput = False

    def LoadApplicationsList(self):
        # List all valid folders
        folder_list = CoreUtils.Directory_FilesList("." + CorePaths.TaiyouPath_CorrectSlash)
        BootFolders = list()
        for file in folder_list:
            if file.endswith(CorePaths.TaiyouPath_CorrectSlash + "boot"):
                BootFolders.append(file)

        ListInstalledApplications(BootFolders, self.ApplicationSelector)

        if len(BootFolders) == 0 or len(self.ApplicationSelector.SeletorItems_ModulePath) == 0:
            self.NoFoldersFound = True

    def Update(self):
        self.RootObj.GoToModeWhenReturning = 0

        self.BottomButtonsList.Update()

        # Update X values
        self.ApplicationSelector.X = Core.MAIN.ScreenWidth / 2 - 550 / 2 + int(self.RootObj.Animation.Value - 255) / 10
        self.BottomButtonsList.Rectangle[0] = 5 + int(self.RootObj.Animation.Value - 255) / 10
        self.TextsBaseX = int(self.RootObj.Animation.Value - 255) / 25

        self.UpdateApplicationManager()

        if self.ApplicationManagerBar.LastInteractionID == 0 and self.ApplicationManagerBar.LastInteractionType is True:
            self.OpenSelectedApp()

    def UpdateApplicationManager(self):
        self.ApplicationManagerBarAnimator.Update()
        self.ApplicationManagerBar.Rectangle[1] = Core.MAIN.ScreenHeight - 100 - 5 - max(2, self.ApplicationManagerBarAnimator.Value) / 10
        self.ApplicationManagerBar.Opacity = self.ApplicationManagerBarAnimator.Value

        self.ApplicationManagerEnabled = self.ApplicationSelector.SelectedItemIndex != -1

        if not self.ApplicationManagerEnabled:
            if not self.ApplicationManagerBarAnimatorDisableToggle and not self.ApplicationManagerBarAnimator.Enabled:
                self.ApplicationManagerBarAnimatorDisableToggle = True
                self.ApplicationManagerBarAnimator.Enabled = True

        else:
            self.ApplicationManagerBar.Update()

            if self.ApplicationManagerBarAnimatorDisableToggle and not self.ApplicationManagerBarAnimator.Enabled:
                self.ApplicationManagerBarAnimatorDisableToggle = False
                self.ApplicationManagerBarAnimator.Enabled = True

    def Draw(self, ContentsSurface):
        self.RenderTitle(ContentsSurface)
        self.RenderApplicationTitle(ContentsSurface)

        self.ApplicationSelector.Draw(ContentsSurface)

        self.BottomButtonsList.Draw(ContentsSurface)

        self.ApplicationManagerBar.Draw(ContentsSurface)

    def RenderTitle(self, ContentsSurface):
        TitleText = "Dashboard"
        TitleFontSize = 58
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), self.TextsBaseX + ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

    def RenderApplicationTitle(self, ContentsSurface):
        # Draw the Selected Application Title
        TitleBarText = self.ApplicationSelector.SelectedItemTitle.rstrip()
        FontSize = 34
        Font = "/Ubuntu.ttf"
        TextColor = (250, 250, 250)
        self.DefaultContent.FontRender(ContentsSurface, Font, FontSize, TitleBarText, TextColor, self.TextsBaseX + Core.MAIN.ScreenWidth / 2 - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, 600 / 2 - 120)

    def InstanceToggled(self):
        pass

    def Toggle(self):
        pass

    def EventUpdate(self, event):
        if self.DisableInput:
            return

        self.ApplicationSelector.EventUpdate(event)

        self.BottomButtonsList.EventUpdate(event)

        if self.ApplicationManagerEnabled:
            self.ApplicationManagerBar.EventUpdate(event)

        ColRect = pygame.Rect(self.ApplicationSelector.X, self.ApplicationSelector.Y, self.ApplicationSelector.Width, self.ApplicationSelector.Height)
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ColRect.collidepoint(pygame.mouse.get_pos()) and self.ApplicationSelector.SelectedItemTitle != "":
            self.OpenSelectedApp()

    def OpenSelectedApp(self):
        self.DisableInput = True
        print("OpenApp : " + self.ApplicationSelector.SelectedItemTitle)

        try:
            # Create the Application Process
            CoreAccess.CreateProcess(self.ApplicationSelector.SelectedItemModulePath, self.ApplicationSelector.SelectedItemModulePath)

            self.RootObj.Toggle()

        except:
            print("Error while opening application in TaiyouUI Dashboard.")
            print(traceback.format_exc())

            CoreAccess.CreateProcess("System{0}SystemApps{0}crash_dialog".format(CorePaths.TaiyouPath_CorrectSlash), "application_crash", (self.ApplicationSelector.SelectedItemTitle, None, None, 1))
            self.RootObj.Toggle()


            """
            Core.MAIN.SystemFault_Traceback = traceback.format_exc()
            Core.MAIN.SystemFault_ProcessObject = None
            WmControl.WindowManagerSignal(None, 4)

            print("AppSeletorModeInstance : Process Error Detected\nin Process PID(unknow)")
            print("Traceback:\n" + Core.MAIN.SystemFault_Traceback)

            # Generate the Crash Log
            """
