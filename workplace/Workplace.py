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

#for configs
from configparser import ConfigParser
from json import load as jsonLoad

#for commands
from os import listdir, path as ospath
from importlib import import_module
from workplace.Advisor import Advisor

# terminal interface
from tools.Termhog.termhog import Termhog

# database
from database.Bar import Databar

# tasks
from tools.tasks import Tasks


class Workplace(Advisor):
    def __init__(self, configsPath:str="configs") -> None:
        self.__configsPath = configsPath
        self.__work = True
        self.__setup()


    def __setup(self):
        # init termhog
        with open("tools/Termhog/Themes/8colors.json", "r") as f:
            self.hog = Termhog(jsonLoad(f))
        self.hog.ok("TermHog has been started.")
        
        self.hog.displayLogo()
        
        # load config
        configiniPath = self.__configsPath + "/config.ini"
        if not ospath.exists(configiniPath):
            self.hog.fatal(f"Config file {configiniPath} is not exsist.\nPlease, create it using config.ini.example.")
            self.hog.pressEnterTo("exit")
            raise(FileNotFoundError(configiniPath))
            
        
        self.__config = ConfigParser()
        self.__config.read(configiniPath)

        with open(self.__config["termhog"]["themeFilePath"], "r") as f:
            self.hog.adjust(jsonLoad(f))

        self.hog.ok("Config has been read.")
        self.hog.ok("TermHog theme was set")

        # load database
        self.bar = Databar(self.__config["database"]["path"], self.__config["database"]["backupsFolder"])
        self.hog.ok("Database has been opened.")

        # load tasks
        self.tasks = Tasks(self.__config["processing"]["taskFilePath"])

        self.__initCommands()
    
    
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
        for name in listdir(folder):
            if ospath.isdir(f"{folder}/{name}"):
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
                self.hog.fatal(str(e))

        self.__ending()