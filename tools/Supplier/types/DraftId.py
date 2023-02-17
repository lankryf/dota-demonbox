from .Draft import Draft
from database import Databar

class DraftId(Draft):
    def __init__(self, idsList:list[int]) -> None:
        self._draftList = idsList
    
    def addCharacter(self, characterId:int) -> None:
        """_summary_

        Args:
            characterId (int): Character's id
        """
        self._draftList.append(characterId)
    
    def idsList(self, *args) -> list[int]:
        """Draft's list as ids

        Returns:
            list[int]: Draft's list as ids
        """
        return self._draftList

    def stringsList(self) -> list[str]:
        """Draft's list as strings

        Returns:
            list[str]: Draft's list as strings
        """
        bar = Databar()
        return [bar.characterAllNames(characterId)[0] for characterId in self._draftList]


    def checkNonExistent(self) -> list[str]:
        bar = Databar()
        return [charId for charId in self._draftList if not bar.characterAllNames(charId)]