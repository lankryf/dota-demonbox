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

class Backup(Father):

    flags = ('c', 'm')
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        marked = False
        if 'm' in cmd.flags:
            wp.hog.info("This backup will be marked")
            marked = True

        if 'c' in cmd.flags:
            wp.bar.clearWithBackup(marked)
            wp.hog.ok("Backuped and cleared.")
        else:
            wp.bar.backup(marked)
            wp.hog.ok("Backuped.")