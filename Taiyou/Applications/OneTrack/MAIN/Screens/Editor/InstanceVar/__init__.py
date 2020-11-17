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
from Core import CntMng

BPM = 150
Rows = 32
Highlight = 4
HighlightSecond = 16
Editor_CurrentOctave = 4
Patterns = 2

FileMenuEnabled = False
DisableControls = False
GenerateSoundCache = True
GenerateSoundCache_MessageSeen = False
PlayMode = False
SelectedTrack = 0
PatternIsUpdating = False
AwaysUpdate = False
ProcessReference = None
Volume = 0.1
DefaultContent = CntMng.ContentManager

def LoadDefaultValues():
    global Volume

    Volume = DefaultContent.Get_RegKey("/options/VolumeMultiplier", float)
