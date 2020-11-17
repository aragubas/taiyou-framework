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

class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = False
        self.INIT_ARGS = pInitArgs

        self.Taks = list()
        self.TaksKey = list()
        self.TaksProcessAgrs = list()
        self.TaskExecutionCycle = False

    def Initialize(self):
        pass

    def RunScheduledTask(self, key):
        print("Running task {0}".format(key))
        Index = self.TaksKey.index(key)

        self.Taks[Index](self.TaksProcessAgrs[Index])

        del self.Taks[Index]
        del self.TaksKey[Index]
        del self.TaksProcessAgrs[Index]

    def Update(self):
        if len(self.TaksKey) != 0:
            self.RunScheduledTask(self.TaksKey[0])

    def AddTask(self, function, key, process_args=()):
        self.Taks.append(function)
        self.TaksKey.append(key)
        self.TaksProcessAgrs.append(process_args)
