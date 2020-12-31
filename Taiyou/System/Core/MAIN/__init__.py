#! /usr/bin/python3.7
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

# Import some stuff
import os
import System.Core as Core
from System.Core import APPDATA as reg
from System.Core import CONTENT_MANAGER as sprite
from System.Core import UTILS as Utils
import pygame, sys, importlib, multiprocessing, traceback, threading, time
from datetime import datetime
from multiprocessing import Process
import gc

# The main Entry Point
print("Taiyou Main version " + Core.Get_TaiyouMainVersion())

# -- Variables -- #
FPS = 75
ScreenWidth = 1024
ScreenHeight = 720
WorkObject = None
InitDelay_Delta = 0
InitDelay_Enabled = True
EngineInitialized = False
ErrorScreenInitialzed = False
ThrowException = True
ProcessListChanged = False
ProcessListChanged_Delay = False
ProcessList = list()
ProcessList_Names = list()
ProcessList_PID = list()
ProcessNextPID = -1
SystemFault_Trigger = False
SystemFault_Traceback = ""
SystemFault_ProcessObject = None
timer = pygame.time.Clock()

# Delta Time
getTicksLastFrame = 0
deltaTime = 0

DISPLAY = False


def Initialize():
    global DISPLAY
    global ScreenWidth
    global ScreenHeight
    global EngineInitialized
    print("TaiyouFramework.Initialize : Initializing Taiyou...")

    # -- Load Engine -- #
    Core.Init()

    EngineInitialized = True
    print("TaiyouFramework.Initialize : Initialization complete.")


