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

# -- Modules Versions -- #
def Get_Version():
    return "4.2"

def Get_ShapeVersion():
    return "2.2"

def Get_AppDataVersion():
    return "1.2"

def Get_UtilsVersion():
    return "2.6"

def Get_TaiyouMainVersion():
    return "3.9"

def Get_ContentManagerVersion():
    return "3.9"

def Get_FXVersion():
    return "1.3"

def Get_BootloaderVersion():
    return "2.4"

def Get_MAINVersion():
    return "2.1"

def Get_WindowManagerManagerVersion():
    return "1.3"

# -- Calculate the Version of Taiyou Game Engine -- #
TaiyouGeneralVersion = float(Get_Version()) + float(Get_ShapeVersion()) + float(Get_AppDataVersion()) + float(Get_UtilsVersion()) + float(Get_TaiyouMainVersion()) + float(Get_ContentManagerVersion()) + float(Get_FXVersion()) + float(Get_BootloaderVersion()) + float(Get_MAINVersion()) + float(Get_WindowManagerManagerVersion())

# -- Print Runtime Version -- #
print("\nTaiyou General version " + str(TaiyouGeneralVersion))
print("\n")

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
AudioPlayblackChannels = 0
RunInFullScreen = False
InputMouseDriver = "fbcon"
InputDisableMouse = False
IgnoreSDL2Parameters = True
PygameFastEvent = True
SmoothScaleTransform = "MMX"
ThrowException = False

# -- Taiyou Paths -- #
TaiyouPath_SystemPath = ""
TaiyouPath_SystemRootPath = ""
TaiyouPath_AppDataFolder = ""
TaiyouPath_TaiyouConfigFile = ""
TaiyouPath_CorrectSlash = ""
TaiyouPath_RootDevice = ""
TaiyouPath_ApplicationsDataPath = ""
TaiyouPath_SystemDataPath = ""
TaiyouPath_UserPackpagesPath = ""
TaiyouPath_UserPath = ""
TaiyouPath_UserTempFolder = ""
TaiyouPath_ApplicationsFolder = ""
TaiyouPath_SystemApplicationsFolder = ""
TaiyouPath_ApplicationsDataFolder = ""
TaiyouPath_SystemApplicationsDataFolder = ""


LastException = "null"
CurrentPlatform = ""

# -- Global Variables -- #
ProcessAccess = list()
ProcessAccess_PID = list()

IsRunning = True

