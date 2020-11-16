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
import Core


print("Taiyou FX version " + Core.Get_FXVersion())

def Simple_BlurredRectangle(SourceSurface, Rectangle, BlurAmmount=100, BackgroundAlpha=100, BackgroundFillColor=(0, 0, 0)):
    # Create new surface, blit SourceSurface
    ResultCeira = pygame.Surface((Rectangle[2], Rectangle[3]))
    ResultCeira.blit(SourceSurface, (0, 0), (Rectangle[0], Rectangle[1], Rectangle[2], Rectangle[3]))
    ResultCeira = Core.Fx.Surface_Blur(ResultCeira, BlurAmmount)

    # Copy the ResultCeira surface, fill with Fill Color then set a Alpha Value
    BlackBG = ResultCeira.copy()
    BlackBG.fill(BackgroundFillColor)
    BlackBG.set_alpha(BackgroundAlpha)

    # Blit everthing when done
    ResultCeira.blit(BlackBG, (0, 0))

    return ResultCeira

def BlurredRectangle(DISPLAY, Rectangle, BlurAmmount=100, BlackContrast_Alpha=50, BlackBackgroundColor=(0, 0, 0)):
    """
    Render a blurred Rectangle, usefull for UI.
    :param DISPLAY:The surface to be blitted
    :param Rectangle:Rectangle
    :param BlurAmmount:The ammount of blur (value higher than 100 is recomended)
    :param BlackContrast:The ammount of Black Color (usefull for contrast in bright surfaces)
    :return:
    """
    # -- the Result Surface -- #
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)

    if BlurAmmount < 1:
        BlurAmmount = 1

    if BlackContrast_Alpha < 1:
        BlackContrast_Alpha = 1

    if not BlackContrast_Alpha == 0:
        DarkerBG = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
        DarkerBG.fill((BlackBackgroundColor[0], BlackBackgroundColor[1], BlackBackgroundColor[2], BlackContrast_Alpha))
        DarkerBG.set_alpha(BlackContrast_Alpha)
        DISPLAY.blit(DarkerBG, Rectangle)

    # -- Only Blur the Necessary Area -- #
    AreaToBlur = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
    AreaToBlur.blit(DISPLAY, (0, 0), Rectangle)

    # -- Then Finnaly, blit the Blurred Result -- #
    ResultPanel.blit(Surface_Blur(AreaToBlur, BlurAmmount, False), (0, 0))

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))

def BlurredRectangleReturnResult(DISPLAY, Rectangle, BlurAmmount=100, BlackContrast_Alpha=50, BlackBackgroundColor=(0, 0, 0)):
    """
    Render a blurred Rectangle, usefull for UI.
    :param DISPLAY:The surface to be blitted
    :param Rectangle:Rectangle
    :param BlurAmmount:The ammount of blur (value higher than 100 is recomended)
    :param BlackContrast:The ammount of Black Color (usefull for contrast in bright surfaces)
    :return:
    """
    # -- the Result Surface -- #
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)

    if BlurAmmount < 1:
        BlurAmmount = 1

    if BlackContrast_Alpha < 1:
        BlackContrast_Alpha = 1

    if not BlackContrast_Alpha == 0:
        DarkerBG = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
        DarkerBG.fill((BlackBackgroundColor[0], BlackBackgroundColor[1], BlackBackgroundColor[2], BlackContrast_Alpha))
        DarkerBG.set_alpha(BlackContrast_Alpha)
        DISPLAY.blit(DarkerBG, Rectangle)

    # -- Only Blur the Necessary Area -- #
    AreaToBlur = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
    AreaToBlur.blit(DISPLAY, (0, 0), Rectangle)

    # -- Then Finnaly, blit the Blurred Result -- #
    ResultPanel.blit(Surface_Blur(AreaToBlur, BlurAmmount, False), (0, 0))

    return ResultPanel


def Surface_Blur(surface, amt, fast_scale=False):
    """
    Applies blur to a Surface
    :param surface:Surface to be blurred
    :param amt:Amount of Blur [minimun 1.0]
    :param fast_scale:If true, pixalizate the surface insted of blurring
    :return:Returns the Blurred Surface
    """

    if amt < 1.0:
        return surface

    Scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * Scale), int(surf_size[1] * Scale))
    if not fast_scale:
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf
    else:
        surf = pygame.transform.scale(surface, scale_size)
        surf = pygame.transform.scale(surf, surf_size)
        return surf
