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


class Match:
    def __init__(self, gamedata:dict) -> None:
        self.__gamedata = gamedata

    def __getattr__(self, name):
        return self.__gamedata[name]
    
    
    @staticmethod
    def matchDataMask(link:str) -> dict:
        return {
            "link": link,
            "teams": [],
            "drafts": [[], []],
            "wins": []
        }

    @property
    def byGames(self):
        for gameNumber in range(len(self.drafts[0])):
            yield Game([self.drafts[0][gameNumber], self.drafts[1][gameNumber]], self.wins[gameNumber])
            
    
    
    @property
    def total(self) -> list[int]:
        result = [0, 0]
        for team in self.wins:
            result[team] += 1
        return result



class Game:
    def __init__(self, drafts:list[list[str]], result:int):
        self.__drafts = [Draft(draft) for draft in drafts]
        self.__result = result
    
    @property
    def drafts(self):
        return self.__drafts
    
    @property
    def result(self):
        return self.__result



class Draft:
    def __init__(self, draftlist:list[str]) -> None:
        self.__stringList = draftlist
    
    @property
    def stringList(self) -> list[str]:
        return self.__stringList
    
    def idList(self, databar) -> list[int]:
        return [databar.characterId(name) for name in self.__stringList]