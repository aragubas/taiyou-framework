#!/usr/bin/python3.8
#   Copyright 2021 Aragubas
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
import pygame
import System.Core as Core
from Library import UI
from Library.UI import Widget
from Library import CoreAccess

class Process(Core.Process):
    def Initialize(self):
        self.DefaultContent = Core.CntMng.ContentManager()

        self.DefaultContent = UI.SystemResources
        self.IntroSoundPlayed = False

        self.SetVideoMode(False, (350, 320))
        self.CenterWindow()

        self.SetTitle("Task Manager")
        self.ICON = UI.SystemResources.GetImage("/task_manager.png")

        self.TaskList = UI.VerticalListWithDescription((0, 25, 350, 320 - 25), self.DefaultContent)
        self.SelectedTask = ""
        self.SelectedTaskPID = -1
        self.FirstCycleRefresh = False

        self.TopOptionsBar = Widget.Widget_Controller(self.DefaultContent, (0, 0, 350, 25))
        self.TopOptionsBar.BackgroundColor = UI.ThemesManager_GetProperty("WidgetControllerBackground1")
        self.TopOptionsBar.Append(Widget.Widget_Button(self.DefaultContent, "Reload", 12, 5, 5, 0))
        self.TopOptionsBar.Append(Widget.Widget_Button(self.DefaultContent, "End Task", 12, 50, 5, 1))
        self.TopOptionsBar.Append(Widget.Widget_Label(self.DefaultContent, "/Ubuntu_Bold.ttf", "No process selected", 12, (230, 230, 230), 105, 5, 2))

        self.ProcessNameLabel = self.TopOptionsBar.GetWidget(2)

    def EventUpdate(self, event):
        self.TaskList.Update(event)
        self.TopOptionsBar.EventUpdate(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
            self.UpdateProcessList()

    def UpdateProcessList(self):
        # Update WindowList Contents
        self.TaskList.ClearItems()

        for process in CoreAccess.ProcessAccess:
            # Skip non-graphical processes
            ProcessHasIcon = False
            ProcessIcon = None

            if process.IS_GRAPHICAL:
                try:
                    if process.ICON is not None:
                        ProcessHasIcon = True
                        ProcessIcon = process.ICON

                except AttributeError:
                    ProcessHasIcon = False
                    ProcessIcon = None

            ItemDescription = "PID: " + str(process.PID)

            if not process.IS_GRAPHICAL:
                ItemDescription += " Non-Graphical"

            if process.FRAMELESS:
                ItemDescription += " Frameless"

            self.TaskList.AddItem(process.TITLEBAR_TEXT, ItemDescription, ItemProperties=process.PID, ItemSprite=ProcessIcon, ItemSpriteIsUnloaded=ProcessHasIcon)

    def Update(self):
        self.TaskList.UpdateOffsetToWindow(self)

        self.TopOptionsBar.Update()
        self.TopOptionsBar.UpdateOffsetToWindow(self)

        if self.TopOptionsBar.LastInteractionID == 0:
            self.UpdateProcessList()

        if self.TopOptionsBar.LastInteractionID == 1:
            if self.SelectedTaskPID != -1:
                CoreAccess.SendSigKillToProcessByPID(self.SelectedTaskPID)

            self.SelectedTaskPID = -1
            self.SelectedTask = ""
            self.TaskList.ResetSelectedItem()
            self.UpdateProcessList()

        self.UpdateSelectedTaskTitle()

        if self.TaskList.LastItemIndex is not None:
            self.SelectedTask = self.TaskList.LastItemClicked
            self.SelectedTaskPID = self.TaskList.ItemProperties[self.TaskList.LastItemIndex]

        if not self.FirstCycleRefresh:
            self.FirstCycleRefresh = True
            self.UpdateProcessList()

    def UpdateSelectedTaskTitle(self):
        if self.SelectedTask == "":
            self.ProcessNameLabel.Text = "No selected process"
        else:
            self.ProcessNameLabel.Text = self.SelectedTask

    def Draw(self):
        self.DISPLAY.fill(UI.ThemesManager_GetProperty("DefaultBackground"))

        self.TaskList.Render(self.DISPLAY)

        self.TopOptionsBar.Draw(self.DISPLAY)

        self.LAST_SURFACE = self.DISPLAY.copy()