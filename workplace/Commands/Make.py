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

from Demon.DataFeeder import inputDataLen

from keras.layers import Dense
import keras

class Make(Father):
    flags = ()
    hints = {None: (), "aimodels": ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        match cmd.mode:
            case 'aimodel':
                inputLen = inputDataLen()
                aimodels = {

                "Little": keras.Sequential([
                    Dense(128, activation='relu', input_shape=(inputLen,)),
                    Dense(64, activation='sigmoid'),
                    Dense(8, activation='sigmoid'),
                    Dense(1, activation='sigmoid')
                ]),

                "Nerdy": keras.Sequential([
                    Dense(560, activation='relu', input_shape=(inputLen,)),
                    Dense(128, activation='sigmoid'),
                    Dense(16, activation='sigmoid'),
                    Dense(1, activation='sigmoid')
                ]),

                "Mistress": keras.Sequential([
                    Dense(1800, activation='relu', input_shape=(inputLen,)),
                    Dense(580, activation='sigmoid'),
                    Dense(128, activation='sigmoid'),
                    Dense(1, activation='sigmoid')
                ])
                }

                for name in aimodels:
                    aimodels[name].compile(
                        optimizer="adam", loss="mean_squared_error",
                        metrics=['accuracy']
                    )
                    aimodels[name].save(f"Demon/Models/{name}")
                    wp.hog.ok(f"Model {name} has been created.")

            case _:
                wp.hog.info("There is nothing to do :)")