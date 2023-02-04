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

from json import load, dump
from os import path as ospath


class Reader:
    def __init__(self, filePath:str) -> None:
        self.path = filePath
        if ospath.exists(self.path):
            with open(self.path, "r") as f:
                self._data = load(f)
        else:
            self.clear()
            self.save()

    def __getattr__(self, name):
        return self._data[name]

    def save(self) -> None:
        """Saves changes to file
        """
        with open(self.path, "w") as f:
            dump(self._data, f, indent=4)