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
import pygame
from OneTrack import MAIN as Main
from OneTrack.MAIN import UI

from Core import MAIN
from Core import Utils
from Core import SHAPES

LagIndicatorSurface = pygame.Surface
LagTextWidth = 0
LagTextHeight = 0
LagTextColor = ()
LagEnabled = False
Alpha = 0
FlashingAnimation = Utils.AnimationController

def Initialize():
    global LagIndicatorSurface
    global LagTextWidth
    global LagTextHeight
    global LagTextColor
    global FlashingAnimation

    LagTextWidth = UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, "LAG")
    LagTextHeight = UI.ContentManager.GetFont_height("/PressStart2P.ttf", 14, "LAG")

    LagIndicatorSurface = pygame.Surface((LagTextWidth + 4, LagTextHeight + 4))
    LagTextColor = (255, 0, 0)
    FlashingAnimation = Utils.AnimationController(5, 255, multiplierRestart=True)

def Draw(DISPLAY):
    global LagIndicatorSurface
    global LagTextColor
    global LagEnabled
    global Alpha

    if not LagEnabled:
        return

    LagText = "LAG: " + Utils.FormatNumber(MAIN.clock.get_fps(), 2)
    LagTextWidth = UI.ContentManager.GetFont_width("/PressStart2P.ttf", 14, LagText)
    LagTextHeight = UI.ContentManager.GetFont_height("/PressStart2P.ttf", 14, LagText)

    SHAPES.Shape_Rectangle(DISPLAY, (0, 0, 0), (5 - 2, 5 - 2, LagTextWidth + 4, LagTextHeight + 4), 0, 3)
    UI.ContentManager.FontRender(DISPLAY, "/PressStart2P.ttf", 14, LagText, LagTextColor, 5, 5)

def Update():
    global Alpha
    global LagEnabled
    global LagTextColor
    global FlashingAnimation

    FPS = MAIN.clock.get_fps()

    if FPS >= 58:
        Alpha = 0

    else:
        Alpha = 255

    if Alpha == 0:
        LagEnabled = False

    else:
        LagEnabled = True

    if not LagEnabled:
        return

    FlashingAnimation.Update()
    # -- Aways Active the Animation Controller -- #
    FlashingAnimation.Enabled = True

    LagTextColor = (FlashingAnimation.Value, 0, 0)

