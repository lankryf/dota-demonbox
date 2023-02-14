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
from Demon.DataFeeder import withGamePacker, getData

class Check(Father):

    flags = ()
    hints = {None:(), "predicts":()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        match cmd.mode:
            case "predicts":
                ok = 0
                gamesCount = 0
                for game, packed in getData(wp.bar.matchIterate(-100), withGamePacker):
                    gamesCount += 1
                    predicted = round(wp.aimodel.predict(packed, verbose=0)[0][0])
                    real = game.result
                    if predicted != real:
                        wp.hog.err(f"predict/real: {predicted}/{real}")
                        continue
                    wp.hog.ok(f"Game {gamesCount} has been predicted.")
                    ok += 1
                    
                wp.hog.info(f"We have {ok}/{gamesCount} games, that have been predicted correctly.")
            case _:
                wp.hog.info("There is nothing to do :)")