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
import Core as tge
import Core.SHAPES as Shape
import Core.UTILS as Utils
import CoreFiles.System.TaiyouUI.MAIN.UI.Widget as widget

TaskBar_Version = "2.0"

#region Theme Manager
ThemesList_Properties = list()
ThemesList_PropertyNames = list()

def ThemesManager_LoadTheme(ContentManager, ThemeName):
    global ThemesList_Properties
    global ThemesList_PropertyNames

    ThemesList_Properties.clear()
    ThemesList_PropertyNames.clear()

    print("Taiyou.TaskBar : Loading UI Theme '" + ThemeName + "'")
    for key in ContentManager.Get_RegKey("/theme/{0}".format(ThemeName)).splitlines():
        if key.startswith("#"):
            continue

        if len(key) < 5:
            continue

        ThemeDataTag = key.split(";")[0]
        ThemeDataType = key.split(";")[1]
        ThemeData = key.split(";")[2]
        ThemeRawData = None

        if ThemeDataType == "tuple":
            ThemeRawData = Utils.Convert.Parse_Tuple(ThemeData)

        if ThemeDataType == "int":
            ThemeRawData = int(ThemeData)

        if ThemeDataType == "str":
            ThemeRawData = str(ThemeData)

        print("Property: '{0}' of type '{1}' loaded with value '{2}'".format(ThemeDataTag, ThemeDataType, ThemeData))

        ThemesManager_AddProperty(ThemeDataTag, ThemeRawData)

    print("Taiyou.TaskBar : Theme Loaded sucefully")

def ThemesManager_GetProperty(pPropertyName):
    Index = ThemesList_PropertyNames.index(pPropertyName)

    return ThemesList_Properties[Index]

def ThemesManager_AddProperty(PropertyName, PropertyValue):
    ThemesList_Properties.append(PropertyValue)
    ThemesList_PropertyNames.append(PropertyName)

#endregion


