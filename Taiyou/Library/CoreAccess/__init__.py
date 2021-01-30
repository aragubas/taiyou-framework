#!/usr/bin/python3.8
#   Copyright 2021 Aragubas
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
import traceback, importlib, sys, threading
from System import Core
from Library import CorePaths
from Library import CoreUtils as UTILS
from Library import CorePrimitives as Shape

# -- Global Variables -- #
ProcessAccess = list()
ProcessAccess_PID = list()
ProcessNextPID = -1

# -- Create Process Variables -- #
LastProcessWasErrorProcess = False
LastProcess = None

def CreateProcess(Path, ProcessName, pInitArgs=None):
    """
     Set the Application Object
    :param ApplicationFolder:Folder Path
    :return:
    """
    global ProcessNextPID
    global LastProcessWasErrorProcess
    global LastProcess

    print("CoreAccess.CreateProcess : Creating Process: [" + ProcessName + "]...")

    try:
        # Get Process Path
        Path = Path.replace("/", CorePaths.TaiyouPath_CorrectSlash)
        ProcessIndex = len(ProcessAccess_PID)
        ProcessNextPID += 1

        # Import Module
        Module = importlib.import_module(Core.Get_MainModuleName(Path))

        try:
            # Get Process Object from Module
            ProcessWax = Module.Process(ProcessNextPID, ProcessName, Core.Get_MainModuleName(Path), pInitArgs, ProcessIndex)

        except:
            # Unload Module
            del Module

            # Check if module is imported and remove it
            if Core.Get_MainModuleName(Path) in sys.modules:
                sys.modules.pop(Core.Get_MainModuleName(Path))
            UTILS.GarbageCollector_Collect()


        # Unload Module
        del Module

        # Check if module is imported and remove it
        if Core.Get_MainModuleName(Path) in sys.modules:
            sys.modules.pop(Core.Get_MainModuleName(Path))
        UTILS.GarbageCollector_Collect()


        # Start process thread with UpdateRequest Function
        Thread = threading.Thread(target=ProcessWax.UpdateRequest).start()

        # Set THIS_THREAD Variable to Process
        ProcessWax.THIS_THREAD = Thread

        print("CoreAccess.CreateProcess : Process created sucefully")
        # Return newly created process PID
        LastProcessWasErrorProcess = False
        LastProcess = None
        return ProcessNextPID

    except:
        print("CoreAccess.CreateProcess : Error while creating process.")
        print(traceback.format_exc())

        if not LastProcessWasErrorProcess:
            LastProcessWasErrorProcess = True

            try:
                LastProcess.KillProcess(False)

                LastProcess = None
            except:
                print("Core.Main.CreateProcess : Error while trying to kill process")

            CreateProcess("System{0}SystemApps{0}crash_dialog".format(CorePaths.TaiyouPath_CorrectSlash), "application_crash", (ProcessName, None, None, 1))

def GetProcesByPID(PID):
    try:
        return ProcessAccess[ProcessAccess_PID.index(PID)]

    except IndexError:
        raise Exception("Cannot find process with PID [{0}]".format(PID))

def SendSigKillToProcessByPID(PID):
    try:
        GetProcesByPID(PID).KillProcess(True)

    except ValueError:
        print("Process with PID {0} cannot be killed because it was already finished\nor it has been not registred to CoreAccess.".format(PID))


def KillProcessByPID(PID):
    global ProcessListChanged
    Index = GetProcessIndexByPID(PID)

    # Call SIG_KILL Function on Process
    ProcessAccess[ProcessAccess_PID.index(PID)].KillProcess(False)

    UTILS.GarbageCollector_Collect()

    print("Taiyou : Finished process index: " + str(Index))

    #ProcessListChanged = True

    ClearPreRendered()

def ClearPreRendered():
    Shape.ClearPreRendered_Rectangles()


def GetProcessIndexByPID(PID):
    try:
        return ProcessAccess_PID.index(PID)

    except ValueError:
        raise ModuleNotFoundError("The process {0} could not be found".format(PID))

def RegisterToCoreAccess(self):
    ProcessAccess.append(self)
    ProcessAccess_PID.append(self.PID)

def RemoveFromCoreAccess(process):
    try:
        Index = ProcessAccess_PID.index(process.PID)

        ProcessAccess.pop(Index)
        ProcessAccess_PID.pop(Index)
    except ValueError:
        print("Cannot remove process that doesn't exist.")
