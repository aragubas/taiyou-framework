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
from OneTrack.MAIN import UI
from Core import Utils

class Screen:
    def __init__(self, pRoot_Process):
        self.RootProcess = pRoot_Process

        # Set the correct screen size
        self.RootProcess.DISPLAY = pygame.Surface((300, 350))

        self.FolderList = UI.VerticalListWithDescription(pygame.Rect(0, 24, 300, 15))
        ButtonsList = list()
        ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "Select", 14))
        ButtonsList.append(UI.Button((0, 0, 0, 0), "New", 14))

        self.OptionsBar = UI.ButtonsBar((0, 0, 0, 0), ButtonsList)
        self.RootProcess.TITLEBAR_TEXT = "Save File"
        self.Inputbox_FileName = UI.InputBox(5, 25, 250, 25, "Default", 14)

        self.FileListUpdated = False
        self.FileListUpdate = False
        self.EnterFileNameEnabled = False

    def Draw(self, DISPLAY):
        # -- Render the Folder List -- #
        self.FolderList.Render(DISPLAY)

        # -- Render the Buttons List -- #
        self.OptionsBar.Render(DISPLAY)

        if self.EnterFileNameEnabled:
            self.Inputbox_FileName.Render(DISPLAY)

    def Update(self):
        if not self.FileListUpdate:
            self.FileListUpdate = True
            self.UpdateFileList()

        #-------------------------------
        self.FolderList.Set_W(self.RootProcess.DISPLAY.get_width())
        self.FolderList.Set_H(self.RootProcess.DISPLAY.get_height() - 35)
        self.FolderList.ColisionXOffset = self.RootProcess.POSITION[0] + self.FolderList.Rectangle[0]
        self.FolderList.ColisionYOffset = self.RootProcess.POSITION[1] + 15 + self.FolderList.Rectangle[1]
        #-------------------------------
        self.OptionsBar.ColisionXOffset = self.RootProcess.POSITION[0]
        self.OptionsBar.ColisionYOffset = self.RootProcess.POSITION[1] + 15
        #--------------------------------
        self.Inputbox_FileName.ColisionOffsetX = self.RootProcess.POSITION[0]
        self.Inputbox_FileName.ColisionOffsetY = self.RootProcess.POSITION[1] + 15

        self.OptionsBar.Update()

        if not self.EnterFileNameEnabled:
            SelectedFile = self.FolderList.LastItemClicked

            if self.OptionsBar.ClickedButtonIndex == 0:
                self.OptionsBar.ClickedButtonIndex = -1

                if not SelectedFile == "null":
                    self.RootProcess.RootProcess.CurrentScreenToUpdate.SaveMusicData(Core.GetAppDataFromAppName("OneTrack") + Core.TaiyouPath_CorrectSlash + SelectedFile)
                    print("Music Data has been saved. on\n{0}".format(SelectedFile))
                    Core.wmm.WindowManagerSignal(self.RootProcess, 1)

            if self.OptionsBar.ClickedButtonIndex == 1:
                self.EnterFileNameEnabled = True

        else:
            if self.OptionsBar.ClickedButtonIndex == 1:

                # -- Write the File -- #
                if not self.Inputbox_FileName.text == "":
                    self.Inputbox_FileName.text = self.Inputbox_FileName.text.replace(" ", "_")
                    self.RootProcess.RootProcess.CurrentScreenToUpdate.SaveMusicData(Core.GetAppDataFromAppName("OneTrack") + Core.TaiyouPath_CorrectSlash + self.Inputbox_FileName.text)

                    print("Music Data has been created. on\n{0}".format(self.Inputbox_FileName.text))
                    Core.wmm.WindowManagerSignal(self.RootProcess, 1)

    def EventUpdate(self, event):
        self.OptionsBar.EventUpdate(event)

        if not self.EnterFileNameEnabled:
            self.FolderList.Update(event)
        else:
            self.Inputbox_FileName.Update(event)

    def UpdateFileList(self):
        print("Save : Updating File List...")
        self.FolderList.ClearItems()
        AllFilesInDir = Utils.Directory_FilesList(Core.GetAppDataFromAppName("OneTrack"))

        for file in AllFilesInDir:
            # Check if file is a valid OneTrack Project
            if file.endswith(".oneprj"):
                FileAllPath = file
                FileName = file.replace(Core.GetAppDataFromAppName("OneTrack"), "").replace(".oneprj", "")

                ItemName = FileName[1:]
                ItemDescription = "Saved on: {0}".format(FileAllPath)

                self.FolderList.AddItem(ItemName, ItemDescription)
