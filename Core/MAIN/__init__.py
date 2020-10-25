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
from Core import UTILS as utils
import pygame, sys, importlib, marshal
import traceback, threading
from datetime import datetime
from multiprocessing import Process
import gc

# The main Entry Point
print("Taiyou Main version " + tge.Get_TaiyouMainVersion())

# -- Variables -- #
clock = pygame.time.Clock()
FPS = 70
DISPLAY = pygame.display
CurrentRes_W = 800
CurrentRes_H = 600
WindowTitle = "Taiyou Game Engine v{0}".format(utils.FormatNumber(tge.TaiyouGeneralVersion))
WorkObject = None
InitDelay_Delta = 0
InitDelay_Enabled = True
EngineInitialized = False
ErrorScreenInitialzed = False
ThrowException = True
ProcessList = list()
ProcessList_Names = list()
ProcessList_PID = list()

# Delta Time
getTicksLastFrame = 0
deltaTime = 0

def Initialize():
    global DISPLAY
    global CurrentRes_W
    global CurrentRes_H
    global EngineInitialized
    print("Taiyou.GameExecution.Initialize : Initializing Taiyou...")

    # -- Load Engine -- #
    tge.InitEngine()

    EngineInitialized = True
    print("Taiyou.GameExecution.Initialize : Initialization complete.")


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
    5 - Set Title:              String\n
    6 - Cursor Visible:         Boolean\n
    :param Command:CommandCode
    :param Arguments:Argument of Specified Command
    :return:
    """
    global DISPLAY
    global FPS
    global CurrentRes_W
    global CurrentRes_H

    CommandWasValid = False
    IsSpecialEvent = False

    try:
        if Command == 0:  # -- Set FPS
            CommandWasValid = True
            IsSpecialEvent = True

            FPS = int(Arguments)

            print("Taiyou.GameExecution.ReceiveCommand : MaxFPS Set to:" + str(FPS))

        elif Command == 1:  # -- Set Resolution
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Arguments.split('x')
            print("Taiyou.GameExecution.ReceiveCommand : Set Resolution to: {0}x{1}".format(str(splitedArg[0]), str(splitedArg[1])))

            CurrentRes_W = int(splitedArg[0])
            CurrentRes_H = int(splitedArg[1])

            SetDisplay()

        elif Command == 2:   #-- Kill Game
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Killing Game Process")

            Destroy()

        elif Command == 3:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = int(Arguments)

            ovelMng.Set_OverlayLevel(int(splitedArg[1]))

            print("Taiyou.GameExecution.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

        elif Command == 4:
            CommandWasValid = True
            IsSpecialEvent = True

            pygame.display.set_icon(CONTENT_MANAGER.GetImage(Arguments))

            print("Taiyou.GameExecution.ReceiveCommand : Set Icon to " + str(Arguments))

        elif Command == 5:
            CommandWasValid = True

            pygame.display.set_caption(Arguments)

        elif Command == 6:
            CommandWasValid = True
            IsSpecialEvent = True

            pygame.mouse.set_visible(Arguments)

            print("Taiyou.GameExecution.ReceiveCommand : Set CURSOR_VISIBLE to " + str(Arguments))

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
    global CurrentRes_W
    global CurrentRes_H

    if not tge.RunInFullScreen:
        DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)

    else:
        DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN)

    pygame.display.set_caption("Taiyou Framework v" + str(tge.TaiyouGeneralVersion))

def CreateProcess(Path, ProcessName):
    """
     Set the Game Object
    :param GameFolder:Folder Path
    :return:
    """
    global ProcessList
    global ProcessList_Names
    global DISPLAY

    print("Taiyou.GameExecution.CreateProcess : Loading Process: [" + ProcessName + "]")

    Path = Path.replace("/", tge.TaiyouPath_CorrectSlash)
    PID = len(ProcessList_Names)
    ProcessList_Names.append("{0}:{1}".format(ProcessName, PID))
    ProcessList.append(importlib.import_module(tge.Get_MainGameModuleName(Path)))
    ProcessList_PID.append(PID)

    ProcessList[PID].Initialize()
    ProcessList[PID].PROCESS_PID = PID
    ProcessList[PID].PROCESS_NAME = ProcessName

def SendSigKillToProcessByPID(PID):
    ProcessList[PID].SendSignal(SIG_KILL)

def KillProcessByPID(PID):
    del ProcessList[PID]
    del ProcessList_PID[PID]
    del ProcessList_Names[PID]

def Run():
    global WorkObject
    global FPS
    global DISPLAY
    global deltaTime
    global getTicksLastFrame

    # -- Run the Update Code -- #
    for process in ProcessList:
        process.Update()

    # deltaTime in seconds.
    deltaTime = clock.tick()

def Destroy():
    pygame.quit()
    sys.exit()
