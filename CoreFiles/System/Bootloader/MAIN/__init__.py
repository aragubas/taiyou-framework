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
import Core, traceback, pygame, time
from Core import Shape
from Core import Utils

class ApplicationSelector:
    def __init__(self, pContentManager, pX, pY):
        self.X = pX
        self.Y = pY
        self.Width = 550
        self.Height = 120
        self.Content = pContentManager
        self.ObjectSurface = pygame.Surface((self.Width, self.Height), pygame.SRCALPHA)
        self.SeletorItems_Title = list()
        self.SeletorItems_Index = list()
        self.SeletorItems_Icon = list()
        self.SeletorItems_ModulePath = list()

        self.SelectedItemIndex = -1
        self.SelectedItemTitle = ""
        self.SelectedItemModulePath = None

        self.HScroll = 10

    def Draw(self, Surface):
        self.ObjectSurface.fill((0, 0, 0, 0))

        Shape.Shape_Rectangle(self.ObjectSurface, (0, 0, 0, 150), (0, 0, self.Width, self.Height), 0, 5)

        index = -1
        for item in self.SeletorItems_Index:
            index += 1
            ItemRect = pygame.Rect(self.HScroll + 105 * index, 5, 100, self.Height - 10)
            ItemPicBox = pygame.Rect(ItemRect[0] + 2, ItemRect[1] + 4, ItemRect[2] - 4, ItemRect[3] - 8)

            if self.SelectedItemIndex == index:
                Shape.Shape_Rectangle(self.ObjectSurface, (255, 255, 255, 150), ItemRect, 0, 2)

            if self.SeletorItems_Icon[index] == None:
                self.Content.ImageRender(self.ObjectSurface, "/folder_question.png", ItemPicBox[0], ItemPicBox[1], ItemPicBox[2], ItemPicBox[3], SmoothScaling=True)
            else:
                self.Content.ImageRender(self.ObjectSurface, self.SeletorItems_Icon[index], ItemPicBox[0], ItemPicBox[1], ItemPicBox[2], ItemPicBox[3], SmoothScaling=True, ImageNotLoaded=True)

        Surface.blit(self.ObjectSurface, (self.X, self.Y))

    def AddItem(self, Title, pModulePath, IconPath="None"):
        self.SeletorItems_Title.append(Title.rstrip())
        self.SeletorItems_Index.append(len(self.SeletorItems_Title))
        self.SeletorItems_ModulePath.append(pModulePath)
        if IconPath == "None":
            self.SeletorItems_Icon.append(None)
        else:
            self.SeletorItems_Icon.append(self.Content.ReturnImageObject(IconPath, True))

    def EventUpdate(self, event):
        ThisRect = pygame.Rect(self.X, self.Y, self.Width, self.Height)

        if ThisRect.collidepoint(pygame.mouse.get_pos()):
            index = -1
            SelectedItems = 0
            for item in self.SeletorItems_Title:
                index += 1
                ItemRect = pygame.Rect(self.X + self.HScroll + 105 * index, 5, 100, self.Y + self.Height - 10)

                if ItemRect.collidepoint(pygame.mouse.get_pos()):
                    SelectedItems += 1
                    self.SelectedItemIndex = index
                    self.SelectedItemTitle = item
                    self.SelectedItemModulePath = self.SeletorItems_ModulePath[index]

            if SelectedItems == 0:
                self.SelectedItemIndex = -1
                self.SelectedItemTitle = ""
                self.SelectedItemModulePath = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.HScroll -= 5

            if event.button == 5:
                self.HScroll += 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_HOME:
                self.HScroll = 10

def ListInstalledApplications(BootFolders, ApplicationSelector):
    for boot in BootFolders:
        ReadData = open(boot, "r").readlines()

        AppTitle = None
        IconPath = None
        ModulePath = None

        for Data in ReadData:
            Data = Data.rstrip().lstrip()
            if Data.startswith("#"):
                continue

            Splited = Data.split(":")

            if Splited[0] == "title":
                AppTitle = Splited[1]

            if Splited[0] == "icon_path":
                IconPath = Splited[1]

            if Splited[0] == "folder":
                ModulePath = Splited[1]

        if AppTitle is None or IconPath is None or ModulePath is None:
            continue

        ApplicationSelector.AddItem(AppTitle, ModulePath, IconPath)


