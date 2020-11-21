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
from System import Core
from System.SystemApps.TaiyouUI.MAIN import UI
from System.Core import Shape
import pygame

class Screen:
    def __init__(self, Root, DefaultContents):
        self.DefaultContents = DefaultContents
        self.Root = Root
        self.Root.ReadCachedHeaderInfos()

        self.ApplicationsList = UI.VerticalListWithDescription((5, 5, 200, self.Root.DISPLAY.get_height() - 10), self.DefaultContents)

        self.WidgetControler = UI.Widget.Widget_Controller(self.DefaultContents, (210, 5, self.Root.DISPLAY.get_width() - 215, self.Root.DISPLAY.get_height() - 10))

        self.WidgetControler.Append(UI.Widget.Widget_Label(self.DefaultContents, "/Ubuntu_Bold.ttf", self.DefaultContents.Get_RegKey("/strings/please_select_application"), 15, (230, 230, 230), 5, 20, 0))
        self.WidgetControler.Append(UI.Widget.Widget_PictureBox(self.DefaultContents, (self.WidgetControler.Rectangle[2] / 2 - 410 / 2, 5, 410, 160), "/default", 1))
        self.WidgetControler.Append(UI.Widget.Widget_Label(self.DefaultContents, "/Ubuntu.ttf", "null", 20, (250, 250, 250), 15, 170, 2))
        self.WidgetControler.Append(UI.Widget.Widget_Label(self.DefaultContents, "/Ubuntu.ttf", "null", 12, (250, 250, 250), 15, 200, 3))
        self.WidgetControler.Append(UI.Widget.Widget_Label(self.DefaultContents, "/Ubuntu.ttf", "null", 12, (250, 250, 250), 15, 220, 4))

        self.UpdateApplicationsList = False
        self.ApplicationSelectedMode = 0
        self.ApplicationSelectedDataDownloaded = False
        self.ApplicationSelectedDataDownloadStarted = False
        self.ApplicationSelectedData = None
        self.FirstUpdateToApplicationsList = False
        self.LastItemIndex = -1
        self.UpdateModes()

    def Render(self, DISPLAY):
        # Draw the bottom bar
        Shape.Shape_Rectangle(DISPLAY, UI.ThemesManager_GetProperty("WM_BorderInactiveColor"), self.WidgetControler.Rectangle)

        self.ApplicationsList.Render(DISPLAY)

        self.WidgetControler.Draw(DISPLAY)

    def Update(self):
        self.WidgetControler.ObjectOffset = (self.Root.POSITION[0], self.Root.POSITION[1] + 15)
        self.ApplicationsList.ColisionXOffset = self.Root.POSITION[0]
        self.ApplicationsList.ColisionYOffset = self.Root.POSITION[1]

        self.WidgetControler.Update()

        if self.Root.HeaderFilerRead:
            if not self.FirstUpdateToApplicationsList:
                self.FirstUpdateToApplicationsList = True
                self.UpdateApplicationsList = True

        if self.UpdateApplicationsList:
            self.UpdateApplicationsList = False
            print("Updating Installed Applications List...")
            self.ApplicationsList.ClearItems()
            for ApplicationEntry in self.Root.HeaderFileAppsEntry:
                self.ApplicationsList.AddItem(ApplicationEntry[2], ApplicationEntry[3], ItemProperties=ApplicationEntry)

        if self.ApplicationsList.LastItemIndex != None:
            if self.ApplicationsList.LastItemIndex != self.LastItemIndex:
                self.LastItemIndex = self.ApplicationsList.LastItemIndex
                self.ApplicationSelectedMode = 1
                self.ApplicationSelectedData = self.ApplicationsList.ItemProperties[self.LastItemIndex]
                print("Clicked at new item.")
                self.UpdateModes()

        if self.ApplicationSelectedMode == 1 and not self.ApplicationSelectedDataDownloaded and not self.ApplicationSelectedDataDownloadStarted:
            self.ApplicationSelectedDataDownloadStarted = True
            DownloadHeader = self.Root.ServerRootPath + "App/" + str(self.ApplicationSelectedData[0]) + "/header_data"
            DownloadBanner = self.Root.ServerRootPath + "App/" + str(self.ApplicationSelectedData[0]) + "/banner.png"

            self.Root.AddToDownloadQueue(DownloadHeader, "app_{0}/header".format(self.ApplicationSelectedData[0]), "app_{0}_header".format(self.ApplicationSelectedData[0]))
            self.Root.AddToDownloadQueue(DownloadBanner, "app_{0}/banner.png".format(self.ApplicationSelectedData[0]), "app_{0}_banner".format(self.ApplicationSelectedData[0]))

        if self.ApplicationSelectedMode == 1 and not self.ApplicationSelectedDataDownloaded and self.Root.IsDownloading is False and self.ApplicationSelectedDataDownloadStarted:
            print("Application Download has been completed!")
            self.ApplicationSelectedMode = 2
            self.UpdateModes()

    def UpdateModes(self):
        if self.ApplicationSelectedMode == 0:
            for widget in self.WidgetControler.WidgetCollection:
                widget.IsVisible = False

            self.WidgetControler.GetWidget(0).IsVisible = True

        elif self.ApplicationSelectedMode == 1:
            self.ApplicationSelectedDataDownloaded = False
            self.ApplicationSelectedDataDownloadStarted = False

            for widget in self.WidgetControler.WidgetCollection:
                widget.IsVisible = False

            self.WidgetControler.GetWidget(0).IsVisible = True
            self.WidgetControler.GetWidget(0).Text = self.DefaultContents.Get_RegKey("/strings/downloading_app_view")

        elif self.ApplicationSelectedMode == 2:
            self.ApplicationSelectedDataDownloaded = True
            self.ApplicationSelectedDataDownloadStarted = False
            for widget in self.WidgetControler.WidgetCollection:
                widget.IsVisible = False

            self.WidgetControler.GetWidget(1).IsVisible = True
            self.WidgetControler.GetWidget(2).IsVisible = True
            self.WidgetControler.GetWidget(3).IsVisible = True
            self.WidgetControler.GetWidget(4).IsVisible = True

            # Files path
            RootWaxPath = "{0}{1}{2}app_{3}{2}".format(Core.TaiyouPath_UserTempFolder, "sieved", Core.TaiyouPath_CorrectSlash, self.ApplicationSelectedData[0])
            BannerImagePath = RootWaxPath + "banner.png"
            HeaderPath = RootWaxPath + "header"

            print("Setting Banner Image...")
            self.WidgetControler.GetWidget(1).IsUnloadedImage = True
            self.WidgetControler.GetWidget(1).Image = pygame.image.load(BannerImagePath)

            # Set the App Name
            print("Setting App Name...")
            self.WidgetControler.GetWidget(2).Text = self.ApplicationSelectedData[2]
            ReadHeader = open(HeaderPath, "r").readlines()

            for line in ReadHeader:
                print("Reading application data header...")
                line = line.rstrip().lstrip().replace("%n", "\n")
                if line.startswith("#") or len(line) < 3:
                    print("Skipped uselless line.")
                    continue

                LineSplit = line.split(":")

                if LineSplit[0] == "Version":
                    print("Found Version Line.")
                    self.WidgetControler.GetWidget(3).Text = LineSplit[1]

                if LineSplit[0] == "FullDescription":
                    print("Found FullDescription Line.")
                    self.WidgetControler.GetWidget(4).Text = LineSplit[1]


    def EventUpdate(self, event):
        self.WidgetControler.EventUpdate(event)
        self.ApplicationsList.Update(event)