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
import pygame, Core
from OneTrack.MAIN import UI
from OneTrack.MAIN.Screens.Editor import InstanceVar as var

WidgetCollection = UI.Widget.Widget_Controller
Surface = pygame.Surface

def Initialize():
    global WidgetCollection
    global Surface

    Surface = pygame.Surface((680, 90))

    WidgetCollection = UI.Widget.Widget_Controller((0, 5, 680, 90))
    WidgetCollection.Append(UI.Widget.Widget_Label("/PressStart2P.ttf", "Current Octave: 7", 12, (230, 230, 230), 2, 5, 0))
    WidgetCollection.Append(UI.Widget.Widget_PianoKeys(2, 24, 0))

    obj = WidgetCollection.GetWidget(0)
    obj.Rectangle[0] = (WidgetCollection.Rectangle[2] - obj.Rectangle[2])

    # -- Initialy Update All Objects -- #
    for obj in WidgetCollection.WidgetCollection:
        obj.Update()

def Draw(DISPLAY):
    global WidgetCollection
    global Surface

    Surface.fill((62, 62, 116))

    WidgetCollection.Draw(Surface)

    DISPLAY.blit(Surface, (Core.MAIN.ScreenWidth / 2 - Surface.get_width() / 2 + 15, DISPLAY.get_height() - Surface.get_height() - 5))
    WidgetCollection.Rectangle[0] = Core.MAIN.ScreenWidth / 2 - Surface.get_width() / 2 + 15
    WidgetCollection.Rectangle[1] = DISPLAY.get_height() - Surface.get_height() - 5

def Update():
    global WidgetCollection

    WidgetCollection.Update()

    UpdateOctaveNumber()

def UpdateOctaveNumber():
    obj = WidgetCollection.GetWidget(0)
    obj.Text = ''.join(("Current Octave: ", str(var.Editor_CurrentOctave)))


def EventUpdate(event):
    global WidgetCollection

    WidgetCollection.EventUpdate(event)

