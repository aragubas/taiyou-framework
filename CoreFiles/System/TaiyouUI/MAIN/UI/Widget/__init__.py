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
from Core import Utils
from Core import Convert
from Core import Shape
from CoreFiles.System.TaiyouUI.MAIN import UI

class Widget_Controller:
    def __init__(self, pContentManager, Rectangle):
        self.Rectangle = Convert.List_PygameRect(Rectangle)
        self.WidgetCollection = list()
        self.LastInteractionID = -1
        self.LastInteractionType = None
        self.Active = False
        self.ContentManager = pContentManager
        self.Opacity = 255

    def Draw(self, DISPLAY):
        WidgetSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        WidgetSurface.set_alpha(self.Opacity)
        for widget in self.WidgetCollection:
            widget.Render(WidgetSurface)

        DISPLAY.blit(WidgetSurface, (self.Rectangle[0], self.Rectangle[1]))

        if not self.LastInteractionID == -1:
            self.WidgetCollection[self.LastInteractionID].InteractionType = None

        self.LastInteractionID = -1
        self.LastInteractionType = None

    def Append(self, Widget):
        self.WidgetCollection.append(Widget)

    def Update(self):
        self.Active = self.Rectangle.collidepoint(pygame.mouse.get_pos())

        if not self.Active:
            for widget in self.WidgetCollection:
                widget.Active = False
            return

        for widget in self.WidgetCollection:
            widget.Update()

            if not widget.InteractionType is None:
                self.LastInteractionID = widget.ID
                self.LastInteractionType = widget.InteractionType

    def EventUpdate(self, event):
        for widget in self.WidgetCollection:
            if widget.AwaysUpdate:  # -- If aways update, update it no matter what
                if widget.EventUpdateable:
                    widget.EventUpdate(event)
                    continue
            else:  # -- If not, only update when mouse is hovering it
                if self.Active:
                    ColideRect = pygame.Rect(self.Rectangle[0] + widget.Rectangle[0], self.Rectangle[1] + widget.Rectangle[1], widget.Rectangle[2], widget.Rectangle[3])
                    if ColideRect.collidepoint(pygame.mouse.get_pos()):
                        if widget.EventUpdateable:
                            widget.CursorOffset = (self.Rectangle[0] + widget.Rectangle[0], self.Rectangle[1] + widget.Rectangle[1])
                            widget.EventUpdate(event)
                        widget.Active = True
                    else:
                        widget.Active = False

    def GetWidget(self, WidgetID):
        for widget in self.WidgetCollection:
            if widget.ID == WidgetID:
                return widget

class Widget_PictureBox:
    def __init__(self, pContentManager, Rectangle, ImageName, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.Rectangle = Utils.Convert.List_PygameRect(Rectangle)
        self.ImageName = ImageName
        self.ID = WidgetID
        self.InteractionType = None
        self.Active = False
        self.EventUpdateable = False
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)
        self.Content = pContentManager

    def Render(self, DISPLAY):
        self.Content.ImageRender(DISPLAY, self.ImageName, self.Rectangle[0], self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

    def Update(self):
        pass

    def EventUpdate(self, event):
        pass

class Widget_ValueChanger:
    def __init__(self, pContentManager, Position, TitleName, ChangerInitialValue, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.Rectangle = Utils.Convert.List_PygameRect((Position[0], Position[1], 48, 34))
        self.TitleName = TitleName
        self.ID = WidgetID
        self.Content = pContentManager
        self.Changer = UI.EditableNumberView(pygame.Rect(self.Rectangle[0], self.Rectangle[1] + 17, self.Rectangle[2], self.Rectangle[3] - 17), ChangerInitialValue)
        self.LastValue = ChangerInitialValue
        self.InteractionType = None
        self.Active = False
        self.EventUpdateable = True
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)

    def Render(self, DISPLAY):
        # -- Render Background -- #
        BGColor = UI.ThemesManager_GetProperty("Button_Active_BackgroundColor")
        LineColor = UI.ThemesManager_GetProperty("Button_Active_IndicatorColor")

        if not self.Active:
            BGColor = UI.ThemesManager_GetProperty("Button_Inactive_BackgroundColor")
            LineColor = UI.ThemesManager_GetProperty("Button_Active_IndicatorColor")

        Shape.Shape_Rectangle(DISPLAY, BGColor, self.Rectangle)
        Shape.Shape_Rectangle(DISPLAY, LineColor, self.Rectangle, 1)

        # -- Render Change Title -- #
        TitleX = self.Rectangle[0] + self.Rectangle[2] / 2 - self.Content.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName) / 2

        self.Content.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 12, self.TitleName, (230, 230, 230), TitleX, self.Rectangle[1])

        # -- Render EditableNumberView -- #
        self.Changer.Render(DISPLAY)

    def Update(self):
        self.Changer.Update()

        if not self.Changer.Value == self.LastValue:
            self.LastValue = self.Changer.Value
            self.InteractionType = self.Changer.Value

        if self.Content.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) > self.Rectangle[2]:
            self.Rectangle[2] = self.Rectangle[2] + self.Content.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) + 5

        if self.Content.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName) > self.Rectangle[2]:
            self.Rectangle[2] = self.Rectangle[2] + self.Content.GetFont_width("/Ubuntu_Bold.ttf", 12, self.TitleName)

        self.Changer.Rectangle[0] = self.Rectangle[0] + self.Rectangle[2] / 2 - self.Content.GetFont_width("/PressStart2P.ttf", 12, self.Changer.Value) / 2

    def EventUpdate(self, event):
        self.Changer.EventUpdate(event)

