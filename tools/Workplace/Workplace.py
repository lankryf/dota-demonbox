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

# terminal interface
from tools.termhog import TermHog

# database
from database.Bar import Databar

class Workplace:
    def __init__(self, configsPath:str="configs") -> None:
        self.__configsPath = configsPath
        self.__setup()


    def __setup(self):
        # init termhog
        with open(self.__configsPath + "/termhog.json", "r") as f:
            self.hog = TermHog(jsonLoad(f)["colors"])
        self.hog.ok("TermHog has been loaded.")
        
        # load config
        self.__config = ConfigParser()
        try:
            self.__config.read(self.__configsPath + "/config.ini")
        #TODO log error
        except: pass #Exception as e:
        else: self.hog.ok("Config has been read.")

        # load database
        self.bar = Databar(self.__config["database"]["path"], self.__config["database"]["backupsFolder"])

        self.__initCommands()

        
    def __initCommands(self):
        self.commands = {}
        folder = self.__config['commands']['path']
        for name in listdir(folder):
            if ospath.isdir(f"{folder}/{name}"):
                continue
            name = name[:-3]
            self.commands[name] = getattr(import_module(f"{folder.replace('/', '.')}.{name}"), name)

    
    def inputLoop(self):
        inp = ""
        while inp != "exit":
            inp = self.hog.input()
            args = inp.split()
            if args[0] not in self.commands:
                self.hog.err(f'Command "{args[0]}" is not found :(')
                continue
            self.commands[args[0]](self, args[1:])
        