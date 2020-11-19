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
import pygame, os
from System import Core
#from System.Core import Utils
from System.Core import UTILS as Utils
from System.SystemApps.TaiyouUI.MAIN import UI
from System.Core import CntMng

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.INIT_ARGS = pInitArgs
        self.DISPLAY = pygame.Surface((400, 340))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = False
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), 15)
        self.TITLEBAR_TEXT = "Packpage Installer"
        self.WindowDragEnable = False
        self.WINDOW_OPACITY = 255
        self.ICON = None

    def Initialize(self):
        ## Initialize Content Manager
        self.ContentManager = CntMng.ContentManager()
        self.ContentManager.SetSourceFolder("PackpageInstaller/")
        self.ContentManager.SetFontPath("fonts/")
        self.ContentManager.SetImageFolder("img/")
        self.ContentManager.SetRegKeysPath("reg/")

        self.ContentManager.LoadImagesInFolder()
        self.ContentManager.LoadRegKeysInFolder()

        self.PackpageVerticalList = UI.VerticalListWithDescription(pygame.Rect(0, 0, self.DISPLAY.get_width(), self.DISPLAY.get_height() - 40), self.ContentManager)

        PackpagesList = Utils.Directory_FilesList(Core.TaiyouPath_UserPackpagesPath)

        for Packpage in PackpagesList:
            if Packpage.endswith(self.ContentManager.Get_RegKey("packpage_file_format")):
                Name = Packpage.rstrip().replace(Core.TaiyouPath_UserPackpagesPath, "").replace(self.ContentManager.Get_RegKey("packpage_file_format"), "")
                self.PackpageVerticalList.AddItem(Name, self.ContentManager.Get_RegKey("packpage_description"))

        self.PackpageInstalationEnabled = False
        self.PackpageInstalationStep = 0
        self.PackpageInstalationStepMax = 8
        self.PackpageInstalationStepNextDelay = 0
        self.PackpageReplaceWarning = False
        self.BackFromPackpageReplaceWarning = False
        self.IgnorePackpageReplace = False
        self.SelectedPackpage = ""
        self.ExtractPath = ""
        self.AppFolderPath = ""
        self.DataFolderPath = ""
        self.LastSelectedPackpage = ""
        self.DownToolbar = UI.Widget.Widget_Controller(self.ContentManager, pygame.Rect(0, self.DISPLAY.get_height() - 40, self.DISPLAY.get_width(), 40))

        self.DownToolbar.Append(UI.Widget.Widget_Label(self.ContentManager, "/Ubuntu_Bold.ttf", self.ContentManager.Get_RegKey("/strings/select_app_list"), 12, (255, 255, 255), 2, 2, 0))
        self.DownToolbar.Append(UI.Widget.Widget_Button(self.ContentManager, self.ContentManager.Get_RegKey("/strings/install_button"), 14, 4, 20, 1))
        self.DownToolbar.Append(UI.Widget.Widget_ProgressBar(self.ContentManager, 0, self.PackpageInstalationStepMax, (5, 25, 200, 15), 2))
        self.DownToolbar.Append(UI.Widget.Widget_Button(self.ContentManager, self.ContentManager.Get_RegKey("/strings/no_button"), 14, 34, 20, 3))
        self.DownToolbar.Append(UI.Widget.Widget_Button(self.ContentManager, self.ContentManager.Get_RegKey("/strings/yes_button"), 14, 4, 20, 4))

        self.DownToolbar.GetWidget(2).IsVisible = False
        self.DownToolbar.GetWidget(3).IsVisible = False
        self.DownToolbar.GetWidget(4).IsVisible = False

        self.POSITION = (Core.MAIN.ScreenWidth / 2 - self.DISPLAY.get_width() / 2, Core.MAIN.ScreenHeight / 2 - self.DISPLAY.get_height() / 2)
        self.ICON = self.ContentManager.GetImage("/app_icon.png")

    def Draw(self):
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.DISPLAY.fill((25, 30, 58))

        self.ContentManager.ImageRender(self.DISPLAY, "/app_icon.png", self.DISPLAY.get_width() / 2 - 128, self.DISPLAY.get_height() / 2 - 128, Opacity=100)

        self.PackpageVerticalList.Render(self.DISPLAY)
        self.DownToolbar.Draw(self.DISPLAY)

        return self.DISPLAY

    def Update(self):
        if not self.APPLICATION_HAS_FOCUS:
            return

        if self.PackpageInstalationEnabled:
            self.PackpageInstalationStepNextDelay += 1

            if self.PackpageReplaceWarning:
                self.SetStatusText(self.ContentManager.Get_RegKey("/strings/application_already_installed_warning"))
                ## Set progress bar Invisible
                self.DownToolbar.GetWidget(2).IsVisible = False

                ## Set Yes Button Visible
                self.DownToolbar.GetWidget(4).IsVisible = True

                ## Set No Button Visible
                self.DownToolbar.GetWidget(3).IsVisible = True

            if self.PackpageInstalationStepNextDelay >= 25 and not self.PackpageReplaceWarning:
                self.PackpageInstalationStepNextDelay = 0
                if not self.BackFromPackpageReplaceWarning:
                    self.PackpageInstalationStep += 1
                else:
                    self.BackFromPackpageReplaceWarning = False

                self.ApplicationInstallingUpdateProgress()

            # Set the Progress Bar Value and Status Text
            if self.PackpageInstalationEnabled and not self.PackpageReplaceWarning:
                self.SetStatusText(self.ContentManager.Get_RegKey("/strings/progress_text").format(self.SelectedPackpage, str(self.PackpageInstalationStep), str(self.PackpageInstalationStepMax)))
                self.DownToolbar.GetWidget(2).Progress = self.PackpageInstalationStep

                if self.PackpageInstalationStep >= self.PackpageInstalationStepMax + 1:
                    print("Instalation steps has been reached its limit")
                    self.PackpageInstalationStep = self.PackpageInstalationStepMax
                    self.FinishInstalation(False)

        else:
            self.PackpageVerticalList.ColisionXOffset = self.POSITION[0]
            self.PackpageVerticalList.ColisionYOffset = self.POSITION[1] + self.TITLEBAR_RECTANGLE[3]

            if self.PackpageVerticalList.LastItemClicked != "null":
                self.SetSelectedPackpage(self.PackpageVerticalList.LastItemClicked)

        self.DownToolbar.ObjectOffset = (self.POSITION[0], self.POSITION[1] + self.TITLEBAR_RECTANGLE[3])
        self.DownToolbar.Update()

        if self.DownToolbar.LastInteractionID == 1 and self.DownToolbar.LastInteractionType is True:
            if not self.PackpageInstalationEnabled:
                if self.SelectedPackpage != "":
                    self.DownToolbar.GetWidget(1).IsVisible = False
                    self.DownToolbar.GetWidget(2).IsVisible = True
                    self.PackpageInstalationEnabled = True
                else:
                    self.ContentManager.Get_RegKey("/strings/select_app_list")

        ## Yes Button when Replace Warning
        if self.DownToolbar.LastInteractionID == 4 and self.DownToolbar.LastInteractionType is True and self.PackpageInstalationEnabled and self.PackpageReplaceWarning:
            self.PackpageReplaceWarning = False
            ## Set progress bar Visible
            self.DownToolbar.GetWidget(2).IsVisible = True

            ## Set Yes Button Invisible
            self.DownToolbar.GetWidget(4).IsVisible = False

            ## Set No Button Invisible
            self.DownToolbar.GetWidget(3).IsVisible = False

            ## Set Back from Replace Warning
            self.BackFromPackpageReplaceWarning = True

            ## Set IgnorePackpageReplace
            self.IgnorePackpageReplace = True

        ## No Button when Replace Warning
        if self.DownToolbar.LastInteractionID == 3 and self.DownToolbar.LastInteractionType is True and self.PackpageInstalationEnabled and self.PackpageReplaceWarning:
            self.FinishInstalation(True)
            self.SetStatusText(self.ContentManager.Get_RegKey("/strings/packpage_instalation_aborted"))

    def ApplicationInstallingUpdateProgress(self):
        print("Instalation Progress Update\nStep: {0}".format(str(self.PackpageInstalationStep)))
        PackpagePath = Core.TaiyouPath_UserPackpagesPath + self.SelectedPackpage + self.ContentManager.Get_RegKey("/packpage_file_format")

        ## Check if File exists
        if self.PackpageInstalationStep == 1:
            if self.SelectedPackpage == "" or not Utils.File_Exists(PackpagePath):
                self.FinishInstalation()

        elif self.PackpageInstalationStep == 2:  ## Check if Extract Path exists and clean it
            print("Packpage : {0}".format(self.SelectedPackpage))
            self.ExtractPath = Core.TaiyouPath_UserTempFolder + self.SelectedPackpage
            print("ExtractPath : " + self.ExtractPath)

            # Check if Extract Path Exists
            if Utils.Directory_Exists(self.ExtractPath):
                print("Extraction Path Exists, Directory Removed and Re-Created")
                Utils.Directory_Remove(self.ExtractPath)
                Utils.Directory_MakeDir(self.ExtractPath)

        elif self.PackpageInstalationStep == 3:  ## Extract the Packpage
            # Extract the Zip File
            print("Un-Zipping packpage....")
            Utils.Unzip_File(PackpagePath, self.ExtractPath)

        elif self.PackpageInstalationStep == 4:  ## Check if Packpage is Valid
            print("Check for app and data folder on extracted path")
            self.AppFolderPath = self.ExtractPath + Core.TaiyouPath_CorrectSlash + "app" + Core.TaiyouPath_CorrectSlash
            self.DataFolderPath = self.ExtractPath + Core.TaiyouPath_CorrectSlash + "data" + Core.TaiyouPath_CorrectSlash
            AppFolderExists = Utils.Directory_Exists(self.AppFolderPath)
            DataFolderExists = Utils.Directory_Exists(self.DataFolderPath)

            if not AppFolderExists or not DataFolderExists:
                self.FinishInstalation(True)
                self.SetStatusText(self.ContentManager.Get_RegKey("/strings/invalid_taiyou_packpage"))

        elif self.PackpageInstalationStep == 5:  ## Check if Application Already Exists
            AppFolderInsideIt = os.listdir(self.AppFolderPath)[0]
            CheckPath = Core.TaiyouPath_ApplicationsFolder + AppFolderInsideIt
            if Utils.Directory_Exists(CheckPath) and not self.IgnorePackpageReplace:
                self.PackpageReplaceWarning = True
                return

            print("Copy Application to Application Folder...")
            Utils.Directory_Copy(self.AppFolderPath[:-1], Core.TaiyouPath_ApplicationsFolder[:-1])

        elif self.PackpageInstalationStep == 6:  ## Copy the Application Folder
            print("Copy Application to Application Folder...")
            Utils.Directory_Copy(self.AppFolderPath, Core.TaiyouPath_ApplicationsFolder[:-1])

        elif self.PackpageInstalationStep == 7:
            print("Copy Application Data to Application Data Folder...")
            Utils.Directory_Copy(self.DataFolderPath, Core.TaiyouPath_ApplicationsDataFolder)

        elif self.PackpageInstalationStep == 8:
            self.FinishInstalation(True)

    def SetStatusText(self, text):
        self.DownToolbar.GetWidget(0).Text = text

    def FinishInstalation(self, DeleteExtractPath=False):
        print("Instalation has been completed.")
        self.PackpageInstalationEnabled = False
        self.PackpageInstalationStepNextDelay = 0
        self.IgnorePackpageReplace = False
        self.PackpageReplaceWarning = False
        self.BackFromPackpageReplaceWarning = False

        if DeleteExtractPath:
            Utils.Directory_Remove(self.ExtractPath)

        if self.PackpageInstalationStep >= self.PackpageInstalationStepMax:
            self.SetStatusText(self.ContentManager.Get_RegKey("/strings/packpage_install_complete").format(self.SelectedPackpage))

        else:
            self.SetStatusText(self.ContentManager.Get_RegKey("/strings/packpage_install_error").format(self.SelectedPackpage))

        self.PackpageInstalationStep = 0

        # Re-Enable the Install Button
        self.DownToolbar.GetWidget(1).IsVisible = True
        self.DownToolbar.GetWidget(2).IsVisible = False
        self.DownToolbar.GetWidget(3).IsVisible = False
        self.DownToolbar.GetWidget(4).IsVisible = False
        self.SelectedPackpage = ""

    def SetSelectedPackpage(self, pkg_path):
        self.SelectedPackpage = pkg_path.rstrip().replace(Core.TaiyouPath_UserPackpagesPath, "").replace(".zip", "")

        if self.LastSelectedPackpage != self.SelectedPackpage:
            self.LastSelectedPackpage = self.SelectedPackpage
            self.SetStatusText("Selected {0}.".format(self.SelectedPackpage))

        self.PackpageVerticalList.ResetSelectedItem()

    def EventUpdate(self, event):
        if not self.PackpageInstalationEnabled:
            self.PackpageVerticalList.Update(event)

        self.DownToolbar.EventUpdate(event)