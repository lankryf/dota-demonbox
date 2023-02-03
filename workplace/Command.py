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

class Command:
    def __init__(self, factory):
        self.__name, self.__mode = factory.nameWithMode
        self.__args = []
        self.__flags = []
        self.__divide(factory.all[1:])
    
    def __len__(self):
        return len(self.__args)
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def args(self) -> list[str]:
        return self.__args
    
    @property
    def flags(self) -> list[str]:
        return self.__flags

    @property
    def mode(self) -> str:
        return self.__mode
    
    def __divide(self, args:list[str]):
        for arg in args:
            if not arg:
                continue
            if arg[0] == '-':
                self.__flags.append(arg[1:])
                continue
            self.__args.append(arg)



class CommandFactory:
    def __init__(self) -> None:
        self.__all = ['']
    
    def __len__(self) -> int:
        return len(self.__all)
    
    def __str__(self) -> str:
        return ' '.join(self.__all)
    
    def __getitem__(self, index:int):
        return self.__all[index]
    
    def isEmpty(self) -> bool:
        return not bool(self.__all[0])

    @property
    def all(self) -> list[str]:
        return self.__all

    def stringLenght(self) -> int:
        return sum((len(arg) for arg in self.__all)) + len(self.__all) - 1
    
    def addChar(self, character:str) -> None:
        if character == ' ' and self.__all[0]:
            self.__all.append('')
            return
        self.__all[-1] += character
    
    def delCharFromEnd(self) -> None:
        if not self.__all[-1] and len(self.__all) > 0:
            self.__all.pop(-1)
            return
        self.__all[-1] = self.__all[-1][:-1]
    
    def inputStage(self) -> int:
        if len(self.__all) == 1:
            if ':' in self.__all[0]:
                return 1
            return 0
        if not self.__all[-1] or self.__all[-1][0] != '-':
            return 2
        return 3
    
    @property
    def nameWithMode(self) -> str|None:
        splited = self.__all[0].split(":")
        return splited[:2] if len(splited) > 1 else splited + [None]
    
    @property
    def last(self):
        return self.__all[-1]

    @property
    def argNow(self) -> None:
        return [obj for obj in self.__all[1:] if not obj or obj[0] != '-'][:-1]
    
    def setLast(self, value:str) -> None:
        self.__all[-1] = value
    
    def produceCommand(self) -> Command:
        return Command(self)



