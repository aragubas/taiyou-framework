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

class Screen:
    def __init__(self, Root, DefaultContents):
        self.DefaultContents = DefaultContents
        self.Root = Root
        self.MainText = "             Downloading header files...\nDownload progress is at top of Screen."
        self.CenterX = self.Root.DISPLAY.get_width() / 2 - self.DefaultContents.GetFont_width("/Ubuntu.ttf", 28, self.MainText) / 2
        self.CenterY = self.Root.DISPLAY.get_height() / 2 - self.DefaultContents.GetFont_height("/Ubuntu.ttf", 28, self.MainText) / 2

    def Render(self, DISPLAY):
        self.DefaultContents.FontRender(DISPLAY, "/Ubuntu.ttf", 28, self.MainText, (250, 250, 255), self.CenterX, self.CenterY)

    def Update(self):
        if self.Root.RequiredFilesDownloaded:
            self.Root.SetScreenByID(1)

    def EventUpdate(self, event):
        pass