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

# -- Modules Versions -- #
def Get_Version():
    return "3.2"

def Get_ShapeVersion():
    return "2.0"

def Get_AppDataVersion():
    return "1.1"

def Get_UtilsVersion():
    return "2.1"

def Get_TaiyouMainVersion():
    return "3.7"

def Get_ContentManagerVersion():
    return "3.1"

def Get_FXVersion():
    return "1.1"

def Get_BootloaderVersion():
    return "1.8"

def Get_MAINVersion():
    return "1.4"

def Get_WindowManagerManagerVersion():
    return "1.2"



# -- Calculate the Version of Taiyou Game Engine -- #
TaiyouGeneralVersion = float(Get_Version()) + float(Get_ShapeVersion()) + float(Get_AppDataVersion()) + float(Get_UtilsVersion()) + float(Get_TaiyouMainVersion()) + float(Get_ContentManagerVersion()) + float(Get_FXVersion()) + float(Get_BootloaderVersion()) + float(Get_MAINVersion()) + float(Get_WindowManagerManagerVersion())

# -- Print Runtime Version -- #
print("\nTaiyou General version " + str(TaiyouGeneralVersion))
print("\n")

# -- Imports All Modules -- #
from Core import CONTENT_MANAGER as cntMng
from Core import APPDATA as appData
from Core import FX as fx
from Core import SHAPES as shape
from Core import UTILS as utils
from Core import MAIN
from Core import WMM as wmm
import os, pygame, platform

# -- Arguments -- #
IsGameRunning = False
VideoDriver = "null"
VideoX11CenterWindow = False
VideoX11DGAMouse = False
VideoX11YUV_HWACCEL = False
AudioDriver = "null"
AudioFrequency = 0
AudioSize = -0
AudioChannels = 0
AudioBufferSize = 0
RunInFullScreen = False
InputMouseDriver = "fbcon"
InputDisableMouse = False
IgnoreSDL2Parameters = True
PygameFastEvent = True
SmoothScaleTransform = "MMX"
ThrowException = False

# -- Taiyou Paths -- #
TaiyouPath_SystemPath = "CoreFiles"
TaiyouPath_AppDataFolder = "AppData"
TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "system.config"
TaiyouPath_CorrectSlash = "/"
LastException = "null"
CurrentPlatform = ""


