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
from Demon.DataFeeder import inputDataLen

class Getinfo(Father):

    flags = ()
    hints = {
        None: (),
        'char': ('characters_names',),
        'team': ('teams_names',),
        'match': (int,)
    }

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        
        match cmd.mode:
            case None:
                wp.hog.info("We have:")
                wp.hog.info(f"{wp.bar.characterCount()} characters,")
                wp.hog.info(f"Character max ID is {wp.bar.characterMaxId()},")
                wp.hog.space()
                wp.hog.info(f"{wp.bar.teamCount()} teams,")
                wp.hog.info(f"Team max ID is {wp.bar.teamMaxId()},")
                wp.hog.space()
                wp.hog.info(f"{wp.bar.matchCount()} matches,")
                wp.hog.info(f"Match max ID is {wp.bar.matchMaxId()};")
                wp.hog.space()
                wp.hog.info(f"Input shape is {inputDataLen()}")
            
            case 'match':
                match = wp.bar.matchById(cmd.args[0])
                if match is None:
                    wp.hog.err(f'Match with id "{cmd.args[0]}" wasn\'t found!')
                    return
                wp.hog.info(f"Match: link: {match.link}")
                wp.hog.info(f"Teams IDs: {match.teams}")
                for n, teamId in enumerate(match.teams):
                    wp.hog.info(f"Team {n} name is {wp.bar.teamAllNames(teamId)[0]}")
                for gameNumber, game in enumerate(match):
                    wp.hog.space()
                    wp.hog.info(f"Game {gameNumber}:")
                    for draftNumber, draft in enumerate(game.drafts):
                        wp.hog.info(f"Draft{draftNumber}: {' '.join(draft.stringsList(wp.bar))}")
                    wp.hog.info(f"Result: {game.result}")
                
                wp.hog.space()
                wp.hog.info(f"Match: link: {match.link}")
            case _:

                funcs = {
                    "char": (
                        wp.bar.characterIdByName,
                        wp.bar.characterAllNames
                    ),
                    "team": (
                        wp.bar.teamIdByName,
                        wp.bar.teamAllNames
                    )
                }

                objectId = funcs[cmd.mode][0](cmd.args[0])
                if objectId is None:
                    wp.hog.err(f'{cmd.mode}\'s name "{cmd.args[0]}" wasn\'t found!'.capitalize())
                    return

                
                names = funcs[cmd.mode][1](objectId)

                wp.hog.info(f"{cmd.mode}'s ID = {objectId}")
                wp.hog.info(f"{cmd.mode}'s names ({len(names)}):\n    {names}")
