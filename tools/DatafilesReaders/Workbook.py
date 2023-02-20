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

from .Reader import Reader
from os import path, listdir

class Workbook(Reader):
    def __init__(self, filePath:str, modelsPath:str) -> None:
        self.__modelsPath = modelsPath
        super().__init__(filePath)

    def clear(self) -> None:
        """Clears workbook
        """
        self._data = {
            "fitter": {name:[] for name in listdir(self.__modelsPath) if path.isdir(f"{self.__modelsPath}/{name}")}
        }
    
    def countFits(self) -> int:
        return sum([len(fitInstruction) for fitInstruction in self.fitter.values()])
    
    def fitInstructionFlow(self):
        return (
            (name, start) for name in self.fitter for start in self.fitter[name]
        )