def InitEngine():
    """
    Initialize all engine
    :return:
    """
    global VideoDriver
    global AudioDriver
    global VideoX11CenterWindow
    global AudioSize
    global AudioBufferSize
    global AudioChannels
    global AudioFrequency
    global RunInFullScreen
    global VideoX11DGAMouse
    global VideoX11YUV_HWACCEL
    global InputMouseDriver
    global InputDisableMouse
    global IgnoreSDL2Parameters
    global SmoothScaleTransform
    global PygameFastEvent
    global TaiyouPath_CorrectSlash
    global TaiyouPath_SystemPath
    global TaiyouPath_TaiyouConfigFile
    global TaiyouPath_CorrectSlash
    global TaiyouPath_AppDataFolder
    global ThrowException
    global CurrentPlatform

    # -- Set the Correct Slash Directory -- #
    CurrentPlatform = platform.system()

    if CurrentPlatform == "Linux":
        TaiyouPath_CorrectSlash = "/"
        TaiyouPath_SystemPath = "CoreFiles/"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "system.config"
        TaiyouPath_AppDataFolder = "./AppsData/"

    elif CurrentPlatform == "Windows":
        TaiyouPath_CorrectSlash = "\\"
        TaiyouPath_SystemPath = "CoreFiles\\"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "system.config"
        TaiyouPath_AppDataFolder = ".\\AppsData\\"

    conf_file = open(TaiyouPath_TaiyouConfigFile)

    for x in conf_file:
        x = x.rstrip()
        SplitedParms = x.split(":")

        if not x.startswith("#"):
            # -- Disable Font Rendering -- #
            if SplitedParms[0] == "DisableFontRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.FontRenderingDisabled = True
                else:
                    CONTENT_MANAGER.FontRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable font rendering set to:" + str(CONTENT_MANAGER.FontRenderingDisabled))

            # -- Disable Image Rendering -- #
            elif SplitedParms[0] == "DisableImageRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.ImageRenderingDisabled = True
                else:
                    CONTENT_MANAGER.ImageRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable sprite rendering set to:" + str(CONTENT_MANAGER.ImageRenderingDisabled))

            # -- Disable Rectangle Rendering -- #
            elif SplitedParms[0] == "DisableRectangleRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.RectangleRenderingDisabled = True
                else:
                    CONTENT_MANAGER.RectangleRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable rectangle rendering set to:" + str(CONTENT_MANAGER.RectangleRenderingDisabled))

            # -- Disable Image Transparency -- #
            elif SplitedParms[0] == "DisableImageTransparency":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.ImageTransparency = True
                else:
                    CONTENT_MANAGER.ImageTransparency = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(CONTENT_MANAGER.ImageTransparency))

            # -- Disable Sound System -- #
            elif SplitedParms[0] == "DisableSoundSystem":
                if SplitedParms[1] == "True":
                    cntMng.DisableSoundSystem = True
                else:
                    cntMng.DisableSoundSystem = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(cntMng.DisableSoundSystem))

            # -- SDL Option: Video Driver -- #
            elif SplitedParms[0] == "VideoDriver":
                VideoDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Video Driver was set to:" + str(VideoDriver))

            # -- SDL Option: Audio Driver -- #
            elif SplitedParms[0] == "AudioDriver":
                AudioDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Audio Driver was set to:" + str(AudioDriver))

            # -- SoundSystem: Audio Device Frequency -- #
            elif SplitedParms[0] == "AudioFrequency":
                AudioFrequency = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Frequency was set to:" + str(AudioFrequency))

            # -- SoundSystem: Audio Device Frame Size -- #
            elif SplitedParms[0] == "AudioSize":
                AudioSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Size was set to:" + str(AudioSize))

            # -- SoundSystem: Audio Device Audio Channels -- #
            elif SplitedParms[0] == "AudioChannels":
                AudioChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Channels was set to:" + str(AudioChannels))

            # -- SoundSystem: Audio Device Buffer Size -- #
            elif SplitedParms[0] == "AudioBufferSize":
                AudioBufferSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Buffer Size was set to:" + str(AudioBufferSize))

            # -- Run in Fullscreen -- #
            elif SplitedParms[0] == "RunInFullScreen":
                if SplitedParms[1].rstrip() == "True":
                    RunInFullScreen = True
                elif SplitedParms[1].rstrip() == "False":
                    RunInFullScreen = False
                else:
                    RunInFullScreen = False

                print("Taiyou.Runtime.InitEngine : Run in Fullscreen was set to:" + str(RunInFullScreen))

            # -- SDL Option: Center Window -- #
            elif SplitedParms[0] == "VideoX11_CenterWindow":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11CenterWindow = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11CenterWindow = False
                else:
                    VideoX11CenterWindow = False

                print("Taiyou.Runtime.InitEngine : VideoX11CenterWindow was set to:" + str(VideoX11CenterWindow))

            # -- SDL Option: DGA Mouse -- #
            elif SplitedParms[0] == "VideoX11_DGAMouse":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11DGAMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11DGAMouse = False
                else:
                    VideoX11DGAMouse = False

                print("Taiyou.Runtime.InitEngine : VideoX11DGAMouse was set to:" + str(VideoX11DGAMouse))

            # -- SDL Option: YUV Hardware Acelleration -- #
            elif SplitedParms[0] == "VideoX11_YUV_HWACCEL":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11YUV_HWACCEL = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11YUV_HWACCEL = False
                else:
                    VideoX11YUV_HWACCEL = False

                print("Taiyou.Runtime.InitEngine : VideoX11YUV_HWACCEL was set to:" + str(VideoX11YUV_HWACCEL))

            # -- SDL Option: Mouse Driver -- #
            elif SplitedParms[0] == "InputMouseDriver":
                InputMouseDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : InputMouseDriver was set to:" + str(InputMouseDriver))

            # -- SDL Option: Disable Mouse -- #
            elif SplitedParms[0] == "InputDisableMouse":
                if SplitedParms[1].rstrip() == "True":
                    InputDisableMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    InputDisableMouse = False
                else:
                    InputDisableMouse = False

                print("Taiyou.Runtime.InitEngine : InputDisableMouse was set to:" + str(InputDisableMouse))

            # -- Ignore all SDL Parameters -- #
            elif SplitedParms[0] == "IgnoreSDL2Parameters":
                if SplitedParms[1].rstrip() == "True":
                    IgnoreSDL2Parameters = True
                elif SplitedParms[1].rstrip() == "False":
                    IgnoreSDL2Parameters = False
                else:
                    IgnoreSDL2Parameters = False

                print("Taiyou.Runtime.InitEngine : IgnoreSDL2Parameters was set to:" + str(IgnoreSDL2Parameters))

            # -- Image: SmoothScaleBackend Backend -- #
            elif SplitedParms[0] == "SmoothScaleBackend":
                SmoothScaleTransform = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : SmoothScaleBackend was set to:" + str(SmoothScaleTransform))

            # -- Pygame: FastEvent -- #
            elif SplitedParms[0] == "FastEvent":
                if SplitedParms[1].rstrip() == "True":
                    PygameFastEvent = True
                elif SplitedParms[1].rstrip() == "False":
                    PygameFastEvent = False
                else:
                    PygameFastEvent = False

                print("Taiyou.Runtime.InitEngine : FastEvent was set to:" + str(PygameFastEvent))

            elif SplitedParms[0] == "ThrowException":
                if SplitedParms[1].rstrip() == "True":
                    ThrowException = True

                elif SplitedParms[1].rstrip() == "False":
                    ThrowException = False

                else:
                    ThrowException = False

                print("Taiyou.Runtime.InitEngine : ThrowException was set to:" + str(ThrowException))

    if not IgnoreSDL2Parameters:  # -- Set SDL2 Parameters (if enabled) -- #
        # -- Set the Enviroments Variables -- #
        os.environ['SDL_VIDEODRIVER'] = str(VideoDriver)  # -- Set the Video Driver
        os.environ['SDL_AUDIODRIVER'] = str(AudioDriver)  # -- Set the Audio Driver

        # -- Set Input Enviroments -- #
        os.environ['SDL_MOUSEDRV'] = str(InputMouseDriver)  # -- Set the Mouse Driver
        os.environ['SDL_NOMOUSE'] = str(InputDisableMouse)  # -- Set the Mouse Driver

        # -- Set X11 Environment -- #
        if VideoDriver == "x11":
            if VideoX11CenterWindow:
                os.environ['SDL_VIDEO_CENTERED'] = "1"  # -- Set the Centered Window

            if VideoX11DGAMouse:
                os.environ['SDL_VIDEO_X11_DGAMOUSE'] = "1"  # -- Set the DGA Mouse Parameter

            if VideoX11YUV_HWACCEL:
                os.environ['SDL_VIDEO_YUV_HWACCEL'] = "1"  # -- Set the YUV HWACCEL Parameter
        print("Taiyou.Runtime.InitEngine : SDL2 Parameters has been applyed")

    else:
        print("Taiyou.Runtime.InitEngine : SDL2 Parameters has been disabled")

    # -- Set SmoothScaleMethod -- #
    pygame.transform.set_smoothscale_backend(SmoothScaleTransform)

    # -- Initialize Pygame and Sound System -- #
    if cntMng.SoundDisabled:
        # -- Set some Variables -- #
        Frequency = int(AudioFrequency)
        Size = int(AudioSize)
        Channels = int(AudioChannels)
        BufferSize = int(AudioBufferSize)

        pygame.mixer.init(Frequency, Size, Channels, BufferSize)

        pygame.init()
    else:
        pygame.init()

    if not pygame.mixer.get_init() and Get_IsSoundEnabled():
        sound.DisableSoundSystem = True

    # -- Initialize FastEvent -- #
    pygame.fastevent.init()

    MAIN.SetDisplay()

    InitializeBootloader()

def InitializeBootloader():
    global TaiyouPath_CorrectSlash

    CurrentGame_Folder = "CoreFiles{0}System{0}Bootloader".format(TaiyouPath_CorrectSlash)
    MAIN.CreateProcess(CurrentGame_Folder, "bootloader")

def GetUserSelectedApplication():
    return open("Selected.txt", "r").read().rstrip().replace("/", TaiyouPath_CorrectSlash)

def GetAppDataFromAppName(AppName):
    Path = "{1}{0}".format(AppName, TaiyouPath_AppDataFolder)
    
    # Check if path exists
    if not utils.Directory_Exists(Path):
        utils.Directory_MakeDir(Path)

    return Path

    pass

def Get_MainGameModuleName(GameFolder):
    """
    Returns the Main Game Module Name.
    :param GameFolder:
    :return:
    """
    return "{0}{1}".format(GameFolder.replace(TaiyouPath_CorrectSlash, "."), ".MAIN")

# endregion
