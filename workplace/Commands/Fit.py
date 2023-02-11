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


import tensorflow as tf
from Demon.DataFeeder import getInputData

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
        trainData = getInputData(wp.bar.matchIterate(wp.bar.matchMaxId() - 6000))
        for x, y in trainData:
            train_x.append(x)
            train_y.append(y)
        x = tf.concat(train_x, 0)
        y = tf.concat(train_y, 0)
        wp.hog.ok("Train data has been taken.")

        indices = tf.range(start=0, limit=tf.shape(x)[0], dtype=tf.int32)
        shuffled_indices = tf.random.shuffle(indices)
        shuffled_x = tf.gather(x, shuffled_indices)
        shuffled_y = tf.gather(y, shuffled_indices)
        wp.hog.ok("Shuffled.")

        wp.hog.info(str(x))
        wp.hog.info(str(y))

        wp.aimodel.fit(shuffled_x, shuffled_y, batch_size=100, epochs=20, validation_split=0.1 )
        wp.aimodel.save("Demon/Models/Marette")