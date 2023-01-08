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
    def __init__(self, text:str):
        self.__all = text.split()
        self.__flags = []
        self.__name = self.__all.pop(0)
        self.__args = []
        self.__distribute()
    
    def __len__(self):
        return len(self.__all)
    
    @property
    def name(self):
        return self.__name
    
    @property
    def args(self):
        return self.__args
    
    @property
    def flags(self):
        return self.__flags
    
    def __distribute(self):
        for arg in self.__all:
            if not arg:
                continue
            if arg[0] == '-':
                self.__flags.append(arg[1:])
                continue
            self.__args.append(arg)