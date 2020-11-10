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
import Core, pygame
from Core import utils
from CoreFiles.System.TaiyouUI.MAIN import UI

class TaskBarInstance:
    def __init__(self, pDefaultContent, pRootProcess):
        self.Enabled = False
        self.DisableToggle = False
        self.RootProcess = pRootProcess
        self.Animation = utils.AnimationController(5.5, multiplierRestart=True)
        self.CurrentMode = None
        self.Welcome = False
        self.GoToModeWhenReturning = None
        self.DefaultContent = pDefaultContent
        self.LastDisplayFrame = pygame.Surface((800, 600))
        self.Workaround_RenderLastFrame = False

    def SetMode(self, pModeID):
        if not self.CurrentMode is None:
            del self.CurrentMode

        if pModeID == 0:
            self.CurrentMode = ApplicationSelectorMode_Instace(self.DefaultContent, self)
            return

        if pModeID == 1:
            self.CurrentMode = SystemFault_Instance(self.DefaultContent, self)
            return

    def Set_LastDisplayFrame(self, pDisplay):
        self.LastDisplayFrame = pDisplay.copy()

    def Toggle(self):
        if not self.Enabled:
            self.Enabled = True
            self.Animation.Enabled = True
            self.Workaround_RenderLastFrame = False

            # Play Error Sound when the UI opened on a System Fault
            if not Core.MAIN.SystemFault_Trigger:
                # Play Welcome Sound when opening the UI for the first time
                if not self.Welcome:
                    self.DefaultContent.PlaySound("/intro_2.wav")
                    print("Task_Bar : Welcome")

                else:  # Play the Opening Sound when not opening for the First Time
                    self.CurrentMode.Toggle()
                    self.DefaultContent.PlaySound("/in.wav")

            else:  # Play error sound when returning from System Fault
                self.DefaultContent.PlaySound("/error.wav")

        else:
            self.DisableToggle = True
            self.Animation.Enabled = True
            self.DefaultContent.PlaySound("/out.wav")

    def Update(self):
        # Check if wax is being disabled
        if self.DisableToggle and not self.Animation.Enabled and self.Animation.Value == self.Animation.MinValue:
            self.DisableToggle = False
            self.Enabled = False
            self.Welcome = True

        if not self.Enabled:
            return

        self.Animation.Update()
        self.CurrentMode.Update()

    def Draw(self, DISPLAY):
        # Draw the Blurred Background
        if self.Animation.Value == 0 and not self.Animation.Enabled and not self.Workaround_RenderLastFrame:
            DISPLAY.blit(Core.fx.Surface_Blur(self.LastDisplayFrame, self.Animation.Value - 25), (0, 0))

        if not self.Enabled:
            self.Workaround_RenderLastFrame = True
            if self.GoToModeWhenReturning is not None:
                self.SetMode(self.GoToModeWhenReturning)
                self.GoToModeWhenReturning = None

            return

        # Render blurred copy of screen
        DISPLAY.blit(Core.fx.Surface_Blur(self.LastDisplayFrame, self.Animation.Value - 25), (0, 0))

        # Contents Surface
        ContentsSurface = pygame.Surface((self.LastDisplayFrame.get_width(), self.LastDisplayFrame.get_height()), pygame.SRCALPHA)
        ContentsSurface.set_alpha(self.Animation.Value)

        self.CurrentMode.Draw(ContentsSurface)

        DISPLAY.blit(ContentsSurface, (0, 0))

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
        self.Tools[0] = self.WindowList.Rectangle[0]
        self.Tools[1] = self.WindowList.Rectangle.bottom

        # WindowList Buttons
        self.Tools_WidgetController.Rectangle = self.Tools

        self.Tools_WidgetController.Update()

        if self.Tools_WidgetController.LastInteractionID == 0 and self.Tools_WidgetController.LastInteractionType:
            self.CloseSelectedProcess()

        if self.Tools_WidgetController.LastInteractionID == 1 and self.Tools_WidgetController.LastInteractionType:
            self.SwitchToSelectedProcess()

    def Draw(self, ContentsSurface):
        TitleText = "Opened Tasks"
        if not self.RootObj.Welcome:
            TitleText = "Welcome"
        TitleFontSize = 58
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

        self.WindowList.Render(ContentsSurface)

        # Render TaskbarTools Background
        Core.shape.Shape_Rectangle(ContentsSurface, (20, 20, 60), self.Tools)
        Core.shape.Shape_Rectangle(ContentsSurface, (94, 114, 219), (self.Tools[0] - 2, self.Tools[1] - 2, self.Tools[2] + 4, self.Tools[3] + 4), BorderWidth=2)

        # Render Close Button
        self.Tools_WidgetController.Draw(ContentsSurface)

        # Draw Bottom Text
        TitleText = "[DELETE] Finish selected task, [SPACEBAR] Switch to selected task, [F12] Open TaskBar Dashboard"
        TitleFontSize = 14
        TextY = 35
        TitleFont = "/Ubuntu.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, ContentsSurface.get_height() - self.DefaultContent.GetFont_height(TitleFont, TitleFontSize, TitleText) - TextY)

        # Draw Bottom Text
        TitleText = "TaskBar v" + UI.TaskBar_Version
        TextY = 15
        TitleFontSize = 12
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, ContentsSurface.get_height() - self.DefaultContent.GetFont_height(TitleFont, TitleFontSize, TitleText) - TextY)


        # Center Window list
        self.WindowList.Set_X(ContentsSurface.get_width() / 2 - self.WindowList.Rectangle[2] / 2)
        self.WindowList.Set_Y(ContentsSurface.get_height() / 2 - self.WindowList.Rectangle[3] / 2)


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

        for process in Core.MAIN.ProcessList:
            if process.PID == self.RootObj.RootProcess.PID:
                continue
            self.WindowList.AddItem(process.NAME, "PID: " + str(process.PID), ItemProperties=process.PID)

    def CloseSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            try:
                ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
                Core.MAIN.KillProcessByPID(ProcessPID)

                self.DefaultContent.PlaySound("/click.wav")

            except IndexError:
                self.WindowList.ResetSelectedItem()

    def SwitchToSelectedProcess(self):
        if self.WindowList.LastItemIndex is not None:
            try:
                ProcessPID = self.WindowList.ItemProperties[self.WindowList.LastItemIndex]
                Process = Core.MAIN.ProcessList[Core.MAIN.GetProcessIndexByPID(ProcessPID)]

                Core.wmm.WindowManagerSignal(Process, 0)

                self.RootObj.RootProcess.UI_Call_Request()

                self.DefaultContent.PlaySound("/click.wav")

            except IndexError:
                self.WindowList.ResetSelectedItem()

    def SwitchToDashboard(self):
        print("Placeholder")

    def Toggle(self):
        pass

