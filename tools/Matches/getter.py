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
from tools.stringwiz import findallWithFunc, directString
from tools.AsyncBoosted import AsyncBoosted
from tools.Matches.types import Match, Game, DraftStr

from bs4 import BeautifulSoup


def normalizeName(text:str) -> str:
    return directString(
        BeautifulSoup(text.replace("&amp;", '&'),'html.parser').get_text()
    ).replace(' ', '_')



class Escorenews(AsyncBoosted):
    
    # Modifiers
    @staticmethod
    def sheetLinkModifier(linkPart) -> str:
        return f"https://escorenews.com/en/dota-2/matches?s2={linkPart}"
    @staticmethod
    def pageLinkModifier(linkPart) -> str:
        return "https://escorenews.com/" + linkPart



    # Getter functions
    @staticmethod
    def getPagesFromSheet(link:str, *_) -> list[str]:
        return findallWithFunc(r'<a class="article v_gl582" href="(.*?)">', link)

    @staticmethod
    def getResultFromPage(page:str, link:str):
        
        #getting scores
        scores = [
            findallWithFunc(r'<span rel="t1" class="team green">(.*?)</span>', page, lambda x: x.lower()),
            findallWithFunc(r'<span rel="t2" class="team red">(.*?)</span>', page, lambda x: x.lower())
            ]
        # skip if it is empty match
        if not len(scores[0]):
            return
        
        
        #getting drafts and scores
        games = []
        sides = [findallWithFunc(fr'<div class="heroes t{side}">(.*?)</div>', page) for side in range(1, 3)]
        for gameNumber in range(len(sides[0])):
            games.append(Game(
                [DraftStr(
                    findallWithFunc(
                        r'<picture class="hero tt" title="(.*?)">',
                        side[gameNumber],
                        lambda x: normalizeName(x.lower())
                    )
                ) for side in sides
                ],
                0 if scores[0][:3] == "<u>" else 1
            ))


        #getting team names
        teamsNames = []
        for score in scores:
            teamsNames.append(normalizeName(score[0]))


        #postprocessing
        for gameNumber in range(1, len(games)):

            teams = [None, None]
            #replace incorrect team names
            for scoresNumber in range(len(scores)):
                scoreNoTag = normalizeName(scores[scoresNumber][gameNumber])
                if scoreNoTag in teamsNames:
                    teams[scoresNumber] = scoreNoTag
            if None in teams:
                noneIndex = teams.index(None)
                teams[noneIndex] = [name for name in teamsNames if name != teams[1-noneIndex]][0]

            #reverce sides if it's wanted
            if teams != teamsNames:
                games[gameNumber].reverse()
        
        return Match(games, link, teamsNames)


    # Additional functions

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