def Init():
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
    global TaiyouPath_RootDevice
    global TaiyouPath_ApplicationsDataPath
    global TaiyouPath_SystemDataPath
    global TaiyouPath_SystemRootPath
    global ThrowException
    global CurrentPlatform
    global AudioPlayblackChannels
    global TaiyouPath_UserPackpagesPath
    global TaiyouPath_UserPath
    global TaiyouPath_UserTempFolder
    global TaiyouPath_ApplicationsFolder
    global TaiyouPath_SystemApplicationsFolder
    global TaiyouPath_ApplicationsDataFolder
    global TaiyouPath_SystemApplicationsDataFolder

    # -- Set the Correct Slash Directory -- #
    CurrentPlatform = platform.system()

    if CurrentPlatform == "Linux":
        TaiyouPath_CorrectSlash = "/"
        TaiyouPath_RootDevice = "./Taiyou/"
        TaiyouPath_SystemPath = "{0}System/CoreFiles/".format(TaiyouPath_RootDevice)
        TaiyouPath_UserPath = "./Taiyou/User/{0}/".format(getpass.getuser())
        TaiyouPath_AppDataFolder = "{0}AppsData/".format(TaiyouPath_UserPath)
        TaiyouPath_UserPackpagesPath = TaiyouPath_UserPath + "Packpages/"
        TaiyouPath_UserTempFolder = TaiyouPath_UserPath + "Temporary/"
        TaiyouPath_ApplicationsDataPath = TaiyouPath_RootDevice + "Data/app/"
        TaiyouPath_SystemDataPath = TaiyouPath_RootDevice + "Data/system/"
        TaiyouPath_SystemRootPath = TaiyouPath_RootDevice + "System/"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemRootPath + "system.config"
        TaiyouPath_ApplicationsFolder = TaiyouPath_RootDevice + "Applications/"
        TaiyouPath_SystemApplicationsFolder = TaiyouPath_RootDevice + "System/SystemApps/"
        TaiyouPath_ApplicationsDataFolder = TaiyouPath_RootDevice + "Data/app/"
        TaiyouPath_SystemApplicationsDataFolder = TaiyouPath_RootDevice + "Data/system/"

    elif CurrentPlatform == "Windows":
        TaiyouPath_CorrectSlash = "\\"
        TaiyouPath_RootDevice = os.getcwd() + "\\Taiyou\\"
        TaiyouPath_SystemPath = "{0}System\\CoreFiles\\".format(TaiyouPath_RootDevice)
        TaiyouPath_UserPath = "Taiyou\\User\\{0}\\".format(getpass.getuser())
        TaiyouPath_AppDataFolder = "{0}AppsData\\".format(TaiyouPath_UserPath)
        TaiyouPath_UserPackpagesPath = TaiyouPath_UserPath + "Packpages\\"
        TaiyouPath_UserTempFolder = TaiyouPath_UserPath + "Temporary\\"
        TaiyouPath_ApplicationsDataPath = TaiyouPath_RootDevice + "Data\\app\\"
        TaiyouPath_SystemDataPath = TaiyouPath_RootDevice + "Data\\system\\"
        TaiyouPath_SystemRootPath = TaiyouPath_RootDevice + "System\\"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemRootPath + "system.config"
        TaiyouPath_ApplicationsFolder = TaiyouPath_RootDevice + "Applications/"
        TaiyouPath_SystemApplicationsFolder = TaiyouPath_RootDevice + "System\\SystemApps\\"
        TaiyouPath_ApplicationsDataFolder = TaiyouPath_RootDevice + "Data\\app\\"
        TaiyouPath_SystemApplicationsDataFolder = TaiyouPath_RootDevice + "Data\\system\\"

    # Create directory for User Paths
    Utils.Directory_MakeDir(TaiyouPath_UserPath)
    Utils.Directory_MakeDir(TaiyouPath_UserPackpagesPath)
    Utils.Directory_MakeDir(TaiyouPath_UserTempFolder)

    # -- Initialize Some Modules
    CntMng.InitModule()

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

                print("Taiyou.Runtime.Init : Disable font rendering set to:" + str(CONTENT_MANAGER.FontRenderingDisabled))

            # -- Disable Image Rendering -- #
            elif SplitedParms[0] == "DisableImageRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.ImageRenderingDisabled = True
                else:
                    CONTENT_MANAGER.ImageRenderingDisabled = False

                print("Taiyou.Runtime.Init : Disable sprite rendering set to:" + str(CONTENT_MANAGER.ImageRenderingDisabled))

            # -- Disable Rectangle Rendering -- #
            elif SplitedParms[0] == "DisableRectangleRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.RectangleRenderingDisabled = True
                else:
                    CONTENT_MANAGER.RectangleRenderingDisabled = False

                print("Taiyou.Runtime.Init : Disable rectangle rendering set to:" + str(CONTENT_MANAGER.RectangleRenderingDisabled))

            # -- Disable Image Transparency -- #
            elif SplitedParms[0] == "DisableImageTransparency":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.ImageTransparency = True
                else:
                    CONTENT_MANAGER.ImageTransparency = False

                print("Taiyou.Runtime.Init : Disable sound system set to:" + str(CONTENT_MANAGER.ImageTransparency))

            # -- Disable Sound System -- #
            elif SplitedParms[0] == "DisableSoundSystem":
                if SplitedParms[1].rstrip() == "True":
                    CntMng.DisableSoundSystem = True
                else:
                    CntMng.DisableSoundSystem = False

                print("Taiyou.Runtime.Init : Disable sound system set to:" + str(CntMng.DisableSoundSystem))

            # -- SDL Option: Video Driver -- #
            elif SplitedParms[0] == "VideoDriver":
                VideoDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.Init : Video Driver was set to:" + str(VideoDriver))

            # -- SDL Option: Audio Driver -- #
            elif SplitedParms[0] == "AudioDriver":
                AudioDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.Init : Audio Driver was set to:" + str(AudioDriver))

            # -- SoundSystem: Audio Device Frequency -- #
            elif SplitedParms[0] == "AudioFrequency":
                AudioFrequency = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.Init : Audio Frequency was set to:" + str(AudioFrequency))

            # -- SoundSystem: Audio Device Frame Size -- #
            elif SplitedParms[0] == "AudioSize":
                AudioSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.Init : Audio Size was set to:" + str(AudioSize))

            # -- SoundSystem: Audio Device Audio Channels -- #
            elif SplitedParms[0] == "AudioChannels":
                AudioChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.Init : Audio Channels was set to:" + str(AudioChannels))

            # -- SoundSystem: Audio Device Buffer Size -- #
            elif SplitedParms[0] == "AudioBufferSize":
                AudioBufferSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.Init : Audio Buffer Size was set to:" + str(AudioBufferSize))

            # -- Run in Fullscreen -- #
            elif SplitedParms[0] == "RunInFullScreen":
                if SplitedParms[1].rstrip() == "True":
                    RunInFullScreen = True
                elif SplitedParms[1].rstrip() == "False":
                    RunInFullScreen = False
                else:
                    RunInFullScreen = False

                print("Taiyou.Runtime.Init : Run in Fullscreen was set to:" + str(RunInFullScreen))

            # -- SDL Option: Center Window -- #
            elif SplitedParms[0] == "VideoX11_CenterWindow":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11CenterWindow = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11CenterWindow = False
                else:
                    VideoX11CenterWindow = False

                print("Taiyou.Runtime.Init : VideoX11CenterWindow was set to:" + str(VideoX11CenterWindow))

            # -- SDL Option: DGA Mouse -- #
            elif SplitedParms[0] == "VideoX11_DGAMouse":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11DGAMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11DGAMouse = False
                else:
                    VideoX11DGAMouse = False

                print("Taiyou.Runtime.Init : VideoX11DGAMouse was set to:" + str(VideoX11DGAMouse))

            # -- SDL Option: YUV Hardware Acelleration -- #
            elif SplitedParms[0] == "VideoX11_YUV_HWACCEL":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11YUV_HWACCEL = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11YUV_HWACCEL = False
                else:
                    VideoX11YUV_HWACCEL = False

                print("Taiyou.Runtime.Init : VideoX11YUV_HWACCEL was set to:" + str(VideoX11YUV_HWACCEL))

            # -- SDL Option: Mouse Driver -- #
            elif SplitedParms[0] == "InputMouseDriver":
                InputMouseDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.Init : InputMouseDriver was set to:" + str(InputMouseDriver))

            # -- SDL Option: Disable Mouse -- #
            elif SplitedParms[0] == "InputDisableMouse":
                if SplitedParms[1].rstrip() == "True":
                    InputDisableMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    InputDisableMouse = False
                else:
                    InputDisableMouse = False

                print("Taiyou.Runtime.Init : InputDisableMouse was set to:" + str(InputDisableMouse))

            # -- Ignore all SDL Parameters -- #
            elif SplitedParms[0] == "IgnoreSDL2Parameters":
                if SplitedParms[1].rstrip() == "True":
                    IgnoreSDL2Parameters = True
                elif SplitedParms[1].rstrip() == "False":
                    IgnoreSDL2Parameters = False
                else:
                    IgnoreSDL2Parameters = False

                print("Taiyou.Runtime.Init : IgnoreSDL2Parameters was set to:" + str(IgnoreSDL2Parameters))

            # -- Image: SmoothScaleBackend Backend -- #
            elif SplitedParms[0] == "SmoothScaleBackend":
                SmoothScaleTransform = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.Init : SmoothScaleBackend was set to:" + str(SmoothScaleTransform))

            # -- Pygame: FastEvent -- #
            elif SplitedParms[0] == "FastEvent":
                if SplitedParms[1].rstrip() == "True":
                    PygameFastEvent = True
                elif SplitedParms[1].rstrip() == "False":
                    PygameFastEvent = False
                else:
                    PygameFastEvent = False

                print("Taiyou.Runtime.Init : FastEvent was set to:" + str(PygameFastEvent))

            elif SplitedParms[0] == "ThrowException":
                if SplitedParms[1].rstrip() == "True":
                    ThrowException = True

                elif SplitedParms[1].rstrip() == "False":
                    ThrowException = False

                else:
                    ThrowException = False

                print("Taiyou.Runtime.Init : ThrowException was set to:" + str(ThrowException))

            elif SplitedParms[0] == "ScreenRes":
                ScreenResCode = SplitedParms[1].rstrip().split("x")

                try:
                    ResWidth = int(ScreenResCode[0])
                    ResHeight = int(ScreenResCode[1])

                except:
                    ResWidth = 790
                    ResHeight = 576

                # Minimun Screen Size
                if ResWidth < 790:
                    ResWidth = 790
                if ResHeight < 576:
                    ResHeight = 576

                MAIN.ScreenWidth = ResWidth
                MAIN.ScreenHeight = ResHeight

                print("Taiyou.Runtime.Init : ScreenResolution was set to:" + str(MAIN.ScreenWidth) + "x" + str(MAIN.ScreenHeight))

            elif SplitedParms[0] == "AudioPlaybackChannels":
                AudioPlayblackChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.Init : AudioPlaybackChannels was set to:" + str(AudioPlayblackChannels))

    # WORKAROUND : Fix bug to run at new Pygame 2.0
    os.environ["PYGAME_BLEND_ALPHA_SDL2"] = "1"

    if not IgnoreSDL2Parameters:  # -- Set SDL2 Parameters (if enabled) -- #
        if not CurrentPlatform == "Windows":        
            # -- Set the Enviroments Variables -- #
            os.environ['SDL_VIDEODRIVER'] = str(VideoDriver)  # -- Set the Video Driver
            os.environ['SDL_AUDIODRIVER'] = str(AudioDriver)  # -- Set the Audio Driver

            # -- Set Input Enviroments -- #
            os.environ['SDL_MOUSEDRV'] = str(InputMouseDriver)  # -- Set the Mouse Driver
            os.environ['SDL_NOMOUSE'] = str(InputDisableMouse)  # -- Set the Mouse Driver

            # -- Set X11 Environment Variables -- #
            if VideoDriver == "x11":
                if VideoX11CenterWindow:
                    os.environ['SDL_VIDEO_CENTERED'] = "1"  # -- Set the Centered Window

                if VideoX11DGAMouse:
                    os.environ['SDL_VIDEO_X11_DGAMOUSE'] = "1"  # -- Set the DGA Mouse Parameter

                if VideoX11YUV_HWACCEL:
                    os.environ['SDL_VIDEO_YUV_HWACCEL'] = "1"  # -- Set the YUV HWACCEL Parameter
                    
            print("Taiyou.Runtime.Init : SDL2 Parameters has been applyed")
            
        else:
            print("Taiyou.Runtime.Init : SDL2 Parameters will be not set because Windows does not support SDL2 Parameters.")
        
    else:
        print("Taiyou.Runtime.Init : SDL2 Parameters has been disabled")

    # -- Set SmoothScaleMethod -- #
    pygame.transform.set_smoothscale_backend(SmoothScaleTransform)

    # -- Initialize Pygame and Sound System -- #
    if not CntMng.DisableSoundSystem:
        InitSoundSystem()
        pygame.init()
    else:
        print("Initializing with no sound\nSoundSystem has been disabled.")
        pygame.init()

    if not pygame.mixer.get_init():
        print("SoundSystem has been not initialized properly, setting DisableSoundSystem do true.")
        CntMng.DisableSoundSystem = True

    # -- Initialize FastEvent -- #
    pygame.fastevent.init()

    MAIN.SetDisplay()

    InitializeBootloader()

