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
    def teamIdExists(self, name:str) -> int|None:
        """Returns team's id (if exists) by name

        Args:
            name (str): Team's name

        Returns:
            int|None: If teamId does not exist returns None
        """
        self.cur.execute("SELECT team_id FROM teams WHERE name=? LIMIT 1", (name,))
        result = self.cur.fetchall()
        return result[0][0] if result else None


    def teamId(self, name:str) -> int:
        """Returns team's id anyways, if it does not exist creates team

        Args:
            name (str): Team's name

        Returns:
            int: Team's id
        """
        teamId = self.teamIdExists(name)
        return teamId if teamId else self.teamAdd(name)


    def teamAdd(self, name:str) -> int:
        """Add team to the database

        Args:
            name (str): Team's name

        Returns:
            int: Team's id
        """
        self.cur.execute("INSERT INTO teams(name) VALUES(?) RETURNING team_id", (name,))
        return self.cur.fetchall()[0][0]