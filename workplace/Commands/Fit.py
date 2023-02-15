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
from database.generators.matchesGenerator import matchesFlow

import tensorflow as tf
from Demon.DataFeeder import getData

class Fit(Father):

    flags = ()
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        wp.aimodel.compile(
            optimizer="adam", loss="mean_squared_error",
            metrics=['accuracy']
        )
        wp.hog.ok("Compiled.")

        train_x, train_y = [], []
        for x, y in getData(matchesFlow(-1000)):
            train_x.append(x)
            train_y.append(y)
        train_x = tf.concat(train_x, 0)
        train_y = tf.concat(train_y, 0)
        wp.hog.ok("Train data has been taken.")
        wp.hog.ok("Shuffled.")

        wp.hog.info(str(train_x))
        wp.hog.info(str(train_y))

        wp.aimodel.fit(train_x, train_y, batch_size=100, epochs=16, shuffle=True)
        wp.aimodel.save(f"Demon/Models/Mistress")