def InitSoundSystem():
    global AudioFrequency
    global AudioSize
    global AudioChannels
    global AudioBufferSize
    global AudioPlayblackChannels

    print("Initializing SoundSystem...")
    if pygame.mixer.get_init():
        print("SoundSystem was already initialized, quitting soundsystem...")
        pygame.mixer.quit()

    # -- Set some Variables -- #
    Frequency = int(AudioFrequency)
    Size = int(AudioSize)
    Channels = int(AudioChannels)
    BufferSize = int(AudioBufferSize)

    pygame.mixer.init(Frequency, Size, Channels, BufferSize)
    pygame.mixer.set_num_channels(AudioPlayblackChannels)

    print("SoundSystem has been initialized.")

def InitializeBootloader():
    global TaiyouPath_CorrectSlash

    CurrentApp_Folder = "System{0}SystemApps{0}Bootloader".format(TaiyouPath_CorrectSlash)
    MAIN.CreateProcess(CurrentApp_Folder, "bootloader")

def GetUserSelectedApplication():
    global TaiyouPath_RootDevice
    global TaiyouPath_CorrectSlash
    Path = "{0}System{1}{2}".format(TaiyouPath_RootDevice, TaiyouPath_CorrectSlash, "Selected.txt")
    return open(Path, "r").read().rstrip().replace("/", TaiyouPath_CorrectSlash)

def GetAppDataFromAppName(AppName):
    Path = "{1}{0}".format(AppName, TaiyouPath_AppDataFolder)
    
    # Check if path exists
    if not Utils.Directory_Exists(Path):
        Utils.Directory_MakeDir(Path)

    return Path

def Get_MainModuleName(AppPath):
    """
    Returns the Main Game Module Name.
    :param GameFolder:
    :return:
    """
    return "{0}{1}".format(AppPath.replace(TaiyouPath_CorrectSlash, "."), ".MAIN")

# endregion

def RegisterToCoreAccess(self):
    ProcessAccess.append(self)
    ProcessAccess_PID.append(self.PID)


# -- Imports All Modules -- #
import os, pygame, platform, getpass
from System.Core import CONTENT_MANAGER as CntMng
from System.Core import APPDATA as AppData
from System.Core import FX as Fx
from System.Core import SHAPES as Shape
from System.Core import UTILS as Utils
from System.Core.UTILS import Convert as Convert
from System.Core.UTILS import CoreUtils as CoreUtils
from System.Core import WMM as wmm
from System.Core import MAIN
