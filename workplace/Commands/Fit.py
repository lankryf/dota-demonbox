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
from database.generators.matchesGenerator import matchesFlow

class Fit(Father):

    flags = ()
    hints = {None: (None,)}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        if cmd.args[0] not in wp.demon.modelsNames:
            wp.hog.fatal(f'There is no model named "{cmd.args[0]}"')
            return
        
        wp.hog.info(f"So, AI model {cmd.args[0]} will be fited.")
        wp.demon.fitModel(cmd.args[0], matchesFlow())