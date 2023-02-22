# Copyright 2023 LankryF

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# metaclasses
from tools.metaclasses import Singleton

# for configs
from configparser import ConfigParser
from json import load as jsonLoad

# for commands
import os
from importlib import import_module
from .Advisor import Advisor

# terminal interface
from tools.Termhog import Termhog

# database
from database import Databar

# datareaders
from tools.DatafilesReaders import Web, Tasks, Workbook

# Demon
from Demon import Demon

# for errors
from traceback import format_exc

class Workplace(Advisor, metaclass=Singleton):

    def setup(self, configsPath:str="configs"):
        self.__configsPath = configsPath
        self.__work = True # for loop
        # init termhog
        self.hog = Termhog()
        with open("configs/TermhogThemes/8colors.json", "r") as f:
            self.hog.setup(jsonLoad(f))
        self.hog.ok("TermHog has been started.")
        
        self.hog.displayLogo()
        
        # load config
        configiniPath = self.__configsPath + "/config.ini"
        if not os.path.exists(configiniPath):
            self.hog.fatal(f"Config file {configiniPath} is not exsist.\nPlease, create it using config.ini.example.")
            self.hog.pressEnterTo("exit")
            raise(FileNotFoundError(configiniPath))
        self.__config = ConfigParser()
        self.__config.read(configiniPath)

        # refresh termhog theame
        with open(self.__config["termhog"]["themeFilePath"], "r") as f:
            self.hog.setTheme(jsonLoad(f))

        self.hog.ok("Config has been read.")
        self.hog.ok("TermHog theme was set.")

        # load database

        self.bar = Databar()
        self.bar.setup(self.__config["database"]["path"], self.__config["database"]["backupsFolder"])
        self.hog.ok("Database has been opened.")

        # Data readers
        self.tasks = Tasks(self.__config["processing"]["taskFilePath"])
        self.web = Web(self.__config["web"]["webFilePath"])
        self.workbook = Workbook(
            self.__config["workbook"]["workbookFilePath"],
            self.__config["demon"]["modelsFolder"]
        )
        self.hog.ok("Data-readers have been loaded.")

        self.hog.info("initialization for some demon's stuff...")

        # Demon
        self.demon = Demon()
        self.demon.setup(self.__config["demon"]["modelsFolder"])

        self.__initCommands()
        self.hog.done("I'm ready to work :)")
    
    
    @property
    def config(self):
        return self.__config
    
    def __ending(self):
        self.bar.close()
        self.hog.ok("Database has been closed.")

        
    def __initCommands(self):
        self.__commands = {}
        self.__commandsNames = []
        
        folder = self.__config['commands']['folder']
        for name in os.listdir(folder):
            if os.path.isdir(f"{folder}/{name}"):
                continue
            name = name[:-3]
            lowerName = name.lower()
            self.__commands[lowerName] = getattr(import_module(f"{folder.replace('/', '.')}.{name}"), name)
            self.__commandsNames.append(lowerName)
        self.__commandsNames.sort()


    @property
    def commandsNames(self) -> list[str]:
        return self.__commandsNames
    
    @property
    def commands(self) -> dict[object]:
        return self.__commands
    
    def stop(self) -> None:
        self.__work = False
    
    def shutdown(self) -> None:
        self.__ending()
        os.system('systemctl poweroff -i')


    def inputLoop(self):
        while self.__work:
            cmd = self.inputCommand()
            if cmd.name not in self.commands:
                self.hog.err(f'Command "{cmd.name}" is not found :(')
                continue
            
            self.hog.space()
            try:
                self.commands[cmd.name].execute(self, cmd)
            except Exception as e:
                self.hog.fatal(format_exc())

        self.__ending()