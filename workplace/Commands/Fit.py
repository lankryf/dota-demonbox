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
from Demon import Teacher
from Demon.DataFeeder import datasetAndLoaderFromMachesFlow
import torch

class Fit(Father):

    flags = ('b', 'p')
    hints = {None: (int,), "workbook": ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        if 'p' in cmd.flags:
            wp.hog.info("There'll be poweroff at the end.")
        numWorkers = wp.config.getint('demon', 'numWorkers')
        wp.hog.info(f"Number of workers is {numWorkers}.")
        match cmd.mode:
            case None:

                start = cmd.args[0]

                if 'b' not in cmd.flags:
                    start = -start
                dataset, dataLoader = datasetAndLoaderFromMachesFlow(start, 32, numWorkers)
                Teacher.teach(wp.demon, dataLoader, epochs=16)
                Teacher.test(wp.demon, dataset, torch.round)
            case "workbook":
                for start in wp.workbook.fitter:
                    dataset, dataLoader = datasetAndLoaderFromMachesFlow(start, 32, numWorkers)
                    wp.hog.info(f"Start point is {start}.")
                    Teacher.teach(wp.demon, dataLoader, epochs=10)
                    Teacher.test(wp.demon, dataset, torch.round)
                
        wp.saveLoader.save(wp.demon)
        wp.hog.info(f"Demon has been saved.")

        if 'p' in cmd.flags:
            wp.shutdown()
            return
        wp.hog.progressEnding()