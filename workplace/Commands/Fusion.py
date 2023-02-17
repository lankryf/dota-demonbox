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

class Fusion(Father):

    flags = ()
    hints = {
        None: (),
        'char': ('characters_names', 'characters_names'),
        'team': ('teams_names', 'teams_names')
    }

    @staticmethod
    def body(wp:Workplace, cmd:Command):

        if cmd.mode is None:
            wp.hog.info("There is nothing to do :)")
            return

        funcs = {
            "char": wp.bar.characterFusionByName,
            "team": wp.bar.teamFusionByName
        }
        
    
        funcs[cmd.mode](*cmd.args)
        wp.hog.ok(f"Fusion on {cmd.mode} has been done.")


        wp.bar.commit()
        wp.hog.ok("Commited.")