class Widget_Label:
    def __init__(self, pContentManager, FontName, Text, FontSize, Color, X, Y, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")

        self.ID = WidgetID
        self.Content = pContentManager
        self.InteractionType = None
        self.Active = False
        self.EventUpdateable = False
        self.Text = Text
        self.FontSize = FontSize
        self.FontName = FontName
        self.Color = Color
        self.X = X
        self.Y = Y
        self.Rectangle = Utils.Convert.List_PygameRect((X, Y, self.Content.GetFont_width(self.FontName, FontSize, self.Text), self.Content.GetFont_height(self.FontName, FontSize, self.Text)))
        self.AwaysUpdate = False
        self.CursorOffset = (0, 0)

    def Render(self, DISPLAY):
        self.Content.FontRender(DISPLAY, self.FontName,self.FontSize, self.Text, self.Color, self.Rectangle[0], self.Rectangle[1])

    def Update(self):
        self.Rectangle = Utils.Convert.List_PygameRect((self.X, self.Y, self.Content.GetFont_width(self.FontName, self.FontSize, self.Text), self.Content.GetFont_height(self.FontName, self.FontSize, self.Text)))

    def EventUpdate(self, event):
        pass


class Widget_Button:
    def __init__(self, pContentManager,Text, FontSize, X, Y, WidgetID):
        if WidgetID == -1:
            raise ValueError("WidgetID cannot be -1")
        self.ID = WidgetID
        self.InteractionType = None
        self.Content = pContentManager
        self.Active = True
        self.EventUpdateable = True
        self.AwaysUpdate = False
        self.X = X
        self.Y = Y
        self.Text = Text
        self.FontSize = FontSize
        self.TextWidth = self.Content.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
        self.TextHeight = self.Content.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
        self.Rectangle = Convert.List_PygameRect((X - 2, Y - 2, self.TextWidth + 4, self.TextHeight + 4))
        self.LastRect = self.Rectangle
        self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        self.Centred_X = self.Rectangle[2] / 2 - self.Content.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
        self.Centred_Y = self.Rectangle[3] / 2 - self.Content.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
        self.ButtonState = 0
        self.CursorOffset = (0, 0)
        self.BgColor = UI.ThemesManager_GetProperty("Button_BackgroundColor")
        self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

    def Render(self, DISPLAY):
        # -- Render Background -- #
        Shape.Shape_Rectangle(self.Surface, self.BgColor, (0, 0, self.Rectangle[2], self.Rectangle[3]))
        # -- Render Indicator -- #
        Shape.Shape_Rectangle(self.Surface, self.IndicatorColor, (0, 0, self.Rectangle[2], self.Rectangle[3]), 1)

        # -- Render the Button Text -- #
        self.Content.FontRender(self.Surface, "/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text, (240, 240, 240), self.Centred_X, self.Centred_Y)

        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ButtonState == 2:
            self.ButtonState = 0

    def Update(self):
        # -- Check if surface has the correct size -- #
        if not self.LastRect == self.Rectangle:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

            # -- Update all Size and Position Variables -- #
            self.TextWidth = UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
            self.TextHeight = UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize, self.Text)
            self.Rectangle = Utils.Convert.List_PygameRect((self.Rectangle[0] - 2, self.Rectangle[1] - 2, self.TextWidth + 4, self.TextHeight + 4))
            self.Centred_X = self.Rectangle[2] / 2 - UI.ContentManager.GetFont_width("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2
            self.Centred_Y = self.Rectangle[3] / 2 - UI.ContentManager.GetFont_height("/Ubuntu_Bold.ttf", self.FontSize - 2, self.Text) / 2

            self.LastRect = self.Rectangle

        self.BgColor = UI.ThemesManager_GetProperty("Button_BackgroundColor")
        self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        if not self.Active:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

            return

        if self.ButtonState == 0:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Inactive_IndicatorColor")

        elif self.ButtonState == 1:
            self.IndicatorColor = UI.ThemesManager_GetProperty("Button_Active_IndicatorColor")

    def EventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.ButtonState = 1

        if event.type == pygame.MOUSEBUTTONUP:
            self.ButtonState = 0
            self.InteractionType = True
            self.Content.PlaySound("/click.wav")

