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
import pygame, os, pickle, io
import Core
from Core import CntMng
from Core import MAIN
from Core import AppData
from Core import Shape
import Core as tge
from OneTrack.MAIN import UI
from OneTrack.MAIN import SaveFileDialog
from OneTrack.MAIN import OpenFileDialog
from OneTrack.MAIN.Screens.Editor import OptionsBar
from OneTrack.MAIN.Screens.Editor import EditorBar
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from OneTrack.MAIN.Screens.Editor import SoundCacheMessage
import OneTrack.MAIN as Main

track_list = UI.TrackList

# -- Top Toolbar -- #
TopBarControls = UI.ButtonsBar
DropDownFileMenu = UI.DropDownMenu
LastScreenFrame = None

def Initialize():
    global track_list
    global TopBarControls
    global DropDownFileMenu

    # Add all widgets
    ButtonsList = list()
    ButtonsList.append(UI.Button(pygame.Rect(0, 0, 0, 0), "File", 14))
    TopBarControls = UI.ButtonsBar((3, 5, Core.MAIN.ScreenWidth, 32), ButtonsList)
    DropDownFileMenuList = (("Load", DropDownButtonsActions_LoadButton), ("Save", DropDownButtonsActions_SaveButton), ("New File", DropDownButtonsActions_NewFileButton), ("About", DropDownButtonsActions_AboutButton), ("Settings", DropDownButtonsActions_SettingsButton))
    DropDownFileMenu = UI.DropDownMenu(pygame.Rect(10, 35, 120, 65), DropDownFileMenuList)

    OptionsBar.Initialize()
    EditorBar.Initialize()
    SoundCacheMessage.Initialize()

    NewMusicFile()

def GameDraw(DISPLAY):
    global track_list
    global TopBarControls
    global DropDownFileMenu
    global LastScreenFrame

    if not var.DisableControls:
        if not var.FileMenuEnabled:
            DISPLAY.fill((UI.ThemesManager_GetProperty("BackgroundColor")))

            track_list.Render(DISPLAY)
            TopBarControls.Render(DISPLAY)

            OptionsBar.Draw(DISPLAY)
            EditorBar.Draw(DISPLAY)

            SoundCacheMessage.Draw(DISPLAY)

            LastScreenFrame = DISPLAY.copy()

        else:
            DISPLAY.blit(LastScreenFrame, (0, 0))

            TopBarControls.Render(DISPLAY)

            DropDownFileMenu.Render(DISPLAY)


def SaveMusicData(FilePath):
    global track_list

    FilePath = FilePath + ".oneprj"

    ProjectDataFile = ""

    ProjectDataFile += "#region,METADATA\n" + \
                       "BPM:" + str(var.BPM) + "\n" + \
                       "Rows:" + str(var.Rows) + "\n" +  \
                       "Highlight:" + str(var.Highlight) + "\n" +  \
                       "HighlightSecond:" + str(var.HighlightSecond) + "\n" +  \
                       "Patterns:" + str(var.Patterns) + "\n" +  \
                       "SavedVersion:" + str(var.ProcessReference.DefaultContents.Get_RegKey("/version")) + "\n" +  \
                       "$end\n"

    for pattern in track_list.PatternList:
        ProjectDataFile += "#region,Pattern:" + str(pattern.PatternID) + "\n"

        for rows in pattern.Tracks:
            ProjectDataFile += "%Row:" + str(rows.ID) + "\n"

            for block in rows.Tracks:
                BlockData = "{0}:{1}".format(block.TrackData[0], block.TrackData[1])

                ProjectDataFile += BlockData + "\n"

            ProjectDataFile += "%row_end\n"

        ProjectDataFile += "$end\n"

    AppData.WriteAppData(FilePath, ProjectDataFile)