class Process():
    def __init__(self, pPID, pProcessName, pROOT_MODULE, pInitArgs):
        self.PID = pPID
        self.NAME = pProcessName
        self.INIT_ARGS = pInitArgs
        self.ROOT_MODULE = pROOT_MODULE
        self.IS_GRAPHICAL = True
        self.DISPLAY = pygame.Surface((Core.MAIN.ScreenWidth, Core.MAIN.ScreenHeight))
        self.LAST_SURFACE = self.DISPLAY.copy()
        self.APPLICATION_HAS_FOCUS = True
        self.POSITION = (0, 0)
        self.FULLSCREEN = True
        self.TITLEBAR_RECTANGLE = pygame.Rect(self.POSITION[0], self.POSITION[1], self.DISPLAY.get_width(), self.DISPLAY.get_height())
        self.TITLEBAR_TEXT = "Taiyou System Loader"

    def Initialize(self):
        self.DefaultContent = Core.CntMng.ContentManager()

        self.DefaultContent.SetSourceFolder("CoreFiles/res/")
        self.DefaultContent.SetFontPath("fonts")
        self.DefaultContent.SetImageFolder("img")
        self.DefaultContent.SetRegKeysPath("reg/BOOTLOADER")
        self.DefaultContent.SetSoundPath("sound")
        self.DefaultContent.SetFontPath("fonts")

        self.DefaultContent.InitSoundSystem()

        self.DefaultContent.LoadRegKeysInFolder()
        self.DefaultContent.LoadImagesInFolder()
        self.DefaultContent.LoadSoundsInFolder()

        self.Progress = 0
        self.ProgressAddDelay = 0
        self.ProgressProgression = True
        self.ProgressMax = 100
        self.LoadingComplete = False
        self.InitialLoadingDelay = 0

        self.CenterX = self.DISPLAY.get_width() / 2
        self.CenterY = self.DISPLAY.get_height() / 2

        self.ApplicationSeletor = False
        self.ApplicationSeletorAnimatorStart = Core.Utils.AnimationController(0.5, multiplierRestart=True)
        self.ApplicationSelectorObj = ApplicationSelector(self.DefaultContent, self.CenterX - 550 / 2, self.CenterY - 120 / 2)

        self.NoFoldersFound = False
        self.FatalErrorScreen = False

        self.ApplicationSeletorWelcomeSound = False

        # List all valid folders
        folder_list = Core.Utils.Directory_FilesList("." + Core.TaiyouPath_CorrectSlash)
        BootFolders = list()
        for file in folder_list:
            if file.endswith(Core.TaiyouPath_CorrectSlash + "boot"):
                BootFolders.append(file)

        ListInstalledApplications(BootFolders, self.ApplicationSelectorObj)

        if len(BootFolders) == 0 or len(self.ApplicationSelectorObj.SeletorItems_Index) == 0:
            self.NoFoldersFound = True

        self.InitialSignal = False

    def Update(self):
        if self.ApplicationSeletor:
            self.ApplicationSeletorAnimatorStart.Update()

            if self.ApplicationSeletorAnimatorStart.Value <= 10 and not self.FatalErrorScreen:
                self.ApplicationSeletorAnimatorStart.Enabled = True

            if not self.ApplicationSeletorWelcomeSound and not self.FatalErrorScreen:
                self.ApplicationSeletorWelcomeSound = True

                self.DefaultContent.PlaySound("/intro.wav")
                Core.wmm.WindowManagerSignal(None, 5)
            return

        if self.ProgressProgression and not self.LoadingComplete:
            self.ProgressAddDelay += 1

            if self.ProgressAddDelay == 5:
                self.ProgressAddDelay = 0
                self.Progress += 1

            if self.ProgressAddDelay == 1:
                self.LoadingSteps(self.Progress)

            if self.Progress >= self.ProgressMax and not self.LoadingComplete:
                self.LoadingComplete = True

                print("Bootloader : Loading Complete")

                # Start the Default Application
                try:
                    # Create the Application Process
                    Core.MAIN.CreateProcess(Core.GetUserSelectedApplication(), Core.GetUserSelectedApplication())

                    # Allow Window Manager do receive request
                    Core.wmm.WindowManagerSignal(None, 4)

                    # Kills the Bootloader process
                    Core.MAIN.KillProcessByPID(self.PID)

                except Exception:
                    print("Fatal Error : Error while creating the process to the Auto-Start Application.")

                    Traceback = traceback.format_exc()

                    # Check if SelectedFile wax exists

                    try:
                        UserSelectedApplication = Core.GetUserSelectedApplication()

                        self.GenerateCrashLog(Traceback, UserSelectedApplication)
                        print(Traceback)
                        print("Something bad happened while creating the process for the default application.")

                        self.FatalErrorScreen = False
                        self.ApplicationSeletor = True
                        self.APPLICATION_HAS_FOCUS = True

                    except:
                        print("Selected application file is not readable.")
                        self.ApplicationSeletor = True
                        self.APPLICATION_HAS_FOCUS = True

    def Draw(self):
        if not self.InitialSignal:
            self.InitialSignal = True

            # Disable Window manager Requests
            Core.wmm.WindowManagerSignal(None, 3)

        # Fill the screen
        self.DISPLAY.fill((18, 10, 38))

        if not self.ApplicationSeletor:
            self.DrawLoadingPart()

        else:
            self.DrawApplicationSelector()

        self.LAST_SURFACE = self.DISPLAY.copy()
        return self.DISPLAY

    def DrawApplicationSelector(self):
        DisplayWithOpacity = self.DISPLAY.copy()
        DisplayWithOpacity.set_alpha(self.ApplicationSeletorAnimatorStart.Value)

        if not self.NoFoldersFound and not self.FatalErrorScreen:
            self.ApplicationSelectorObj.Draw(DisplayWithOpacity)

            # Draw the Selected Application Title
            TitleBarText = self.ApplicationSelectorObj.SelectedItemTitle.rstrip()
            FontSize = 34
            Font = "/UbuntuMono.ttf"
            TextColor = (250, 250, 250)
            self.DefaultContent.FontRender(DisplayWithOpacity, Font, FontSize, TitleBarText, TextColor, self.CenterX - self.DefaultContent.GetFont_width(Font, FontSize, TitleBarText) / 2, self.CenterY - 120)

            # Draw the Select the Enter
            Text = self.DefaultContent.Get_RegKey("/seletor/down_text")
            FontSize = 12
            Font = "/Ubuntu.ttf"
            TextColor = (150, 150, 150)
            self.DefaultContent.FontRender(DisplayWithOpacity, Font, FontSize, Text, TextColor, self.CenterX - self.DefaultContent.GetFont_width(Font, FontSize, Text) / 2, self.CenterY + 250)

        elif not self.FatalErrorScreen:
            self.ApplicationSeletorAnimatorStart.Enabled = True
            self.ApplicationSeletorAnimatorStart.ValueMultiplierSpeed = 0.05
            self.DefaultContent.ImageRender(DisplayWithOpacity, "/folder_question.png", self.CenterX - 186 / 2, self.CenterY - 186 / 2, 186, 186, SmoothScaling=True)

            # Draw the Select the Enter
            Text = self.DefaultContent.Get_RegKey("/seletor/no_folders_found_down_text")
            FontSize = 12
            Font = "/Ubuntu.ttf"
            TextColor = (150, 150, 150)
            self.DefaultContent.FontRender(self.DISPLAY, Font, FontSize, Text, TextColor, self.CenterX - self.DefaultContent.GetFont_width(Font, FontSize, Text) / 2, self.CenterY + 250)

        else:
            self.ApplicationSeletorAnimatorStart.Enabled = True
            self.ApplicationSeletorAnimatorStart.ValueMultiplierSpeed = 0.2
            self.DefaultContent.ImageRender(DisplayWithOpacity, "/error.png", self.CenterX - 186 / 2, self.CenterY - 186 / 2, 186, 186, SmoothScaling=True)

            # Draw the Select the Enter
            Text = self.DefaultContent.Get_RegKey("/seletor/fatal_error_down_text")
            FontSize = 12
            Font = "/Ubuntu.ttf"
            TextColor = (150, 150, 150)
            self.DefaultContent.FontRender(self.DISPLAY, Font, FontSize, Text, TextColor, self.CenterX - self.DefaultContent.GetFont_width(Font, FontSize, Text) / 2, self.CenterY + 250)

        self.DISPLAY.blit(DisplayWithOpacity, (0, 0))

    def DrawLoadingPart(self):
        self.DrawProgressBar(self.DISPLAY)

        # Draw the Logo
        LogoPos = (self.CenterX - 231 / 2, self.CenterY - 242, 231, 242)

        self.DefaultContent.ImageRender(self.DISPLAY, "/framework_logo.png", LogoPos[0], LogoPos[1], LogoPos[2], LogoPos[3])

    def DrawProgressBar(self, DISPLAY):
        self.LoadingBarPos = (DISPLAY.get_width() / 2 - 250 / 2, DISPLAY.get_height() / 2 + 10 / 2, 250, 10)
        self.LoadingBarProgress = (self.LoadingBarPos[0], self.LoadingBarPos[1], max(10, Utils.Get_Percentage(self.Progress, self.LoadingBarPos[2], self.ProgressMax)), 10)

        Shape.Shape_Rectangle(DISPLAY, (20, 20, 58), self.LoadingBarPos, 0, self.LoadingBarPos[3])
        Shape.Shape_Rectangle(DISPLAY, (94, 114, 219), self.LoadingBarProgress, 0, self.LoadingBarPos[3])

    def EventUpdate(self, event):
        if self.ApplicationSeletor:
            self.ApplicationSelectorObj.EventUpdate(event)

            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                if not self.ApplicationSelectorObj.SelectedItemIndex == -1:
                    try:
                        # Create the Application Process
                        Core.MAIN.CreateProcess(self.ApplicationSelectorObj.SelectedItemModulePath, self.ApplicationSelectorObj.SelectedItemModulePath)

                        # Allow Window Manager do receive request
                        Core.wmm.WindowManagerSignal(None, 4)

                        # Kills the Bootloader process
                        Core.MAIN.KillProcessByPID(self.PID)

                    except Exception as e:
                        Traceback = traceback.format_exc()

                        self.GenerateCrashLog(Traceback, self.ApplicationSelectorObj.SelectedItemModulePath)

                        print(Traceback)
                        self.FatalErrorScreen = True
                        self.ApplicationSeletor = True
                        self.APPLICATION_HAS_FOCUS = True

        else:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and self.Progress == 0:
                self.LoadingComplete = False
                self.LoadingBarProgress = 0
                self.Progress = 0
                self.ProgressAddDelay = 0
                self.ProgressProgression = False

                self.ApplicationSeletor = True

        if self.FatalErrorScreen:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.FatalErrorScreen = False
                self.ApplicationSeletor = True

    def GenerateCrashLog(self, Traceback, ApplicationName):
        print("Generating crash log...")
        # Create the directory for the Crash Logs
        CrashLogsDir = "./Logs/".replace("/", Core.TaiyouPath_CorrectSlash)
        Utils.Directory_MakeDir(CrashLogsDir)

        # Set the FileName
        FilePath = CrashLogsDir + ApplicationName + "_boot.txt"

        # Set the Application Information
        ProcessInformation = "This application has been failed to boot\n --- Application INFORMATION ---\n"

        ProcessInformation += "Name:" + ApplicationName + "\n"

        ProcessInformation += "--- ERROR TRACEBACK ---"

        FileWrite = open(FilePath, "w")
        FileWrite.write(ProcessInformation)
        FileWrite.write(Traceback)
        FileWrite.close()

        print("Crash log completed")

    def InstallPackpagedApplication(self):
        pass

    def FinishLoadingScreen(self):
        self.ProgressMax = self.Progress

    def LoadingSteps(self, CurrentProgres):
        if CurrentProgres == 0:
            # Start the SystemUI
            Core.MAIN.CreateProcess("CoreFiles/System/TaiyouUI", "system_ui", pPriority=1)

        if CurrentProgres == 1:
            # Start the Task Scheduler
            Core.MAIN.CreateProcess("CoreFiles/System/task_scheduler", "task_scheduler", pPriority=1)

        if CurrentProgres == 2:
            # Finish the Loading
            self.FinishLoadingScreen()