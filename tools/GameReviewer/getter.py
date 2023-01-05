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


from requests import get
from tools.stringwiz import stringsInside
from tools.threadbooster import ThreadBooster
from tools.GameReviewer.types import Match



class Escorenews(ThreadBooster):
    
    @staticmethod
    def getInputs(pageNumber:int) -> list[str]:
        return stringsInside(get(f"https://escorenews.com/en/dota-2/matches?s2={pageNumber}").text, '<a class="article v_gl582" href="', '">')
    

    @staticmethod
    def getResult(multithreads, matchLinkAddition:str):
        page = get("https://escorenews.com/" + matchLinkAddition).text
        result = Match.matchDataMask(matchLinkAddition)

        # #for test
        # with open("a.txt", "w", encoding="utf-8") as f:
        #     f.write(page)

        #getting drafts
        for side in range(2):
            for game in stringsInside(page, f'<div class="heroes t{side+1}">', '</div>'):
                result["drafts"][side].append(stringsInside(game, '<picture class="hero tt" title="', '">', lambda x: x.lower()))


        #getting scores
        scores = [
            stringsInside(page, '<span rel="t1" class="team green">', '</span>', lambda x: x.lower()),
            stringsInside(page, '<span rel="t2" class="team red">', '</span>', lambda x: x.lower())
            ]
        
        # skip if it is empty match
        if not len(scores[0]):
            return

        for score in scores[0]:
            if score[:3] == "<u>":
                result["wins"].append(0)
            else:
                result["wins"].append(1)


        #remove tage from team name
        def removeTag(text:str) -> str:
            if text[:3] == "<u>":
                return text[3:-4]
            return text


        #getting team names
        for score in scores:
            result["teams"].append(removeTag(score[0]))


        #postprocessing
        for scoreNumber in range(1, len(scores[0])):

            #replace incorrect team names
            teams = [None, None]
            for scoresNumber in range(len(scores)):
                scoreNoTag = removeTag(scores[scoresNumber][scoreNumber])
                if scoreNoTag in result["teams"]:
                    teams[scoresNumber] = scoreNoTag
            if None in teams:
                noneIndex = teams.index(None)
                teams[noneIndex] = [name for name in result["teams"] if name != teams[1-noneIndex]][0]

            #reverce sides if it's wanted
            if teams != result["teams"]:
                result["wins"][scoreNumber] = 1 - result["wins"][scoreNumber]
                result["drafts"][0][scoreNumber], result["drafts"][1][scoreNumber] = result["drafts"][1][scoreNumber], result["drafts"][0][scoreNumber]

        multithreads._addResult(result)


    @staticmethod
    def pageExists(pageNumber:int):
        if get(f"https://escorenews.com/en/dota-2/matches?s2={pageNumber}").text.find('<div class="nodata">No matches found</div>') != -1:
            return False
        return True
        

    @staticmethod
    def getLastPageNumber() -> int:
        step = 1000
        result = 0
        plus = True
        
        while step >= 1:
            result += step if plus else -step
            if plus != Escorenews.pageExists(result):
                plus = not plus
                step /= 10
                continue
        return int(result)