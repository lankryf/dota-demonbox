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

import tensorflow as tf
from keras.models import load_model

class Demon(metaclass=Singleton):
    def setup(self, modelsFolder:str) -> None:
        self.__foler = modelsFolder
        self.__models = {}
    
    def loadAllModels(self) -> None:
        for name in os.listdir(self.__foler):
            path = f"{self.__foler}/{name}"
            if os.path.isdir(path):
                self.loadModel(name, path)
    
    def loadModel(self, name:str, path:str) -> None:
        self.__models[name] = load_model(path, compile=True)
    
    def predictMatchAllModels(self, match:Match):
        bar = Databar()
        predictions = {}
        numCharacters, numTeams = bar.characterMaxId()+1, bar.teamMaxId()+1
        
        for name in self.__models:
            predictions[name] = self.predictMatch(name, match, numCharacters, numTeams)
        return predictions
    
    def mutualPredictMatchAllModels(self, match:Match) -> float:
        bar = Databar()
        predictions = {}
        numCharacters, numTeams = bar.characterMaxId()+1, bar.teamMaxId()+1

        for name in self.__models:
            pred = self.predictMatch(name, match, numCharacters, numTeams)
            match.reverse()
            predReversed = self.predictMatch(name, match, numCharacters, numTeams)
            if round(pred) == round(predReversed):
                predictions[name] = 0.5
                continue
            predictions[name] = pred

        return predictions
    
    def fitModel(self, modelName:str, matchesFlow):
        train_x, train_y = [], []
        for x, y in getData(matchesFlow):
            train_x.append(x)
            train_y.append(y)
        train_x = tf.concat(train_x, 0)
        train_y = tf.concat(train_y, 0)

        self.__models[modelName].fit(train_x, train_y, batch_size=100, epochs=16, shuffle=True)
        self.__models[modelName].save(f"{self.__foler}/{modelName}")

    @property
    def modelsNames(self) -> tuple[str]:
        return tuple(self.__models.keys())

    def predictMatch(self, modelName:str, match:Match, numCharacters:int, numTeams:int) -> float:
        inputs = packInputs(draftsCategorical(match[0], numCharacters), teamsCategorical(match, numTeams))
        return self.predictWithInputs(modelName, inputs)
    
    def predictWithInputs(self, modelName:str, inputs) -> float:
        return self.__models[modelName].predict(inputs, verbose=0)[0][0]