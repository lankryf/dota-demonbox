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
from tools.Supplier.types import Match, Game
from keras.utils import to_categorical
import tensorflow as tf


def inputDataLen() -> int:
    """Input shape lenght

    Returns:
        int: lenght
    """
    bar = Databar()
    return (bar.characterMaxId() + bar.teamMaxId() + 2) * 2


def teamsCategorical(match:Match, teamMaxId:int) -> list:
    return [to_categorical(
        match.teams[teamNumber], teamMaxId
        ) for teamNumber in range(0, 2)] 

def draftsCategorical(game:Game, characterMaxId:int):
    return [tf.math.reduce_sum(
            to_categorical(game.drafts[draftNumber].idsList(), characterMaxId), 0
            ) for draftNumber in range(0, 2)]


def packInputs(drafts:list, teams:list):
    return tf.expand_dims(tf.concat(drafts + teams, 0), axis=0)


def packData(drafts:list, teams:list, result:int):
    """Pacs inputs and output

    Args:
        drafts (list): draftsCategorical output
        teams (list): teamsCategorical output
        result (int): game's result

    Returns:
        tf.constant: packed inputs
        tf.constant: packed output
    """
    return packInputs(drafts, teams), tf.constant(result, dtype="float32", shape=(1,1))



# packers
def regularPacker(drafts:list, teams:list, game:Game):
    """Packs inputs and outputs and yields them

    Args:
        drafts (list): draftsCategorical output
        teams (list): teamsCategorical output
        game (Game): current game

    Yields:
        tf.constant: packed inputs
        tf.constant: packed output
    """
    yield packData(drafts, teams, game.result)

def trainPacker(drafts:list, teams:list, game:Game):
    """Packs inputs and outputs and yields them and reversed versions

    Args:
        drafts (list): draftsCategorical output
        teams (list): teamsCategorical output
        game (Game): current game

    Yields:
        tf.constant: packed inputs
        tf.constant: packed output
    """
    yield packData(drafts, teams, game.result)
    yield packData(list(reversed(drafts)), list(reversed(teams)), 1-game.result)

def inputsWithGamePacker(drafts:list, teams:list, game:Game):
    """Packs only inputs and current game

    Args:
        drafts (list): draftsCategorical output
        teams (list): teamsCategorical output
        game (Game): current game

    Yields:
        Game: current game
        tf.constant: packed inputs
    """
    yield game, packInputs(drafts, teams)



def getData(matches, packer=trainPacker):
    bar = Databar()
    characterMaxId = bar.characterMaxId() + 1
    teamMaxId = bar.teamMaxId() + 1

    for match in matches:
        teams = teamsCategorical(match, teamMaxId)
        for game in match:
            drafts = draftsCategorical(game, characterMaxId)
            for packedData in packer(drafts, teams, game):
                yield packedData 