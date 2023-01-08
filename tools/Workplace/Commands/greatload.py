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

from tools.Workplace.Workplace import Workplace
from tools.Workplace.Command import Command

from tools.GameReviewer.getter import Escorenews

def greatload(wp:Workplace, cmd:Command):
    
    getter = Escorenews(wp.config.getint("processing", "threadCount"))
    
    wp.hog.info("Getting last page ...")
    lastPage = getter.getLastPageNumber()
    wp.hog.ok(f"Last page is {lastPage}")
    
    if wp.tasks.hasCurrentTask() and wp.tasks.currentTask[0] == cmd.name:
        starting = lastPage - wp.tasks.currentTask[1][0]
    else:
        starting = lastPage
        wp.bar.clearWithBackup()
        wp.hog.ok("Backuped and cleared")

    wp.hog.info(f"We will start from {starting}")

    for pageNumber in range(starting, 0, -1):
        
        if wp.hog.wantToStopProcess():
            break
        
        getter.loadInput(pageNumber)
        for result in getter:
            for match in result:
                wp.bar.matchAdd(match)

            message = f"Page: {pageNumber}"
            if result:
                wp.bar.commit()
                wp.hog.ok(message)
            else:
                wp.hog.err(message)
    
    wp.tasks.setCurrentTask(cmd.name, lastPage - pageNumber)
    wp.tasks.save()
    wp.hog.ok("Task has been saved!")
    wp.hog.done("Refreshed!")