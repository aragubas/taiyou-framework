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
import Core

# The main Entry Point
print("Taiyou Window Manager Manager (WMM) version " + Core.Get_WindowManagerManagerVersion())


def WindowManagerSignal(self, Signal):
    """
    Sends a signal to the TaskBar's Window Manager
    :param self:Process Objct
    :param Signal:Signal Table:
    SignalID          Description\n
    ########          #############\n
    0                 Force Focus on Window\n
    1                 Kill Process
    :return:
    """
    # Gain Focus
    OriginalDragValue = self.WINDOW_DRAG_ENABLED
    if Signal == 0:
        for process in Core.MAIN.ProcessList:
            process.APPLICATION_HAS_FOCUS = False
            process.WINDOW_DRAG_ENABLED = False

        # Make this application focused again
        self.APPLICATION_HAS_FOCUS = True
        self.WINDOW_DRAG_ENABLED = OriginalDragValue
        return

    if Signal == 1:
        Core.MAIN.KillProcessByPID(self.PID)
        return