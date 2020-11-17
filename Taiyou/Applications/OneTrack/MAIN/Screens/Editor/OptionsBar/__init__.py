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
import pygame, re, Core
from Core import Utils
import OneTrack.MAIN as Main
from OneTrack.MAIN import UI
from OneTrack.MAIN.Screens import Editor
from OneTrack.MAIN.Screens.Editor import InstanceVar as var

WidgetCollection = UI.Widget.Widget_Controller
OptionsBarSurface = pygame.Surface

def Initialize():
    global WidgetCollection
    global OptionsBarSurface

    OptionsBarSurface = pygame.Surface((680, 90))

    WidgetCollection = UI.Widget.Widget_Controller((0, 5, 680, 90))
    WidgetCollection.Append(UI.Widget.Widget_PictureBox((5, 5, 203, 81), "/logo.png", 0))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((5, 5), "BPM", "150", 1))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((5, 42), "ROWS", "31", 2))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((58, 5), "HIGHLIGHT", "04x16", 3))
    WidgetCollection.Append(UI.Widget.Widget_Label("/PressStart2P.ttf", ''.join(("v", UI.ContentManager.Get_RegKey("/version"))), 9, (200, 200, 200), 5, 5, 4))
    WidgetCollection.Append(UI.Widget.Widget_ValueChanger((58, 42), "CHANNELS", "4", 5))
    WidgetCollection.Append(UI.Widget.Widget_Button("Apply", 18, 175, 7, 6))

    # -- Set Logo Location -- #
    obj = WidgetCollection.GetWidget(0)
    obj.Rectangle[0] = (WidgetCollection.Rectangle[2] - obj.Rectangle[2])

    # -- Initialy Update All Objects -- #
    for obj in WidgetCollection.WidgetCollection:
        obj.Update()

def EventUpdate(event):
    global WidgetCollection

    WidgetCollection.EventUpdate(event)

def Update():
    global WidgetCollection

    WidgetCollection.Update()

    UpdateBPMSelector()
    UpdateRowsSelector()
    UpdateHighlightSelector()
    UpdatePatternsSelector()
    UpdateApplyButton()

    # -- Set Label Version Location
    obj = WidgetCollection.GetWidget(4)
    PictcBox = WidgetCollection.GetWidget(0)
    obj.Rectangle[0] = PictcBox.Rectangle[0]
    obj.Rectangle[1] = PictcBox.Rectangle[1] + PictcBox.Rectangle[3] - 5

def UpdateChanger():
    global NewBPMValue
    global NewRowsValue
    global NewPatternValue
    global NewHighlightSelector
    global NewHighlightSecoundSelector
    global WidgetCollection

    NewBPMValue = var.BPM
    NewRowsValue = var.Rows
    NewPatternValue = var.Patterns
    NewHighlightSelector = var.Highlight
    NewHighlightSecoundSelector = var.HighlightSecond

    Obj = WidgetCollection.GetWidget(1)
    Obj.Changer.Value = str(NewBPMValue).zfill(3)
    Obj.Active = True

    Obj = WidgetCollection.GetWidget(2)
    Obj.Changer.Value = str(NewRowsValue).zfill(2)
    Obj.Active = True

    Obj = WidgetCollection.GetWidget(3)
    Obj.Changer.Value = str(''.join((str(NewHighlightSelector).zfill(2), "x", str(NewHighlightSecoundSelector).zfill(2))))
    Obj.Active = True

    Obj = WidgetCollection.GetWidget(5)
    Obj.Changer.Value = str(NewPatternValue)
    Obj.Active = True


    WidgetCollection.Active = True
    WidgetCollection.Update()

NewBPMValue = 0
NewPatternValue = 0
NewRowsValue = 0
NewHighlightSelector = 0
NewHighlightSecoundSelector = 0

def UpdateBPMSelector():
    global NewBPMValue
    if WidgetCollection.LastInteractionID == 1:
        NewBPMValue = int(WidgetCollection.LastInteractionType)

        if NewBPMValue <= 10:
            NewBPMValue = 10

        if NewBPMValue >= 500:
            NewBPMValue = 500

    else:
        obj = WidgetCollection.GetWidget(1)
        obj.Changer.Value = str(NewBPMValue).zfill(3)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdatePatternsSelector():
    global NewPatternValue
    if WidgetCollection.LastInteractionID == 5:
        NewPatternValue = int(WidgetCollection.LastInteractionType)

        if NewPatternValue > 4:
            NewPatternValue = 4
        elif NewPatternValue <= 0:
            NewPatternValue = 1

    else:
        if NewPatternValue > 4:
            NewPatternValue = 4
        elif NewPatternValue <= 0:
            NewPatternValue = 1

        obj = WidgetCollection.GetWidget(5)
        obj.Changer.Value = str(NewPatternValue)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdateRowsSelector():
    global NewRowsValue
    if WidgetCollection.LastInteractionID == 2:
        # -- Validate the Current Value -- #
        CurrentValue = WidgetCollection.LastInteractionType
        RowsValue = int(CurrentValue)

        if RowsValue > 74:
            RowsValue = 74

        NewRowsValue = RowsValue

        # -- Get the Changer Object -- #
        obj = WidgetCollection.GetWidget(2)
        # -- Re-Format the String -- #
        obj.Changer.Value = str(NewRowsValue).zfill(2)
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdateHighlightSelector():
    global NewHighlightSelector
    global NewHighlightSecoundSelector

    if WidgetCollection.LastInteractionID == 3:
        # -- Validate the Current Value -- #
        CurrentValue = WidgetCollection.LastInteractionType
        HightLightValue = list(CurrentValue)

        FirstVal = ''.join((HightLightValue[0], HightLightValue[1]))
        SecondVal = ''.join((HightLightValue[3], HightLightValue[4]))

        if int(FirstVal) > 32:
            FirstVal = 32

        if int(SecondVal) > 32:
            SecondVal = 32

        NewHighlightSelector = int(FirstVal)
        NewHighlightSecoundSelector = int(SecondVal)

        # -- Get the Changer Object -- #
        obj = WidgetCollection.GetWidget(3)
        # -- Re-Format the String -- #4
        obj.Changer.Value = ''.join((str(NewHighlightSelector).zfill(2), "x", str(NewHighlightSecoundSelector).zfill(2)))
        obj.Changer.SplitedAlgarims = list(obj.Changer.Value)

def UpdateApplyButton():
    if WidgetCollection.LastInteractionID == 6:
        if WidgetCollection.LastInteractionType:
            # -- Set Variables -- #
            var.BPM = NewBPMValue
            var.Rows = NewRowsValue
            var.Patterns = NewPatternValue
            var.Highlight = NewHighlightSelector
            var.HighlightSecond = NewHighlightSecoundSelector

            # -- Update the Tracks Blocks -- #
            for track in Editor.track_list.PatternList:
                for patternCol in track.Tracks:
                    for block in patternCol.Tracks:
                        block.Active = True

            # -- Re-Check the Variables Values -- #
            UpdateChanger()

def Draw(DISPLAY):
    global WidgetCollection

    OptionsBarSurface.fill((62, 62, 116))

    WidgetCollection.Draw(OptionsBarSurface)

    DISPLAY.blit(OptionsBarSurface, (Core.MAIN.ScreenWidth / 2 - OptionsBarSurface.get_width() / 2 + 15, 5))
    WidgetCollection.Rectangle[0] = Core.MAIN.ScreenWidth / 2 - OptionsBarSurface.get_width() / 2 + 15
    WidgetCollection.Rectangle[1] = 5

