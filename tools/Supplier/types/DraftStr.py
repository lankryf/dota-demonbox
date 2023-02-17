from .Draft import Draft
from database import Databar

class DraftStr(Draft):
    def __init__(self, namesList:list[str]) -> None:
        self._draftList = namesList
    
    def addCharacter(self, characterName:str) -> None:
        """Appends character's name to draft's list

        Args:
            characterName (str): Character's name
        """
        self._draftList.append(characterName)
    
    def stringsList(self, *args) -> list[str]:
        """Draft's list as strings

        Returns:
            list[str]: Draft's list as strings
        """
        return self._draftList
    
    def idsList(self) -> list[int]:
        """Draft's list as ids

        Returns:
            list[int]: Draft's list as ids
        """
        bar = Databar()
        return [bar.characterIdAnyways(name) for name in self._draftList]
    
    def checkNonExistent(self) -> list[str]:
        bar = Databar()
        return [name for name in self._draftList if bar.characterIdByName(name) is None]