def LoadMusicData(FileName):
    global track_list

    FileName = FileName + ".oneprj"
    print("Loading Music {0}...".format(FileName))

    # -- Unload the Current SoundCahce -- #
    UI.ContentManager.UnloadSoundTuneCache()

    # -- Clear the Current Patterns -- #
    track_list.PatternList.clear()

    FileDataRead = open(FileName, "r").readlines()

    FileImportedFromOlderVersion = False
    IsReadingRegion = False
    IsReadingMetadata = False
    LastReadingRegion_Name = ""

    MusicData_BPM = 0
    MusicData_Rows = 0
    MusicData_Highlight = 0
    MusicData_HighlightSecound = 0
    MusicData_Patterns = 0
    MusicData_VersionSaved = ""

    RowReading_LastRowID = 0
    RowReading_IsReadingRow = False
    RowReading_BlocksList = list()

    ReadPatternsList = list()

    for line in FileDataRead:
        line = line.rstrip()
        if not IsReadingRegion:
            if line.startswith("#region"):
                IsReadingRegion = True
                SplitRegionRead = line.replace("#region", "").split(",")
                LastReadingRegion_Name = SplitRegionRead[1]

                # Check what type of data is being read
                IsReadingMetadata = LastReadingRegion_Name == "METADATA"

                # Create the Pattern
                if not IsReadingMetadata:
                    ObjToAdd = UI.Pattern(int(LastReadingRegion_Name.split(":")[1]), False)
                    ReadPatternsList.append(ObjToAdd)

                    print("CreatedPattern_ID : " + str(LastReadingRegion_Name.split(":")[1]))

            continue

        # Check if reading hit it's end
        if line == "$end":
            print("Finished reading region ({0})".format(LastReadingRegion_Name))
            IsReadingRegion = False
            if not IsReadingMetadata:
                ReadPatternsList[int(LastReadingRegion_Name.split(":")[1])].UpdateTracksPosition()

                LastReadingRegion_Name = ""
            IsReadingMetadata = False
            continue

        # Read Metadata
        if IsReadingMetadata:
            ArgsSplit = line.split(":")

            if ArgsSplit[0] == "BPM":
                MusicData_BPM = int(ArgsSplit[1])
                print("BPM was set to: {0}".format(str(MusicData_BPM)))
                continue

            if ArgsSplit[0] == "Rows":
                MusicData_Rows = int(ArgsSplit[1])
                print("Rows was set to: {0}".format(str(MusicData_Rows)))
                continue

            if ArgsSplit[0] == "Highlight":
                MusicData_Highlight = int(ArgsSplit[1])
                print("Highlight was set to: {0}".format(str(MusicData_Highlight)))
                continue

            if ArgsSplit[0] == "HighlightSecond":
                MusicData_HighlightSecound = int(ArgsSplit[1])
                print("HighlightSecond was set to: {0}".format(str(MusicData_HighlightSecound)))
                continue

            if ArgsSplit[0] == "Patterns":
                MusicData_Patterns = int(ArgsSplit[1])
                print("Patterns was set to: {0}".format(str(MusicData_Patterns)))
                continue

            if ArgsSplit[0] == "SavedVersion":
                MusicData_VersionSaved = ArgsSplit[1]
                print("VersionSaved was set to: {0}".format(MusicData_VersionSaved))
                continue

            print("Invalid Metadata Argument ({0})".format(ArgsSplit[0]))
            continue

        # Start Row Reading
        if line.startswith("%Row") and not RowReading_IsReadingRow:
            LineSplit = line.split(":")

            RowReading_IsReadingRow = True
            RowReading_LastRowID = int(LineSplit[1])
            print("RowReading : RowID {0}".format(str(RowReading_LastRowID)))
            continue

        # Finish Row Reading
        if line == "%row_end" and RowReading_IsReadingRow:
            print("RowReading : Finished Reading Row {0}".format(RowReading_LastRowID))

            ObjToAdd = UI.TrackColection(int(RowReading_LastRowID), False)
            for block in RowReading_BlocksList:
                ObjToAdd.Tracks.append(block)

            ReadPatternsList[int(LastReadingRegion_Name.split(":")[1])].Tracks.append(ObjToAdd)

            RowReading_IsReadingRow = False
            RowReading_LastRowID = 0

            RowReading_BlocksList.clear()
            continue

        # Get BlockData
        BlockData = line.split(":")

        BlockFrequency = BlockData[0]
        BlockDuration = BlockData[1]

        TrackblockToAdd = UI.TrackBlock((BlockFrequency, BlockDuration))

        RowReading_BlocksList.append(TrackblockToAdd)

    # Set the VarValues
    var.BPM = MusicData_BPM
    var.Rows = MusicData_Rows
    var.Highlight = MusicData_Highlight
    var.HighlightSecond = MusicData_HighlightSecound
    var.Patterns = MusicData_Patterns
    var.SelectedTrack = 0

    # Replace the Patterns List
    track_list.PatternList.clear()
    track_list.PatternList = ReadPatternsList

    # -- Set to the Pattern 0 -- #
    track_list.SetCurrentPattern_ByID(0)

    if MusicData_VersionSaved != var.ProcessReference.DefaultContents.Get_RegKey("/version"):
        FileImportedFromOlderVersion = True

    OptionsBar.UpdateChanger()

    # Re-Update all tracks
    for track in track_list.PatternList:
        track.UpdateTracksPosition()
        for TrackCol in track.Tracks:
            for block in TrackCol.Tracks:
                block.Active = True
                block.HighlightUpdated = False
                block.SurfaceUpdateTrigger = True
                block.DisabledTrigger = False
                block.RootActivated = True
                block.ResetSurface()
                block.Update()
                block.ReRender()

    if FileImportedFromOlderVersion and not var.ProcessReference.DefaultContents.Get_RegKey("/dialog/imported_older_version/show_once", bool):
        var.ProcessReference.GreyDialog(var.ProcessReference.DefaultContents.Get_RegKey("/dialog/imported_older_version/title"), var.ProcessReference.DefaultContents.Get_RegKey("/dialog/imported_older_version/text"))
        var.ProcessReference.DefaultContents.Write_RegKey("/dialog/imported_older_version/show_once", "True")

