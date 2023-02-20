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

    flags = ('b')
    hints = {None: (None, int), "workbook": ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        match cmd.mode:
            case None:
                if cmd.args[0] not in wp.demon.modelsNames:
                    wp.hog.fatal(f'There is no model named "{cmd.args[0]}"')
                    return
                
                start = cmd.args[1]

                if 'b' not in cmd.flags:
                    start = -start

                wp.hog.info(f"So, AI model {cmd.args[0]} will be fited.")
                wp.demon.fitModel(cmd.args[0], matchesFlow(start))

            case "workbook":
                modelNames = wp.demon.modelsNames
                for modelName, start in wp.workbook.fitInstructionFlow():
                    if modelName not in modelNames:
                        wp.hog.err(f"Model {modelName} hasn't been loaded. Passing.")
                        continue

                    wp.hog.info(f"Model {modelName} will now be fitted with start {start}")
                    wp.demon.fitModel(modelName, matchesFlow(start))
                
                wp.hog.done(f"Fitting has been done.")
        wp.hog.progressEnding(True)