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



class Tasks(Father):

    flags = ('c',)
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        if 'c' in cmd.flags:
            wp.tasks.clear()
            wp.tasks.save()
            wp.hog.ok("Tasks have been cleared!")
        else:
            if wp.tasks.hasCurrentTask():
                wp.hog.info(f"Current task: {wp.tasks.currentTask[0]}")
                wp.hog.info(f"Current task args: {wp.tasks.currentTask[1]}")
            else:
                wp.hog.info("No current task here")