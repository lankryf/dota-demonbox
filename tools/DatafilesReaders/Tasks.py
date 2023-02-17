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

from .Reader import Reader


class Tasks(Reader):

    def hasCurrentTask(self) -> bool:
        """Does tasks have current task

        Returns:
            bool: True if has, False if don't
        """
        return bool(self.currentTask)

    def clear(self) -> None:
        """Clears tasks
        """
        self._data = {
            "currentTask": []
        }
    
    def setCurrentTask(self, taskName:str, *args) -> None:
        """Set current task with arguments

        Args:
            taskName (str): Task's name
            *args (any): arguments that should be given to current task
        """
        self._data["currentTask"] = [taskName, args]