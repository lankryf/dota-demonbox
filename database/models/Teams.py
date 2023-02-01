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
    def teamIdByName(self, name:str) -> int|None:
        """Returns team's id (if exists) by name

        Args:
            name (str): Team's name

        Returns:
            int|None: If teamId does not exist returns None
        """
        self.cur.execute("SELECT team_id FROM teams_names WHERE name=? LIMIT 1", (name,))
        result = self.cur.fetchall()
        return result[0][0] if result else None


    def teamIdAnyways(self, name:str) -> int:
        """Returns team's id anyways, if it does not exist creates team

        Args:
            name (str): Team's name

        Returns:
            int: Team's id
        """
        teamId = self.teamIdByName(name)
        if teamId:
            return teamId
        
        teamId = self.teamAdd()
        self.teamAddName(teamId, name)
        return teamId


    def teamAdd(self, tinyName:str=None) -> int:
        """Adds team to the database

        Args:
            tinyName (str, optional): Name's tiny form, will be used for search. Defaults to None.

        Returns:
            int: Teams's id
        """
        self.cur.execute("INSERT INTO teams(tiny_name) VALUES(?) RETURNING team_id", (tinyName,))
        return self.cur.fetchall()[0][0]
    
    
    def teamAddName(self, teamId:int, name:str) -> None:
        """Adds team's name to the database

        Args:
            teamId (int): Team's id
            name (str): Name that should be added
        """
        self.cur.execute("INSERT INTO teams_names(team_id, name) VALUES(?,?)", (teamId, name))
    
    def teamCount(self) -> int:
        """Count of teams

        Returns:
            int: Count of teams
        """
        self.cur.execute("SELECT COUNT(*) FROM teams")
        return self.cur.fetchall()[0][0]
    
    def teamMaxId(self) -> int:
        self.cur.execute("SELECT MAX(team_id) FROM teams")
        return self.cur.fetchall()[0][0]
    
    def teamFusionById(self, oldTeamId:int, newTeamId:int) -> None:
        """Deletes team from database and gives it's names to another

        Args:
            oldTeamId (int): Id of team that should be deleted
            newTeamId (int): Id of team that will take names
        """
        self.cur.execute("UPDATE teams_names SET team_id = ? WHERE team_id == ?", (newTeamId, oldTeamId))
        
        for teamNumber in range(1, 3):
            self.cur.execute(f"UPDATE matches SET team{teamNumber}_id = ? WHERE team{teamNumber}_id == ?", (newTeamId, oldTeamId))
        
        self.cur.execute("DELETE FROM teams WHERE team_id = ?", (oldTeamId,))
    
    def teamFusionByName(self, oldTeamName:str, newTeamName:str) -> None:
        """Deletes team from database and gives it's names to another

        Args:
            oldTeamName (str): Name of team that should be deleted
            newTeamName (str): Name of team that will take names
        """
        names = (oldTeamName, newTeamName)
        self.cur.execute("SELECT name, team_id FROM teams_names WHERE name IN (?, ?)", names)
        namesIds = self.cur.fetchall()
        if len(namesIds) != 2:
            return
        namesIds = dict(namesIds)
        self.teamFusionById(*[namesIds[name] for name in names])
        
    def teamAllNames(self, teamId:int) -> list[str]:
        self.cur.execute("SELECT name from teams_names WHERE team_id == ?", (teamId,))
        return [row[0] for row in self.cur.fetchall()]