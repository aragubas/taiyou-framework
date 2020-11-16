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
import Core as tge
from Core import APPDATA as reg
from Core import CONTENT_MANAGER as sprite
from Core import UTILS as Utils
import pygame, sys, importlib, marshal, multiprocessing
import traceback, threading
from datetime import datetime
from multiprocessing import Process
import gc

# The main Entry Point
print("Taiyou Main version " + tge.Get_TaiyouMainVersion())

# -- Variables -- #
clock = pygame.time.Clock()
FPS = 75
DISPLAY = pygame.display
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


# Delta Time
getTicksLastFrame = 0
deltaTime = 0

# Priority List
HigherPriorityProcess = list()
NormalPriorityProcess = list()
LowerPriorityProcess = list()


def Initialize():
    global DISPLAY
    global ScreenWidth
    global ScreenHeight
    global EngineInitialized
    print("TaiyouFramework.Initialize : Initializing Taiyou...")

    # -- Load Engine -- #
    tge.InitEngine()

    EngineInitialized = True
    print("TaiyouFramework.Initialize : Initialization complete.")


def ReceiveCommand(Command, Arguments=None):
    """
    Sends a command to the Game Engine
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

        elif Command == 2:   #-- Kill Game
            CommandWasValid = True
            IsSpecialEvent = True

            print("TaiyouFramework.ReceiveCommand : Killing Game Process")

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

def SetDisplay():
    global DISPLAY
    global ScreenWidth
    global ScreenHeight

    if not tge.RunInFullScreen:
        DISPLAY = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)

    else:
        DISPLAY = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN)

    pygame.display.set_caption("Taiyou Framework v" + Utils.FormatNumber(tge.TaiyouGeneralVersion))

def CreateProcess(Path, ProcessName, pInitArgs = None, pPriority=0):
    """
     Set the Game Object
    :param GameFolder:Folder Path
    :return:
    """
    global ProcessList
    global ProcessList_Names
    global DISPLAY
    global ProcessListChanged
    global ProcessNextPID

    print("TaiyouFramework.CreateProcess : Creating Process: [" + ProcessName + "]")

    Path = Path.replace("/", tge.TaiyouPath_CorrectSlash)
    ProcessIndex = len(ProcessList_Names)
    print("ProcessIndex: " + str(ProcessIndex))
    print("Path: " + Path)
    print("ProcessName: " + ProcessName)

    ProcessNextPID += 1

    ProcessList_Names.append(ProcessName)
    Module = importlib.import_module(tge.Get_MainGameModuleName(Path))
    ProcessList.append(Module.Process(ProcessNextPID, ProcessName, tge.Get_MainGameModuleName(Path), pInitArgs))
    ProcessList_PID.append(ProcessNextPID)

    importlib.reload(Module)
    del Module

    if tge.Get_MainGameModuleName(Path) in sys.modules:
        sys.modules.pop(tge.Get_MainGameModuleName(Path))
    Utils.GarbageCollector_Collect()

    # Inject Variables and Functions
    Index = ProcessList_PID.index(ProcessNextPID)
    ProcessList[Index].PROCESS_INDEX = ProcessIndex
    ProcessList[Index].WINDOW_DRAG_ENABLED = False
    ProcessList[Index].APPLICATION_HAS_FOCUS = True
    ProcessList[Index].EXECUTABLE_PATH = Path
    ProcessList[Index].PRIORITY = pPriority

    ProcessListChanged = True

    # Initialize
    try:
        # Intialize Process Code
        ProcessList[Index].Initialize()

    except Exception as ex:
        # Remove the last item from the lists
        print("TaiyouFramework.CreateProcess : Process: [" + ProcessName + "] thrown an error on while trying to initialize")

        del ProcessList[-1]
        del ProcessList_PID[-1]
        del ProcessList_Names[-1]
        Utils.GarbageCollector_Collect()

        raise ex

    print("TaiyouFramework.CreateProcess : Process: [" + ProcessName + "] created successfully.")

    return ProcessNextPID

def SendSigKillToProcessByPID(PID):
    ProcessList[PID].ReceiveSignal("SIG_KILL")

def KillProcessByPID(PID):
    global ProcessListChanged
    Index = GetProcessIndexByPID(PID)

    ProcessList.pop(Index)
    ProcessList_PID.pop(Index)
    ProcessList_Names.pop(Index)
    Utils.GarbageCollector_Collect()

    print("Taiyou : Finished process index: " + str(Index))

    ProcessListChanged = True

def GetProcessIndexByPID(PID):
    try:
        return ProcessList_PID.index(PID)

    except ValueError:
        raise ModuleNotFoundError("The process {0} could not be found".format(PID))

def UpdateProcessPriorityList():
    global HigherPriorityProcess
    global NormalPriorityProcess
    global LowerPriorityProcess

    HigherPriorityProcess.clear()
    NormalPriorityProcess.clear()
    LowerPriorityProcess.clear()

    for process in ProcessList:
        if process.PRIORITY == 1:
            HigherPriorityProcess.append(process)
        elif process.PRIORITY == 0:
            NormalPriorityProcess.append(process)

        elif process.PRIORITY == -1:
            LowerPriorityProcess.append(process)

        else:
            raise Exception("Invalid priority value: {0}".format(str(process.PRIORITY)))


def Run():
    global WorkObject
    global FPS
    global DISPLAY
    global deltaTime
    global getTicksLastFrame
    global ProcessListChanged
    global ProcessListChanged_Delay
    global SystemFault_Trigger
    global SystemFault_Traceback
    global SystemFault_ProcessObject
    global HigherPriorityProcess
    global NormalPriorityProcess
    global LowerPriorityProcess

    # -- Run the Update Code -- #
    if ProcessListChanged:
        UpdateProcessPriorityList()

    # Update high priority process
    for process in HigherPriorityProcess:
        try:
            process.Update()

        except Exception:
            UpdateProcess(process)

    # Limit the application to the designed FPS
    clock.tick(FPS)

    # Update Normal Priority process
    for process in NormalPriorityProcess:
        try:
            process.Update()

        except Exception:
            UpdateProcess(process)

    # Update Lower Priority process
    for process in LowerPriorityProcess:
        try:
            process.Update()

        except Exception:
            UpdateProcess(process)


    if ProcessListChanged_Delay:
        ProcessListChanged_Delay = False
        ProcessListChanged = False

    if ProcessListChanged:
        ProcessListChanged_Delay = True

def UpdateProcess(process):
    global SystemFault_Trigger
    global SystemFault_Traceback
    global SystemFault_ProcessObject

    SystemFault_Trigger = True
    SystemFault_Traceback = traceback.format_exc()
    SystemFault_ProcessObject = process
    print("TaiyouApplicationLoop : Process Error Detected\nin Process PID({0})".format(process.PID))
    print("Traceback:\n" + SystemFault_Traceback)

    # Call the Window Manager to Toggle the UI Mode
    tge.wmm.WindowManagerSignal(None, 4)
    tge.wmm.CallWindowManagerUI()

    # Kill the Process
    KillProcessByPID(process.PID)

    # Generate the Crash Log
    GenerateCrashLog()


def GenerateCrashLog():
    print("Generating crash log...")
    # Create the directory for the Crash Logs
    CrashLogsDir = "./Logs/".replace("/", tge.TaiyouPath_CorrectSlash)
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
    pygame.quit()
    sys.exit()
