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
import pygame
import System.Core as Core

class Process(Core.Process):
    def Initialize(self):
        self.Taks = list()
        self.TaksKey = list()
        self.TaksProcessAgrs = list()
        self.TaskExecutionCycle = False
        self.Timer = pygame.time.Clock()

    def RunScheduledTask(self, key):
        print("Running task {0}".format(key))
        Index = self.TaksKey.index(key)

        self.Taks[Index](self.TaksProcessAgrs[Index])

        del self.Taks[Index]
        del self.TaksKey[Index]
        del self.TaksProcessAgrs[Index]

    def Update(self):
        while self.Running:
            self.Timer.tick(100)
            if len(self.TaksKey) != 0:
                self.RunScheduledTask(self.TaksKey[0])

    def AddTask(self, function, key, process_args=()):
        self.Taks.append(function)
        self.TaksKey.append(key)
        self.TaksProcessAgrs.append(process_args)
