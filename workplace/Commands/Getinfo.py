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

class Getinfo(Father):

    flags = ()
    hints = {
        None: (),
        'char': ('characters_names',),
        'team': ('teams_names',)
    }

    @staticmethod
    def body(wp:Workplace, cmd:Command):

        if cmd.mode is None:
            wp.hog.info("There is nothing to do :)")
            return

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
