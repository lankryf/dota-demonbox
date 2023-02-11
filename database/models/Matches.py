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

from tools.Supplier.types import Match, Game
from sqlite3 import IntegrityError

class Matches:
    """Matches include games, drafts
    """


    def matchIdByLink(self, link:str) -> int|None:
        """Returns match's id (if exists) by link

        Args:
            link (str): Match's link

        Returns:
            int|None: If matchId does not exist returns None
        """
        self.cur.execute("SELECT match_id FROM matches WHERE link=? LIMIT 1", (link,))
        result = self.cur.fetchall()
        return result[0][0] if result else None
    
    
    def matchIterate(self, start:int=0):
        """Yields matches from database

        Args:
            start (int, optional): Start from id (this id will be not included). Defaults to 0.

        Yields:
            _type_: Wow, it's a match
        """

        self.cur.execute('''
            SELECT matches.link, matches.team1_id,
                matches.team2_id, matches.match_id,
                games.result, games.game_id,
                drafts.team, drafts.character_id
            
            FROM matches, games, drafts 
            
            ON matches.match_id > ? AND drafts.game_id = games.game_id
                AND games.match_id = matches.match_id''', (start,))

        # first
        first = next(self.cur)
        match = Match.empty(*first[:4])
        game = Game.empty(*first[4:6])
        game.drafts[first[6]].addCharacter(first[7])
        
        # other
        for row in self.cur:
            if row[5] != game.id:
                match.addGame(game)
                game = Game.empty(*row[4:6])
            
            game.drafts[row[6]].addCharacter(row[7])
            
            if row[3] != match.id:
                yield match
                match = Match.empty(*row[:4])
        
        match.addGame(game)
        yield match


    def matchCount(self) -> int:
        """Count of matches

        Returns:
            int: Count of matches
        """
        self.cur.execute("SELECT COUNT(*) FROM matches")
        return self.cur.fetchall()[0][0]
    
    def matchMaxId(self) -> int:
        self.cur.execute("SELECT MAX(match_id) FROM matches")
        return self.cur.fetchall()[0][0]
    
    def matchDelete(self, matchId:int) -> None:
        """Deletes match from database

        Args:
            matchId (int): Match's id
        """
        self.cur.execute("DELETE FROM matches WHERE match_id = ?", (matchId,))


    def matchAdd(self, match:Match) -> bool:
        """Adds match to database

        Args:
            match (Match): Match that should be added

        Returns:
            bool: True if added else False
        """
        #insert match and teams
        try:
            self.cur.execute(
                "INSERT INTO matches(link, team1_id, team2_id) VALUES(?,?,?) RETURNING match_id",
                (match.link, *[self.teamIdAnyways(name) for name in match.teams])
            )
        except Exception as e:
            if isinstance(e, IntegrityError):
                return False
            raise e
        matchId = self.cur.fetchall()[0][0]
        
        #inert games and drafts
        for game in match:
            self.cur.execute(
                "INSERT INTO games(match_id, result) VALUES(?,?) RETURNING game_id",
                (matchId, game.result)
            )
            gameId = self.cur.fetchall()[0][0]
            for teamNumber, draft in enumerate(game.drafts):
                for characterId in draft.idsList(self):
                    self.cur.execute(
                        "INSERT INTO drafts(game_id, team, character_id) VALUES(?,?,?)",
                        (gameId, teamNumber, characterId)
                    )
        return True