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

from workplace.Commands.Common.CommandFather import *
from tools.Supplier.types import Match, Game, DraftStr
from workplace.Advisor import inputWithAdvice
from Demon.Demon import predictMatch


class Predict(Father):

    flags = ()
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        menu = wp.hog.menu()
        drafts = []
        teams = []
        for teamIndex in range(2):
            name = inputWithAdvice(wp.hog, menu, lambda inp: wp.bar.searchFullNames(inp, "teams_names"))
            wp.hog.info(f"Team {teamIndex} is {name}")
            teams.append(name)
        drafts = []
        for draftIndex in range(2):
            wp.hog.space()
            draft = []
            for characterIndex in range(5):
                name = inputWithAdvice(wp.hog, menu, lambda inp: wp.bar.searchFullNames(inp, "characters_names"))
                wp.hog.info(f"Team {draftIndex} character {characterIndex} is {name}")
                draft.append(name)
            drafts.append(DraftStr(draft))
        wp.hog.space()
        predicted = predictMatch(Match([Game(drafts, None)], None, [wp.bar.teamIdByName(name) for name in teams]))[0][0]
        wp.hog.ok(str(predicted))
        wp.hog.proportion(*teams, (1 - predicted)*100)
        wp.hog.progressEnding()
