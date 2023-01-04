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
    
    @property
    def total(self) -> list[int]:
        result = [0, 0]
        for team in self.wins:
            result[team] += 1
        return result
    




# class Draft:
#     def __init__(self, draftlist:list[str]) -> None:
#         self.__stringList = draftlist
    
#     @property
#     def stringList(self) -> list[str]:
#         return self.__stringList

#     @property
#     def idsList(self) -> list[int]:
        