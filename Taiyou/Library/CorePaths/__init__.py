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

# -- Imports --
import System.Core as Core
import os, platform, getpass
from Library import CoreUtils

print("CorePaths version " + Core.Get_CorePathsVersion())

TaiyouPath_SystemPath = ""
TaiyouPath_SystemRootPath = ""
TaiyouPath_AppDataFolder = ""
TaiyouPath_CorrectSlash = ""
TaiyouPath_TaiyouConfigFile = ""
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
TaiyouPath_UserFilesFolder = ""

def CheckPaths():
    global TaiyouPath_CorrectSlash
    global TaiyouPath_SystemPath
    global TaiyouPath_TaiyouConfigFile
    global TaiyouPath_CorrectSlash
    global TaiyouPath_AppDataFolder
    global TaiyouPath_RootDevice
    global TaiyouPath_ApplicationsDataPath
    global TaiyouPath_SystemDataPath
    global TaiyouPath_SystemRootPath
    global TaiyouPath_UserPackpagesPath
    global TaiyouPath_UserPath
    global TaiyouPath_UserTempFolder
    global TaiyouPath_ApplicationsFolder
    global TaiyouPath_SystemApplicationsFolder
    global TaiyouPath_ApplicationsDataFolder
    global TaiyouPath_SystemApplicationsDataFolder
    global TaiyouPath_UserFilesFolder

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
        TaiyouPath_UserFilesFolder = TaiyouPath_UserPath + "UserFiles/"

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
        TaiyouPath_ApplicationsFolder = TaiyouPath_RootDevice + "Applications\\"
        TaiyouPath_SystemApplicationsFolder = TaiyouPath_RootDevice + "System\\SystemApps\\"
        TaiyouPath_ApplicationsDataFolder = TaiyouPath_RootDevice + "Data\\app\\"
        TaiyouPath_SystemApplicationsDataFolder = TaiyouPath_RootDevice + "Data\\system\\"
        TaiyouPath_UserFilesFolder = TaiyouPath_UserPath + "UserFiles\\"

    # Creates user folder
    CoreUtils.Directory_MakeDir(TaiyouPath_UserTempFolder)
    CoreUtils.Directory_MakeDir(TaiyouPath_UserPackpagesPath)
    CoreUtils.Directory_MakeDir(TaiyouPath_UserFilesFolder)


# -- Read App Data Functions -- #
def GetAppDataFromAppName(AppName):
    Path = "{1}{0}".format(AppName, TaiyouPath_AppDataFolder)

    # Check if path exists
    if not CoreUtils.Directory_Exists(Path):
        CoreUtils.Directory_MakeDir(Path)

    return Path