def NewMusicFile():
    global track_list

    track_list = UI.TrackList()
    del track_list
    tge.Utils.GarbageCollector_Collect()

    # -- Unload the Current SoundCahce -- #
    UI.ContentManager.UnloadSoundTuneCache()

    # -- Update Tittlebar -- #
    var.ProcessReference.TITLEBAR_TEXT = "OneTrack v{0}".format(var.ProcessReference.DefaultContents.Get_RegKey("/version"))

    track_list = UI.TrackList()
    track_list.Rectangle = pygame.Rect(0, 100, Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight - 200)

    var.BPM = 150
    var.Rows = 32
    var.GenerateSoundCache = True
    var.SelectedTrack = 0
    var.Highlight = 4
    var.HighlightSecond = 16
    var.Patterns = 2

    OptionsBar.UpdateChanger()
    OptionsBar.Update()

    var.ProcessReference.DefaultContents.Write_RegKey("/dialog/imported_older_version/show_once", "False")


def Update():
    global track_list
    global TopBarControls
    global DropDownFileMenu

    SaveFileDialog.Update()
    OpenFileDialog.Update()

    if var.DisableControls:
        return

    TopBarControls.Update()
    UpdateTopBar()

    if var.FileMenuEnabled:
        DropDownFileMenu.Update()
        return

    track_list.Update()
    OptionsBar.Update()
    EditorBar.Update()
    SoundCacheMessage.Update()

def UpdateTopBar():
    if TopBarControls.ClickedButtonIndex == 0:
        if not var.FileMenuEnabled:
            var.FileMenuEnabled = True

        else:
            var.FileMenuEnabled = False

def DropDownButtonsActions_SaveButton():
    DropDownFileMenu.SelectedItem = ""
    var.FileMenuEnabled = False
    var.DisableControls = True

    SaveFileDialog.Enabled = True

def DropDownButtonsActions_LoadButton():
    DropDownFileMenu.SelectedItem = ""
    var.FileMenuEnabled = False
    var.DisableControls = True

    OpenFileDialog.Enabled = True


def DropDownButtonsActions_NewFileButton():
    DropDownFileMenu.SelectedItem = ""
    var.FileMenuEnabled = False

    NewMusicFile()

def DropDownButtonsActions_AboutButton():
    DropDownFileMenu.SelectedItem = ""
    var.FileMenuEnabled = False

    var.ProcessReference.GreyDialog("About", var.ProcessReference.DefaultContents.Get_RegKey("/dialog/about/text").replace("$version", var.ProcessReference.DefaultContents.Get_RegKey("/version")), "logo")

def DropDownButtonsActions_SettingsButton():
    DropDownFileMenu.SelectedItem = ""
    var.FileMenuEnabled = False

    Core.MAIN.CreateProcess("OneTrack/UnatachedDialog", "OneTrack Dialog", (var.ProcessReference, "DIALOG_SETTINGS"))


def EventUpdate(event):
    global track_list
    global TopBarControls
    global DropDownFileMenu

    if not var.DisableControls:
        if not var.FileMenuEnabled:
            track_list.EventUpdate(event)
            OptionsBar.EventUpdate(event)
            EditorBar.EventUpdate(event)

        DropDownFileMenu.EventUpdate(event)
        TopBarControls.EventUpdate(event)
