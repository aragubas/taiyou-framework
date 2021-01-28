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
import System.Core as Core
import traceback

# The main Entry Point
print("Taiyou Window Manager Manager (WMM) version " + Core.Get_WindowManagerManagerVersion())

TaskBarUIProcessID = -1

def CallWindowManagerUI():
    try:
        process_obj = Core.ProcessAccess[TaskBarUIProcessID]

        process_obj.UI_Call_Request()
    except:
        print("Error while processing WindowManager call request.")

def GetWindowManager():
    return Core.ProcessAccess[TaskBarUIProcessID]


def WindowManagerSignal(self, Signal, Args=None):
    """
    Sends a signal to the TaskBar's Window Manager
    :param self:Process Object
    :param Signal:Signal Table:
    SignalID          Description\n
    ########          #############\n
    0                 Force Focus on Window\n
    1                 Kill Process\n
    2                 Play Notify Sound on Task Bar Graphical Interface\n
    3                 Disable GUI Task Manager\n
    4                 Enable GUI Task Manager\n
    5                 Disable Intro Sound Trigger\n
    :return:
    """
    global TaskBarUIProcessID

    try:
        if TaskBarUIProcessID == -1:
            raise Exception("Cant send signal to TaskBarGUI because it is not running.")

        print("WindowManagerManager : TaskBAR ProcessID {0}".format(TaskBarUIProcessID))

        if Signal == 0:
            OriginalDragValue = self.WINDOW_DRAG_ENABLED

            for process in Core.ProcessAccess:
                process.APPLICATION_HAS_FOCUS = False
                process.WINDOW_DRAG_ENABLED = False

            # Make this application focused again
            self.APPLICATION_HAS_FOCUS = True
            self.WINDOW_DRAG_ENABLED = OriginalDragValue
            return

        elif Signal == 1:
            Core.MAIN.KillProcessByPID(self.PID)
            return

        elif Signal == 2:
            Core.ProcessAccess[TaskBarUIProcessID].PlayNotifySound = True
            return

        elif Signal == 3:
            Core.ProcessAccess[TaskBarUIProcessID].GUI_ALLOW_TASKMANAGER = False
            return

        elif Signal == 4:
            Core.ProcessAccess[TaskBarUIProcessID].GUI_ALLOW_TASKMANAGER = True
            return

        elif Signal == 5:
            Core.ProcessAccess[TaskBarUIProcessID].WelcomeScreenAppered = True
            return
    except:
        print("Error while processing Window Manager Request")
        print(traceback.format_exc())
