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

from workplace.Workplace import Workplace
from tools.Supplier.types import Match, Game
from keras.utils import to_categorical
import tensorflow as tf

def inputDataLen():
    wp = Workplace()
    return (wp.bar.characterMaxId() + wp.bar.teamMaxId() + 2) * 2


def teamsCategorical(match:Match, teamMaxId:int):
    return [to_categorical(
        match.teams[teamNumber], teamMaxId
        ) for teamNumber in range(0, 2)] 

def draftsCategorical(game:Game, characterMaxId:int):
    return [tf.math.reduce_sum(
            to_categorical(game.drafts[draftNumber].idsList(Workplace().bar), characterMaxId), 0
            ) for draftNumber in range(0, 2)]


def packInputs(drafts:list, teams:list):
    return tf.expand_dims(tf.concat(drafts + teams, 0), axis=0)


def packData(drafts:list, teams:list, result:int):
    return packInputs(drafts, teams), tf.constant(result, dtype="float32", shape=(1,1))


def getInputData(matches):
    wp = Workplace()
    characterMaxId = wp.bar.characterMaxId() + 1
    teamMaxId = wp.bar.teamMaxId() + 1

    for match in matches:
        teams = teamsCategorical(match, teamMaxId)
        for game in match:
            drafts = draftsCategorical(game, characterMaxId)
            yield packData(teams, drafts, game.result)
            yield packData(list(reversed(teams)), list(reversed(drafts)), 1-game.result)