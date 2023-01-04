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


class Teams:
    def teamExists(self, name:str) -> bool:
        """Checks for team by name

        Args:
            name (str): team's name

        Returns:
            bool: True if exists, False if not
        """
        self.cur.execute("SELECT id FROM teams WHERE name=? LIMIT 1", (name,))
        return bool(self.cur.fetchall())
    
    def teamAdd(self, name:str) -> None:
        """Add team to the database

        Args:
            name (str): team's name
        """
        self.cur.execute("INSERT INTO teams(name) VALUES(?)", (name,))