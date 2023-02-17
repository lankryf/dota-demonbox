
from .DraftId import DraftId
from .DraftStr import DraftStr

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
    
    def setDraft(self, team:int, draft:DraftId|DraftStr) -> None:
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