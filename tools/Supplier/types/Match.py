
from .Game import Game

class Match:
    def __init__(self, games:list[Game], link:str, teams:list[str]|list[int], id:int|None=None) -> None:
        self.__games = games
        self.__link = link
        self.__teams = teams
        self.__id = id
    
    def __getitem__(self, index) -> Game:
        return self.__games[index]
    
    def __len__(self):
        return len(self.__games)
    
    def __iter__(self):
        return iter(self.__games)
    
    @classmethod
    def empty(cls, link:str, team1, team2, id:int|None=None):
        return cls([], link, [team1, team2], id)
    
    def addGame(self, game:Game) -> None:
        """Appends game to match's list of games

        Args:
            game (Game): game that should be appended
        """
        self.__games.append(game)
    
    def reverse(self) -> None:
        self.__teams.reverse()
        for game in self.__games:
            game.reverse()

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