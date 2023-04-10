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

from tools.metaclasses import Singleton

import torch
import torch.nn as nn
from os import path

class SaveLoader(metaclass=Singleton):
    def setup(self, modelsFolderPath:str) -> None:
        self.__modelsFolderPath = modelsFolderPath

    def save(self, model:nn.Module) -> None:
        torch.save(model.state_dict(), f'{self.__modelsFolderPath}/{model.__class__.__name__}.pt')
    
    def load(self, model:nn.Module) -> nn.Module:
        model.load_state_dict(torch.load(f'{self.__modelsFolderPath}/{model.__class__.__name__}.pt'))

    def saved(self, model:nn.Module) -> bool:
        return path.exists(f'{self.__modelsFolderPath}/{model.__class__.__name__}.pt')