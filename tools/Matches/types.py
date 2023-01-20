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



class Draft:
    @classmethod
    def empty(cls):
        return cls([])
    
    def __len__(self):
        return len(self._draftList)
    


class DraftStr(Draft):
    def __init__(self, namesList:list[str]) -> None:
        self._draftList = namesList
    
    def addCharacter(self, characterName:str) -> None:
        """Appends character's name to draft's list

        Args:
            characterName (str): Character's name
        """
        self._draftList.append(characterName)
    
    def stringsList(self) -> list[str]:
        """Draft's list as strings

        Returns:
            list[str]: Draft's list as strings
        """
        return self._draftList
    
    def idsList(self, databar) -> list[int]:
        """Draft's list as ids

        Returns:
            list[int]: Draft's list as ids
        """
        return [databar.characterIdAnyways(name) for name in self._draftList]


class DraftId(Draft):
    def __init__(self, idsList:list[int]) -> None:
        self._draftList = idsList
    
    def addCharacter(self, characterId:int) -> None:
        """_summary_

        Args:
            characterId (int): Character's id
        """
        self._draftList.append(characterId)
    
    def idsList(self) -> list[int]:
        """Draft's list as ids

        Returns:
            list[int]: Draft's list as ids
        """
        return self._draftList



class Game:
    def __init__(self, drafts:list[DraftId|DraftStr], result:int, id:int|None=None):
        self.__drafts = drafts
        self.__result = result
        self.__id = id
    
    
    @classmethod
    def empty(cls, result:int, id:int|None=None, draftClass:type[DraftId]|type[DraftStr]=DraftId):
        """Creates empty game without drafts

        Args:
            result (int): Who wins
            id (int | None, optional): Game's id in database. Defaults to None.
            draftClass (type[DraftId] | type[DraftStr], optional): Class that will be used as draft. Defaults to DraftId.

        Returns:
            Game: Class' instance
        """
        return cls([draftClass.empty() for _ in range(2)], result, id)
    
    def setDraft(self, team:int, draft:Draft) -> None:
        """Sets draft to specified team

        Args:
            team (int): Team's number (0 or 1)
            draft (Draft): Draft that should replace current value
        """
        self.__drafts[team] = draft
    
    def reverse(self) -> None:
        """Reverses teams' data
        """
        self.__drafts.reverse()
        self.__result = 1 - self.result
    
    @property
    def drafts(self):
        return self.__drafts
    
    @property
    def result(self):
        return self.__result
    
    @property
    def id(self) -> int|None:
        return self.__id

    
class Match:
    def __init__(self, games:list[Game], link:str, teams:list[str], id:int|None=None) -> None:
        self.__games = games
        self.__link = link
        self.__teams = teams
        self.__id = id
    
    def __getitem__(self, index) -> Game:
        return self.__games[index]
    
    def __len__(self):
        return len(self.__games)
    
    @classmethod
    def empty(cls, link:str, team1, team2, id:int|None=None):
        return cls([], link, [team1, team2], id)
    
    def addGame(self, game:Game) -> None:
        """Appends game to match's list of games

        Args:
            game (Game): game that should be appended
        """
        self.__games.append(game)
    
    @property
    def link(self) -> str:
        return self.__link
    
    @property
    def teams(self) -> str:
        return self.__teams
    
    @property
    def id(self) -> int|None:
        return self.__id
    
    @property
    def total(self) -> list[int]:
        result = [0, 0]
        for game in self.__games:
            result[game.result] += 1
        return result