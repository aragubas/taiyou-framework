#! /usr/bin/python3.8
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
import sys, os, sys, platform
print("Check for Taiyou Framework Instalation...")

if not os.path.exists("./Taiyou"):
    print("\n\nFatal Error!\nCannot find Taiyou Instalation Folder!\n\nExecution cannot complete.")
    sys.exit(1)

print("Adding Required Path for All Modules...")
if platform.system() == "Linux":
    sys.path.append("Taiyou/Applications/")
    sys.path.append("Taiyou/")
    
    print("Added linux compatible dir.")

if platform.system() == "Windows":
    sys.path.append("Taiyou\\Applications\\")
    sys.path.append("Taiyou")
    print("Added windows compatible dir.")

import System.Core as Core

# Start the Application Loop #
LoopEnabled = True
Core.MAIN.Initialize()

while Core.IsRunning:
    Core.MAIN.UpdateDisplayDevice()

print("\nSee you later!")

