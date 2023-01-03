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

class Characters:
    def validName(self, name:str) -> bool:
        self._cur.execute("SELECT id FROM characters WHERE name=? LIMIT 1", (name,))
        return bool(self._cur.fetchall())
    
    def add(self, name:str):
        self._cur.execute("INSERT OR IGNORE INTO characters(name) VALUES(?)", (name,))