class VerticalListWithDescription:
    def __init__(self, Rectangle, pContentManager):
        self.Rectangle = pygame.Rect(Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3])
        self.LastRectangle = pygame.Rect(0, 0, 0, 0)
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemIndexes = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.ItemProperties = list()
        self.LastItemClicked = "null"
        self.LastItemIndex = None
        self.ScrollY = 0
        self.ListSurface = pygame.Surface
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)
        self.ListSurfaceUpdated = False
        self.ContentManager = pContentManager

    def ResetSelectedItem(self):
        self.LastItemClicked = "null"
        self.LastItemIndex = None

    def Render(self, DISPLAY):
        if not self.Rectangle[2] == self.LastRectangle[2] or not self.Rectangle[3] == self.LastRectangle[3]:
            self.LastRectangle[2] = self.Rectangle[2]
            self.LastRectangle[3] = self.Rectangle[3]

            self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        self.ListSurface.fill((0, 0, 0, 0))

        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (0, self.ScrollY + 42 * i, self.Rectangle[2], 40)

            BackgroundColor = (20, 42, 59, 50)
            ItemNameFontColor = (250, 250, 250)
            BorderColor = (32, 164, 243)
            TextsX = 5
            if self.ItemSprite[i] != "null":
                TextsX = 45

            if self.LastItemIndex == self.ItemIndexes[i]:  # -- When the Item is Selected
                BackgroundColor = (20, 42, 59, 100)
                ItemNameFontColor = (255, 255, 255)
                BorderColor = (46, 196, 182)

            if self.ItemSelected[i]:  # -- When the Item is Clicked
                BackgroundColor = (30, 52, 69, 150)
                ItemNameFontColor = (250, 250, 250)
                BorderColor = (255, 51, 102)

            # -- Background -- #
            Shape.Shape_Rectangle(self.ListSurface, BackgroundColor, ItemRect)

            # -- Indicator Bar -- #
            Shape.Shape_Rectangle(self.ListSurface, BorderColor, ItemRect, 1)

            # -- Render Item Name -- #
            self.ContentManager.FontRender(self.ListSurface, "/Ubuntu_Bold.ttf", 14, itemNam, ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 5)

            # -- Render Item Description -- #
            self.ContentManager.FontRender(self.ListSurface, "/Ubuntu.ttf", 12, self.ItemsDescription[i], ItemNameFontColor, TextsX + ItemRect[0], ItemRect[1] + 25)

            # -- Render the Item Sprite -- #
            if self.ItemSprite[i] != "null":
                self.ContentManager.ImageRender(self.ListSurface, self.ItemSprite[i], ItemRect[0] + 4, ItemRect[1] + 4, 36, 32)

        # -- Blit All Work to Screen -- #
        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        ColisionRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

        if ColisionRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.ScrollY += 5
                    return

                elif event.button == 4:
                    self.ScrollY -= 5
                    return

            # -- Select the Clicked Item -- #
            for i, itemNam in enumerate(self.ItemsName):
                ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ItemRect.collidepoint(pygame.mouse.get_pos()):
                        self.LastItemClicked = itemNam
                        self.ItemSelected[i] = True
                        self.LastItemIndex = self.ItemIndexes[i]

                if event.type == pygame.MOUSEBUTTONUP:
                    self.ItemSelected[i] = False

    def Set_X(self, Value):
        self.Rectangle[0] = int(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = int(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = int(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = int(Value)

    def AddItem(self, ItemName, ItemDescription, ItemSprite = "null", ItemProperties = None):
        self.ItemsName.append(ItemName)
        self.ItemsDescription.append(ItemDescription)
        self.ItemSprite.append(ItemSprite)
        self.ItemSelected.append(False)
        self.ItemIndexes.append((len(self.ItemIndexes)))
        self.ItemProperties.append(ItemProperties)

    def ClearItems(self):
        self.ItemsName.clear()
        self.ItemsDescription.clear()
        self.ItemSprite.clear()
        self.ItemSelected.clear()
        self.ItemIndexes.clear()
        self.ItemProperties.clear()


class ApplicationSelector:
    def __init__(self, pContentManager, pX, pY):
        self.X = pX
        self.Y = pY
        self.Width = 550
        self.Height = 120
        self.Content = pContentManager
        self.ObjectSurface = pygame.Surface((self.Width, self.Height), pygame.SRCALPHA)
        self.SeletorItems_Title = list()
        self.SeletorItems_Index = list()
        self.SeletorItems_Icon = list()
        self.SeletorItems_ModulePath = list()

        self.SelectedItemIndex = -1
        self.SelectedItemTitle = ""
        self.SelectedItemModulePath = None

        self.HScroll = 10

    def Draw(self, Surface):
        self.ObjectSurface.fill((0, 0, 0, 0))

        Shape.Shape_Rectangle(self.ObjectSurface, (0, 0, 0, 150), (0, 0, self.Width, self.Height), 0, 5)

        index = -1
        for item in self.SeletorItems_Index:
            index += 1
            ItemRect = pygame.Rect(self.HScroll + 105 * index, 5, 100, self.Height - 10)
            ItemPicBox = pygame.Rect(ItemRect[0] + 2, ItemRect[1] + 4, ItemRect[2] - 4, ItemRect[3] - 8)

            if self.SelectedItemIndex == index:
                Shape.Shape_Rectangle(self.ObjectSurface, (255, 255, 255, 150), ItemRect, 0, 2)

            if self.SeletorItems_Icon[index] == None:
                self.Content.ImageRender(self.ObjectSurface, "/folder_question.png", ItemPicBox[0], ItemPicBox[1], ItemPicBox[2], ItemPicBox[3], SmoothScaling=True)
            else:
                self.Content.ImageRender(self.ObjectSurface, self.SeletorItems_Icon[index], ItemPicBox[0], ItemPicBox[1], ItemPicBox[2], ItemPicBox[3], SmoothScaling=True, ImageNotLoaded=True)

        Surface.blit(self.ObjectSurface, (self.X, self.Y))

    def AddItem(self, Title, pModulePath, IconPath="None"):
        self.SeletorItems_Title.append(Title.rstrip())
        self.SeletorItems_Index.append(len(self.SeletorItems_Title))
        self.SeletorItems_ModulePath.append(pModulePath)
        if IconPath == "None":
            self.SeletorItems_Icon.append(None)
        else:
            self.SeletorItems_Icon.append(self.Content.ReturnImageObject(IconPath, True))

    def EventUpdate(self, event):
        ThisRect = pygame.Rect(self.X, self.Y, self.Width, self.Height)

        if ThisRect.collidepoint(pygame.mouse.get_pos()):
            index = -1
            SelectedItems = 0
            for item in self.SeletorItems_Title:
                index += 1
                ItemRect = pygame.Rect(self.X + self.HScroll + 105 * index, 5, 100, self.Y + self.Height - 10)

                if ItemRect.collidepoint(pygame.mouse.get_pos()):
                    SelectedItems += 1
                    self.SelectedItemIndex = index
                    self.SelectedItemTitle = item
                    self.SelectedItemModulePath = self.SeletorItems_ModulePath[index]

            if SelectedItems == 0:
                self.SelectedItemIndex = -1
                self.SelectedItemTitle = ""
                self.SelectedItemModulePath = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.HScroll -= 5

            if event.button == 5:
                self.HScroll += 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_HOME:
                self.HScroll = 10
