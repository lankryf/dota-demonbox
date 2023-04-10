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

import torch
import torch.nn as nn
from tools.Termhog import Termhog

class Teacher:

    @staticmethod
    def defaultOptimizer(model:nn.Module) -> torch.optim.Optimizer:
        return torch.optim.Adam(model.parameters(), lr=0.001)
    
    @staticmethod
    def defaultLossFn() -> torch.optim.Optimizer:
        return nn.MSELoss()

    @classmethod
    def teach(
            cls, model:nn.Module,
            dataLoader:torch.utils.data.DataLoader,
            optimizer:torch.optim.Optimizer|None=None,
            lossFn:torch.nn.modules.loss._Loss|None=None,
            epochs=1
    ) -> None:
        hog = Termhog()
        if optimizer is None:
            optimizer = cls.defaultOptimizer(model)
        if lossFn is None:
            lossFn = cls.defaultLossFn()
        hog.info(f"Teaching model {model.__class__.__name__}.")
        loss = 'noTrainData'
        for epoch in range(1, epochs+1):
            for inputs, outputs in dataLoader:
                optimizer.zero_grad()
                predicted = model(inputs)
                loss = lossFn(predicted, outputs)
                loss.backward()
                optimizer.step()
            hog.ok(f"Epoch: {epoch}; Loss: {loss}.")
        hog.done("Done!")
    
    @staticmethod
    def test(
            model:nn.Module,
            dataset:torch.utils.data.TensorDataset,
            predictedTransformer=lambda x:x
    ) -> None:
        hog = Termhog()
        name = model.__class__.__name__
        hog.info(f"Testing model {name}.")
        fails = 0
        for inputs, outputs in dataset:
            if not torch.equal(predictedTransformer(model(inputs)), outputs):
                fails += 1
        hog.info(f"Model {name} was wrong {fails}/{len(dataset)}.{' Congrats!'if not fails else ''}")