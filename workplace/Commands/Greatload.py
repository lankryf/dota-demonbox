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

from tools.Supplier.getters import Escorenews
from tools.Supplier import Proxima
from tools.Termhog.types import Progressbar

class Greatload(Father):

    flags = ()
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        
        proxima = Proxima(wp.web.proxies, withMe=True)
        if proxima.isEmpty():
            wp.hog.warn("There are no proxies, greatload will be slow")
        else:
            allproxies = len(proxima)
            proxima.setWorkingOnly(Escorenews.sheetLinkModifier(1))
            wp.hog.info(f"Proxies that work {len(proxima)}/{allproxies}")
            del allproxies

        getter = Escorenews(waitingTime=2, proxima=proxima)
        
        wp.hog.info("Getting last page ...")
        lastPage = getter.getLastPageNumber()
        wp.hog.ok(f"Last page is {lastPage}")
        
        # loads a task if it exists
        if wp.tasks.hasCurrentTask() and wp.tasks.currentTask[0] == cmd.name:
            starting = lastPage - wp.tasks.currentTask[1][0]
        else:
            starting = lastPage
            wp.bar.clearWithBackup()
            wp.hog.ok("Backuped and cleared")

        wp.hog.info(f"We will start from {starting}")

        clasterSize = wp.config.getint("getter", "clasterSize")
        wp.hog.info(f"Claster size is {clasterSize}")

        clasterNumbers = None
        wp.hog.info(f"Starting ...")
        for clasterStart in Progressbar(range(starting, 0, -clasterSize), lastPage, "GREATLOAD", lastPage - starting, step=5):
            
            if wp.hog.wantToStopProcess():
                break
            
            clasterNumbers = tuple(range(clasterStart, max(0, clasterStart-clasterSize), -1))

            data = getter.getTrueResults(clasterNumbers)
            for match in data:
                added = wp.bar.matchAdd(match)
                if not added:
                    wp.hog.info(f'Match with link "{match.link}" is already in the database')


            if data:
                wp.bar.commit()
                wp.hog.ok(f"Claster {clasterNumbers} : {len(data)} matches")
            else:
                wp.hog.err(f"Claster {clasterNumbers} : empty")

        if not clasterNumbers is None:
            if clasterNumbers[-1] > 1:
                wp.tasks.setCurrentTask(cmd.name, lastPage - clasterNumbers[-1] + 1)
            else:
                wp.tasks.clear()
            wp.tasks.save()
            wp.hog.ok("Task has been saved!")
        else:
            wp.hog.info("Nothing was done, task has stayed the same.")
        
        
        wp.hog.done("Greatload has been done!")
        wp.hog.progressEnding()