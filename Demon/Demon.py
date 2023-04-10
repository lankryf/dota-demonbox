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
from .DataFeeder import draftsCategorical, teamsCategorical, packInputs, getData

from tools.Supplier.types import Match
from database import Databar
from tools.metaclasses import Singleton
import os

import torch
import torch.nn as nn

class Demon(nn.Module):
    def __init__(self, inputSize:int):
        super(self.__class__, self).__init__()
        self.li1 = nn.Linear(inputSize, 512)
        self.li2 = nn.Linear(512, 64)
        self.li3 = nn.Linear(64, 1)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()


    def forward(self, x):
        x = self.li1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.li2(x)
        x = self.sigmoid(x)
        x = self.li3(x)
        return self.sigmoid(x)