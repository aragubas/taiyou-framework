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
import Core, pygame
from OneTrack.MAIN.Screens.Editor import InstanceVar as var
from OneTrack.MAIN import UI


class Screen:
    def __init__(self, pRoot_Process):
        self.Root_Process = pRoot_Process
        self.Root_Process.DISPLAY = pygame.Surface((420, 320))

        self.Root_Process.TITLEBAR_TEXT = "OneTrack Settings"

        self.WidgetController = UI.Widget.Widget_Controller((0, 0, self.Root_Process.DISPLAY.get_width(), self.Root_Process.DISPLAY.get_height()))
        self.ReloadUI()

        self.LastThemeName = ""
        self.LastAnimationScale = ""
        self.LastVolumeMultiplier = ""

    def ReloadUI(self):
        self.WidgetController.Clear()

        ButtonFalseSize = UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", 14, "False")

        # Smooth Scroll Option
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/smooth_scroll"), 14, 5, 5, 0))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Smooth Scrolling", 14, (230, 230, 230), ButtonFalseSize + 10, 5, 1))

        # Disable Dynamic Color Option
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/disabled_block_color"), 14, 5, 35, 2))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Dynamic Block Color", 14, (230, 230, 230), ButtonFalseSize + 10, 35, 3))

        # Trackpointer Animation Option
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/trackpointer_animation"), 14, 5, 65, 4))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Animated Trackpointer", 14, (230, 230, 230), ButtonFalseSize + 10, 65, 5))

        # Selected Theme
        self.WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/selected_theme"), 14, (230, 230, 230), 120, 95, 6))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "UI Theme", 14, (230, 230, 230), 5, 95, 7))
        self.WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 75, 95, 8))

        # Animation Scale
        self.WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/options/animation_scale"), 14, (230, 230, 230), 160, 125, 9))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Animation Scale", 14, (230, 230, 230), 5, 125, 10))
        self.WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 115, 125, 11))

        # Volume Multiplier
        self.WidgetController.Append(UI.Widget.Widget_Textbox("/Ubuntu.ttf", var.DefaultContent.Get_RegKey("/options/VolumeMultiplier"), 14, (230, 230, 230), 170, 155, 12))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Volume Multiplier", 14, (230, 230, 230), 5, 155, 13))
        self.WidgetController.Append(UI.Widget.Widget_Button("Apply", 14, 127, 155, 14))

        # PerTrack Scroll
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/per_track_scroll"), 14, 5, 185, 15))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Per-Track Scroll", 14, (230, 230, 230), ButtonFalseSize + 10, 185, 16))

        # Looking Glass
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/looking_glass"), 14, 5, 215, 17))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Looking Glass Windows", 14, (230, 230, 230), ButtonFalseSize + 10, 215, 18))

        # Square Trackpointer
        self.WidgetController.Append(UI.Widget.Widget_Button(var.DefaultContent.Get_RegKey("/options/block_trackpointer"), 14, 5, 245, 19))
        self.WidgetController.Append(UI.Widget.Widget_Label("/Ubuntu.ttf", "Toggle Arrow/Block Trackpointer", 14, (230, 230, 230), ButtonFalseSize + 10, 245, 20))

    def Update(self):
        self.WidgetController.Update()

        # SmoothScrolling Option
        if self.WidgetController.LastInteractionID == 0:
            if var.DefaultContent.Get_RegKey("/options/smooth_scroll", bool):
                var.DefaultContent.Write_RegKey("/options/smooth_scroll", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/smooth_scroll", "True")
            self.ReloadUI()

        # Disabled Block Color
        if self.WidgetController.LastInteractionID == 2:
            if var.DefaultContent.Get_RegKey("/options/disabled_block_color", bool):
                var.DefaultContent.Write_RegKey("/options/disabled_block_color", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/disabled_block_color", "True")
            self.ReloadUI()

        # Trackpointer Animation
        if self.WidgetController.LastInteractionID == 4:
            if var.DefaultContent.Get_RegKey("/options/trackpointer_animation", bool):
                var.DefaultContent.Write_RegKey("/options/trackpointer_animation", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/trackpointer_animation", "True")
            self.ReloadUI()

        # Theme Name textbox
        if self.WidgetController.LastInteractionID == 6:
            CurrentText = self.WidgetController.LastInteractionType

            if len(CurrentText) == 0:
                CurrentText = "default"

            CurrentText = CurrentText.replace(" ", "_")

            # Check if theme exists
            self.LastThemeName = CurrentText

        # Theme Apply
        if self.WidgetController.LastInteractionID == 8:
            # Check if theme exists
            try:
                UwU = var.DefaultContent.Get_RegKey("/theme/{0}".format(self.LastThemeName))
                UwU = self.LastThemeName

            except:
                print("Cannot find the theme file ({0}).".format(self.LastThemeName))
                UwU = "default"

            var.DefaultContent.Write_RegKey("/selected_theme", UwU)

            UI.ThemesManager_LoadTheme(UI.ContentManager.Get_RegKey("/selected_theme"))
            self.ReloadUI()

        # Animation Scale Textbox
        if self.WidgetController.LastInteractionID == 9:
            CurrentText = self.WidgetController.LastInteractionType

            if not CurrentText.isdigit():
                CurrentText = "10"

            if len(CurrentText) == 0:
                CurrentText = "10"

            # Check if theme exists
            self.LastAnimationScale = CurrentText

        # Animation Apply
        if self.WidgetController.LastInteractionID == 11:
            UwU = self.LastAnimationScale
            if not UwU.isdigit():
                UwU = "10"

            # Check if theme exists
            var.DefaultContent.Write_RegKey("/options/animation_scale", UwU)

            self.ReloadUI()

        # Volume Multiplier Textbox
        if self.WidgetController.LastInteractionID == 12:
            CurrentText = self.WidgetController.LastInteractionType

            # Check if theme exists
            self.LastVolumeMultiplier = CurrentText

        # Volume Multiplier Apply
        if self.WidgetController.LastInteractionID == 14:
            ActualValue = self.LastVolumeMultiplier
            print(ActualValue)

            try:
                ValueConverted = float(ActualValue)

            except Exception:
                ValueConverted = 0.1

            if ValueConverted >= 1.0:
                ValueConverted = 0.1

            # Check if theme exists
            var.DefaultContent.Write_RegKey("/options/VolumeMultiplier", str(ValueConverted))

            self.ReloadUI()

        # Per-Track Scroll
        if self.WidgetController.LastInteractionID == 15:
            if var.DefaultContent.Get_RegKey("/options/per_track_scroll", bool):
                var.DefaultContent.Write_RegKey("/options/per_track_scroll", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/per_track_scroll", "True")
            self.ReloadUI()

        # Looking Glass Option
        if self.WidgetController.LastInteractionID == 17:
            if var.DefaultContent.Get_RegKey("/options/looking_glass", bool):
                var.DefaultContent.Write_RegKey("/options/looking_glass", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/looking_glass", "True")
            self.ReloadUI()

        # Block Trackpointer Option
        if self.WidgetController.LastInteractionID == 19:
            if var.DefaultContent.Get_RegKey("/options/block_trackpointer", bool):
                var.DefaultContent.Write_RegKey("/options/block_trackpointer", "False")
            else:
                var.DefaultContent.Write_RegKey("/options/block_trackpointer", "True")
            self.ReloadUI()


    def Draw(self, DISPLAY):
        self.WidgetController.Draw(DISPLAY)

    def EventUpdate(self, event):
        self.WidgetController.ClickOffset = (self.Root_Process.POSITION[0], self.Root_Process.POSITION[1] + self.Root_Process.TITLEBAR_RECTANGLE[3])
        self.WidgetController.EventUpdate(event)

    def WhenClosing(self):
        # Reload UI Theme
        var.LoadDefaultValues()
        UI.ThemesManager_LoadTheme(UI.ContentManager.Get_RegKey("/selected_theme"))
        var.GenerateSoundCache = True
        var.PlayMode = True