class SystemFault_Instance:
    def __init__(self, pDefaultContent, pRootObj):
        self.DefaultContent = pDefaultContent
        self.RootObj = pRootObj

    def Update(self):
        self.RootObj.GoToModeWhenReturning = 0

    def Draw(self, ContentsSurface):
        # Draw the title
        TitleText = "The process {0} has failed.".format(Core.utils.ShortString(Core.MAIN.SystemFault_ProcessObject.NAME, 40))
        TitleFontSize = 22
        TitleFont = "/Ubuntu_Bold.ttf"
        self.DefaultContent.FontRender(ContentsSurface, TitleFont, TitleFontSize, TitleText, (240, 240, 240), ContentsSurface.get_width() / 2 - self.DefaultContent.GetFont_width(TitleFont, TitleFontSize, TitleText) / 2, 15)

        # Draw the SystemFault message
        TitleText = "Title : {0}\nPID : {1}\nExecPath : {2}\n\nDetails about the crash has been saved on logs folder\nlocated in: <root>/logs/.".format(Core.utils.ShortString(Core.MAIN.SystemFault_ProcessObject.TITLEBAR_TEXT, 35), str(Core.MAIN.SystemFault_ProcessObject.PID), Core.utils.ShortString(Core.MAIN.SystemFault_ProcessObject.ROOT_MODULE, 35))
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

