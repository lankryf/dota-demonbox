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

from database import Databar
from tools.Supplier.types import Match, Game, Draft
from database.generators.matchesGenerator import matchesFlow
from tools.Termhog.types import Progressbar

import torch
import torch.nn as nn


def inputDataLen() -> int:
    """Input shape lenght

    Returns:
        int: lenght
    """
    bar = Databar()
    return (bar.characterMaxId() + bar.teamMaxId() + 2) * 2


def teamsCategorical(teams:list[int], teamMaxId:int) -> torch.Tensor:
    teams = torch.tensor(teams)
    return nn.functional.one_hot(teams, teamMaxId)

def draftsCategorical(drafts:list[Draft], characterMaxId:int) -> torch.Tensor:
    tensor = torch.zeros((2, characterMaxId), dtype=torch.float32)
    drafts = torch.tensor([draft.idsList() for draft in drafts])
    tensor.scatter_(1, drafts, 1)
    return tensor


def packInputs(drafts:torch.Tensor, teams:torch.Tensor):
    return torch.cat([drafts, teams], dim=1).view(1,-1)


def packData(drafts:list, teams:list, result:int):
    """Pacs inputs and output
    """
    return packInputs(drafts, teams), torch.tensor(result, dtype=torch.float32).view(1,1)



# packers
def regularPacker(drafts:list, teams:list, game:Game):
    """Packs inputs and outputs and yields them
    """
    yield packData(drafts, teams, game.result)

def trainPacker(drafts:list, teams:list, game:Game):
    """Packs inputs and outputs and yields them and reversed versions
    """
    yield packData(drafts, teams, game.result)
    yield packData(drafts.flip(0), teams.flip(0), 1-game.result)

def inputsWithGamePacker(drafts:list, teams:list, game:Game):
    """Packs only inputs and current game
    """
    yield game, packInputs(drafts, teams)

def forOnePrediction(drafts:list[Draft], teams:list[int]):
    bar = Databar()
    characterMaxId = bar.characterMaxId() + 1
    teamMaxId = bar.teamMaxId() + 1
    drafts = draftsCategorical(drafts, characterMaxId)
    teams = teamsCategorical(teams, teamMaxId)
    return packInputs(drafts, teams)

def getData(start:int, packer=trainPacker):
    bar = Databar()
    characterMaxId = bar.characterMaxId() + 1
    teamMaxId = bar.teamMaxId() + 1

    for match in Progressbar(matchesFlow(start), abs(start) if start < 0 else (bar.matchCount()-start),"LOADING"):
        teams = teamsCategorical(match.teams, teamMaxId)
        for game in match:
            drafts = draftsCategorical(game.drafts, characterMaxId)
            for packedData in packer(drafts, teams, game):
                yield packedData

def datasetFromMachesFlow(start:int) -> torch.utils.data.TensorDataset:
    dataGetter = getData(start)
    xs, ys = [], []
    for x, y in dataGetter:
        xs.append(x)
        ys.append(y)
    return torch.utils.data.TensorDataset(torch.cat(xs), torch.cat(ys))


def datasetAndLoaderFromMachesFlow(start:int, batchSize:int=32, numWorkers:int=1) -> tuple[torch.utils.data.TensorDataset, torch.utils.data.DataLoader]:
    dataset = datasetFromMachesFlow(start)
    dataLoader = torch.utils.data.DataLoader(dataset, batch_size=batchSize, shuffle=True, num_workers=numWorkers)
    return dataset, dataLoader