def ReceiveCommand(Command, Arguments=None):
    """
    Sends a command to the Application Engine
    \n
    Command:                   Argument\n
    0 - Set FPS:                Integer\n
    1 - Set Resolution:         [Width]x[Height]\n
    2 - KILL:                   None\n
    3 - OverlayLevel:           Integer\n
    4 - Set Icon:               String [Image Name loaded on Image System]\n
    5 - Cursor Visible:         Boolean\n
    :param Command:CommandCode
    :param Arguments:Argument of Specified Command
    :return:
    """
    global DISPLAY
    global FPS
    global ScreenWidth
    global ScreenHeight

    CommandWasValid = False
    IsSpecialEvent = False

    try:
        if Command == 0:  # -- Set FPS
            CommandWasValid = True
            IsSpecialEvent = True

            FPS = int(Arguments)

            print("TaiyouFramework.ReceiveCommand : MaxFPS Set to:" + str(FPS))

        elif Command == 1:  # -- Set Resolution
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Arguments.split('x')
            print("TaiyouFramework.ReceiveCommand : Set Resolution to: {0}x{1}".format(str(splitedArg[0]), str(splitedArg[1])))

            ScreenWidth = int(splitedArg[0])
            ScreenHeight = int(splitedArg[1])

            SetDisplay()

        elif Command == 2:   #-- Kill Application
            CommandWasValid = True
            IsSpecialEvent = True

            print("TaiyouFramework.ReceiveCommand : Killing Application Process")

            Destroy()

        elif Command == 3:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = int(Arguments)

            ovelMng.Set_OverlayLevel(int(splitedArg[1]))

            print("TaiyouFramework.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

        elif Command == 4:
            CommandWasValid = True
            IsSpecialEvent = True

            pygame.display.set_icon(CONTENT_MANAGER.GetImage(Arguments))

            print("TaiyouFramework.ReceiveCommand : Set Icon to " + str(Arguments))

        elif Command == 5:
            CommandWasValid = True
            IsSpecialEvent = True

            pygame.mouse.set_visible(Arguments)

            print("TaiyouFramework.ReceiveCommand : Set CURSOR_VISIBLE to " + str(Arguments))

        if not CommandWasValid:
            Txt = "TaiyouMessage: Invalid Command:\n'{0}'".format(Command)
            print(Txt)
        elif IsSpecialEvent:
            Txt = "TaiyouMessage: Command Processed:\n'{0}' with Argument: '{1}'".format(Command, Arguments)
            print(Txt)

    except IndexError:
        Txt = "TaiyouMessage EXCEPTION\nThe Command {0}\ndoes not have the necessary number of arguments.".format(str(Command))
        print(Txt)

def CreateProcess(Path, ProcessName, pInitArgs=None):
    """
     Set the Application Object
    :param ApplicationFolder:Folder Path
    :return:
    """
    global ProcessList
    global ProcessList_Names
    global ProcessList_PID
    global DISPLAY
    global ProcessListChanged
    global ProcessNextPID

    print("TaiyouFramework.CreateProcess : Creating Process: [" + ProcessName + "]")

    Path = Path.replace("/", Core.TaiyouPath_CorrectSlash)
    ProcessIndex = len(ProcessList_Names)
    ProcessNextPID += 1

    print("ProcessIndex: " + str(ProcessIndex))
    print("Path: " + Path)
    print("ProcessName: " + ProcessName)
    print("ProcessPID : " + str(ProcessNextPID))

    Module = importlib.import_module(Core.Get_MainModuleName(Path))

    ProcessWax = Module.Process(ProcessNextPID, ProcessName, Core.Get_MainModuleName(Path), pInitArgs, ProcessIndex)

    importlib.reload(Module)
    del Module

    if Core.Get_MainModuleName(Path) in sys.modules:
        sys.modules.pop(Core.Get_MainModuleName(Path))
    Utils.GarbageCollector_Collect()

    Thread = threading.Thread(target=ProcessWax.Update).start()

    ProcessList.append(Thread)
    ProcessList_PID.append(ProcessNextPID)
    ProcessList_Names.append(ProcessName)

    ProcessWax.THIS_THREAD = Thread

    return ProcessNextPID

def SendSigKillToProcessByPID(PID):
    ProcessList[PID].ReceiveSignal("SIG_KILL")

def KillProcessByPID(PID):
    global ProcessListChanged
    Index = GetProcessIndexByPID(PID)

    # Call SIG_KILL Function on Process
    Core.ProcessAccess[Core.ProcessAccess_PID.index(PID)].Running = False
    if hasattr(Core.ProcessAccess[Core.ProcessAccess_PID.index(PID)], "KillProcess"):
        Core.ProcessAccess[Core.ProcessAccess_PID.index(PID)].KillProcess()

    # Remove Thread Object
    del Core.ProcessAccess[Core.ProcessAccess_PID.index(PID)].THIS_THREAD

    # Delete from CoreAcess
    index = Core.ProcessAccess_PID.index(PID)
    Core.ProcessAccess.pop(index)
    Core.ProcessAccess_PID.pop(index)

    # Remove from Process List
    ProcessList.pop(Index)
    ProcessList_PID.pop(Index)
    ProcessList_Names.pop(Index)
    Utils.GarbageCollector_Collect()

    print("Taiyou : Finished process index: " + str(Index))

    ProcessListChanged = True

    ClearPreRendered()

def ClearPreRendered():
    Core.Shape.ClearPreRendered_Rectangles()


def GetProcessIndexByPID(PID):
    try:
        return Core.ProcessAccess_PID.index(PID)

    except ValueError:
        raise ModuleNotFoundError("The process {0} could not be found".format(PID))

def GenerateCrashLog():
    print("Generating crash log...")
    # Create the directory for the Crash Logs
    CrashLogsDir = "./Logs/".replace("/", Core.TaiyouPath_CorrectSlash)
    Utils.Directory_MakeDir(CrashLogsDir)

    try:
        FilePath = CrashLogsDir + SystemFault_ProcessObject.NAME + ".txt"
    except:
        FilePath = CrashLogsDir + "unknow_process_name.txt"

    ProcessInformation = " --- PROCESS INFORMATION ---\n"

    ProcessInformation += "Name:"
    try:
        ProcessInformation += SystemFault_ProcessObject.NAME + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "PID:"
    try:
        ProcessInformation += SystemFault_ProcessObject.PID + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "ModulePath:"
    try:
        ProcessInformation += SystemFault_ProcessObject.ROOT_MODULE + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "IsFullscreen:"
    try:
        ProcessInformation += SystemFault_ProcessObject.FULLSCREEN + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "HasFocus:"
    try:
        ProcessInformation += SystemFault_ProcessObject.APPLICATION_HAS_FOCUS + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "TitlebarText:"
    try:
        ProcessInformation += SystemFault_ProcessObject.TITLEBAR_TEXT + "\n"
    except:
        ProcessInformation += "Error while parsing\n"

    ProcessInformation += "\nAny field with 'Error while parsing' was because the process does not actualy have the variable\n\n --- ERROR TRACEBACK ---"

    FileWrite = open(FilePath, "w")
    FileWrite.write(ProcessInformation)
    FileWrite.write(SystemFault_Traceback)
    FileWrite.close()

    print("Crash log completed")


def Destroy():
    Core.IsRunning = False
    pygame.quit()
    sys.exit()

DrawingCode = None
EventUpdateCode = None
CeiraDeFPS = Utils.FPS()

def UpdateDisplayDevice():
    global DrawingCode
    global timer
    global EventUpdateCode

    timer.tick(Core.MainLoopRefreshRate)

    if DrawingCode is not None:
        DrawingCode()

    if EventUpdateCode is not None:
        if not pygame.fastevent.get_init():
            return
            
        else:
            EventUpdateCode()

    pygame.display.flip()

def SetDisplay():
    global DISPLAY
    if not Core.RunInFullScreen:
        DISPLAY = pygame.display.set_mode((Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)

    else:
        DISPLAY = pygame.display.set_mode((Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN)

    pygame.display.set_caption("Taiyou Framework v" + Utils.FormatNumber(Core.TaiyouGeneralVersion))
