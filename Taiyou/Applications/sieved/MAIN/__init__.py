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
import pygame, threading
from System import Core
from System.Core import Utils
from System.Core import CntMng
from System.Core import Shape
from System.SystemApps.TaiyouUI.MAIN import UI
from Applications.sieved.MAIN import LoadingScreen
from Applications.sieved.MAIN import MainScreen

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs, pProcessIndex):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((650, 420))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = False
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "Sieved Store"
        self.WindowDragEnable = False
        self.DefaultContents = CntMng.ContentManager()
        self.ICON = None
        self.ProcessIndex = pProcessIndex
        self.WINDOW_DRAG_ENABLED = False
        self.Running = True
        self.Timer = pygame.time.Clock()

        Core.RegisterToCoreAccess(self)

        self.Initialize()

        # Initialize Drawing Thread
        self.InterruptDrawing = False
        self.TerminateDrawing = False
        self.DrawThread = threading.Thread(target=self.Draw).start()

    def Initialize(self):
        self.POSITION = (Core.MAIN.ScreenWidth / 2 - self.DISPLAY.get_width() / 2, Core.MAIN.ScreenHeight / 2 - self.DISPLAY.get_height() / 2)

        self.DefaultContents.SetSourceFolder("Sieved/")
        self.DefaultContents.SetFontPath("fonts/")
        self.DefaultContents.SetRegKeysPath("reg/")
        self.DefaultContents.SetImageFolder("img/")

        self.DefaultContents.LoadRegKeysInFolder()
        self.DefaultContents.LoadImagesInFolder()

        self.IsDownloading = False
        self.IsDownloadingDisableTrigger = False
        self.DownloadingBarAnimator = Utils.AnimationController(0.5, multiplierRestart=True)
        self.RequiredFilesDownloaded = False
        self.IsDownloadingWidgetController = UI.Widget.Widget_Controller(self.DefaultContents, (0, 0, self.DISPLAY.get_width(), 35))

        # Add the widgets
        self.IsDownloadingWidgetController.Append(UI.Widget.Widget_Label(self.DefaultContents, "/Ubuntu_Bold.ttf", "Downloading...", 14, (230, 230, 230), 5, 2, 0))
        self.IsDownloadingWidgetController.Append(UI.Widget.Widget_ProgressBar(self.DefaultContents, 0, 100, (5, 20, 200, 12), 1))

        self.DownloadObj = Utils.Downloader()

        self.DownloadQueue = list()

        self.ServerRootPath = "http://dpaulootavio5.000webhostapp.com/Taiyou/"
        self.LastFinishedDownload = ""
        self.CurrentlyDownloadingFile = ""

        # Data
        self.HeaderFileData = ""
        self.BanksFileData = ""
        self.NewsFileData = ""

        self.HeaderFilePropertiesData = list()
        self.HeaderFileAppsEntry = list()

        self.HeaderFilerRead = False

        self.SelectedScreen = None
        self.SetScreenByID(0)

        # Download newest header file
        self.AddToDownloadQueue(self.ServerRootPath + "header", "header", "header_file")
        self.AddToDownloadQueue(self.ServerRootPath + "news", "news", "news_file")

    def HeadFile_GetProperty(self, PropertyName):
        for propData in self.HeaderFilePropertiesData:
            if propData[0] == PropertyName:
                return propData[1]

    def InterpretHeadFile(self):
        self.HeaderFilePropertiesData.clear()
        self.HeaderFileAppsEntry.clear()

        print("Interpreting Head File...")
        for line in self.HeaderFileData.splitlines():
            line = line.rstrip().lstrip()

            if line.startswith("!") or len(line) < 3:
                print("Skipped invalid line")
                continue

            if line.startswith("$"):
                LineSplit = line.replace("$", "").split(":")
                print("Found Property ({0}) with Value ({1})".format(LineSplit[0], LineSplit[1]))

                self.HeaderFilePropertiesData.append(LineSplit)

            if line.startswith("#"):
                print("Found command line.")

                LineSplit = line.replace("#", "").split(";")

                if LineSplit[0] == "APP_ENTRY":
                    AppDescription = LineSplit[4]
                    AppFormalName = LineSplit[3]
                    AppID = LineSplit[2]
                    AppIdentifier = LineSplit[1]
                    print("Command line is an App Entry.")
                    print("AppID {0}\nAppIdentifier {1}\nAppFormalName {2}\nAppDescription {3}".format(AppID, AppIdentifier, AppFormalName, AppDescription))

                    self.HeaderFileAppsEntry.append((AppID, AppIdentifier, AppFormalName, AppDescription))
                    print("AppEntry added to to list of Avaliable Applications.")

        self.HeaderFilerRead = True

    def SetScreenByID(self, ScreenID):
        if ScreenID == 0:
            self.SelectedScreen = LoadingScreen.Screen(self, self.DefaultContents)

        if ScreenID == 1:
            self.SelectedScreen = MainScreen.Screen(self, self.DefaultContents)

    def AddToDownloadQueue(self, url, file_path, tag):
        self.IsDownloading = True
        self.IsDownloadingDisableTrigger = False
        self.DownloadingBarAnimator.Enabled = True
        self.DownloadingBarAnimator.CurrentMode = True

        DownloadPath = "{0}{1}{2}{3}".format(Core.TaiyouPath_UserTempFolder, "sieved", Core.TaiyouPath_CorrectSlash, file_path)

        self.DownloadQueue.append((url, DownloadPath, tag))

    def Update(self):
        while self.Running:
            self.Timer.tick(100)

            if not self.APPLICATION_HAS_FOCUS:
                return

            if self.IsDownloading:
                self.UpdateDownloaderStatusBar()

                self.UpdateDownloadQueue()

            if not self.RequiredFilesDownloaded:
                if self.LastFinishedDownload == "news_file":
                    self.ReadCachedHeaderInfos()

            self.SelectedScreen.Update()

    def ReadCachedHeaderInfos(self):
        self.RequiredFilesDownloaded = True
        print("Reading Header Files...")
        DownloadPath = "{0}{1}".format(Core.TaiyouPath_UserTempFolder, "sieved")
        HeaderFilePath = "{0}{1}{2}".format(DownloadPath, Core.TaiyouPath_CorrectSlash, "header")
        NewsFilePath = "{0}{1}{2}".format(DownloadPath, Core.TaiyouPath_CorrectSlash, "news")

        self.HeaderFileData = open(HeaderFilePath).read()
        self.NewsFileData = open(NewsFilePath).read()
        print("Header Files read has been completed.")
        self.InterpretHeadFile()

    def UpdateDownloadQueue(self):
        self.DownloadingBarAnimator.Update()

        if self.IsDownloadingDisableTrigger:
            if self.DownloadingBarAnimator.Enabled is False and self.DownloadingBarAnimator.Value == self.DownloadingBarAnimator.MinValue:
                self.IsDownloadingDisableTrigger = False
                self.IsDownloading = False
                print("IsDownloading has been finished.")

            return

        if self.DownloadObj.DownloadState == "INACTIVE":
            if len(self.DownloadQueue) != 0:
                ItemSelected = self.DownloadQueue[0]
                SelectedItemUrl = ItemSelected[0]
                SelectedItemFilePath = ItemSelected[1]
                ItemTag = ItemSelected[2]

                self.DownloadObj.StartDownload(SelectedItemUrl, SelectedItemFilePath)
                print("Started download for:\nURL ({0})\nPath ({1})".format(SelectedItemUrl, SelectedItemFilePath))
                self.IsDownloadingWidgetController.GetWidget(0).Text = self.DefaultContents.Get_RegKey("/strings/download_started").format(len(self.DownloadQueue))

                self.CurrentlyDownloadingFile = ItemTag

            else:
                print("Download queue has been finished.")
                self.IsDownloadingWidgetController.GetWidget(0).Text = self.DefaultContents.Get_RegKey("/strings/download_queue_finished")

                self.IsDownloadingDisableTrigger = True
                self.DownloadingBarAnimator.Enabled = True

        self.IsDownloadingWidgetController.GetWidget(1).Progress = int(self.DownloadObj.DownloadMetaData[0])

        if self.DownloadObj.DownloadState == "DOWNLOADING":
            self.IsDownloadingWidgetController.GetWidget(0).Text = self.DefaultContents.Get_RegKey("/strings/downloading_text").format(len(self.DownloadQueue))

        if self.DownloadObj.DownloadState == "FINISHED":
            self.IsDownloadingWidgetController.GetWidget(0).Text = self.DefaultContents.Get_RegKey("/strings/downloading_completed").format(len(self.DownloadQueue))
            self.DownloadObj.SetInactiveState()
            self.LastFinishedDownload = self.CurrentlyDownloadingFile
            print("Finished download of: {0}.".format(self.LastFinishedDownload))
            self.DownloadQueue.pop(0)

    def Draw(self):
        Clock = pygame.time.Clock()

        while not self.TerminateDrawing:
            if self.InterruptDrawing:
                continue

            Clock.tick(60)

            self.DISPLAY.fill(UI.ThemesManager_GetProperty("WM_BorderInactiveColor"))

            self.SelectedScreen.Render(self.DISPLAY)

            # Downloading Overlay
            if self.IsDownloading:
                self.DrawDownloaderStatusBar()

            self.LAST_SURFACE = self.DISPLAY.copy()

    def UpdateDownloaderStatusBar(self):
        self.IsDownloadingWidgetController.Update()

    def DrawDownloaderStatusBar(self):
        DownloadingBarSurface = pygame.Surface((self.DISPLAY.get_width(), 35), pygame.SRCALPHA)
        DownloadingBarSurface.set_alpha(self.DownloadingBarAnimator.Value - 10)

        Shape.Shape_Rectangle(DownloadingBarSurface, UI.ThemesManager_GetProperty("WM_TitlebarActiveColor"), (0, 0, DownloadingBarSurface.get_width(), DownloadingBarSurface.get_height()))

        self.IsDownloadingWidgetController.Draw(DownloadingBarSurface)

        self.DISPLAY.blit(DownloadingBarSurface, (0, self.DownloadingBarAnimator.Value - 255))

    def EventUpdate(self, event):
        if self.IsDownloading:
            self.IsDownloadingWidgetController.EventUpdate(event)

        self.SelectedScreen.EventUpdate(event)
