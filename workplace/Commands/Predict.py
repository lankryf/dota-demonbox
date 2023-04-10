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

from .Common.CommandFather import *
from tools.Supplier.types import Match, Game, DraftStr
from tools.Termhog.types import Menu
from workplace.Advisor import inputWithAdvice
from Demon.DataFeeder import forOnePrediction


class Predict(Father):

    flags = ()
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        menu = Menu()
        drafts = []
        teamsNames = []
        teamsIds = []
        for teamIndex in range(2):
            name = inputWithAdvice(wp.hog, menu, lambda inp: wp.bar.searchFullNames(inp, "teams_names"))
            wp.hog.info(f"Team {teamIndex} is {name}")
            teamId = wp.bar.teamIdByName(name)
            if teamId is None:
                wp.hog.fatal(f'Team\'s name "{name}" wasn\'t found!')
                return
            teamsIds.append(teamId)
            teamsNames.append(name)
        drafts = []
        for draftIndex in range(2):
            wp.hog.space()
            draft = []
            for characterIndex in range(5):
                name = inputWithAdvice(wp.hog, menu, lambda inp: wp.bar.searchFullNames(inp, "characters_names"))
                wp.hog.info(f"Team {draftIndex} character {characterIndex} is {name}")
                draft.append(name)
            draft = DraftStr(draft)
            nonExistmentDrafts = draft.checkNonExistent()
            if nonExistmentDrafts:
                wp.hog.fatal(f'Character\'s name "{nonExistmentDrafts[0]}" wasn\'t found!')
                return
            drafts.append(draft)
        data = forOnePrediction(drafts, teamsIds)
        predicted = float(wp.demon(data)[0][0])
        wp.hog.ok(f'Demon: {predicted}')
        wp.hog.proportion(*teamsNames, (1 - predicted)*100)