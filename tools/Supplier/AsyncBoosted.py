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


import asyncio, aiohttp
from tools.Supplier.Proxima import Proxima

class AsyncBoosted:
    def __init__(self, waitingTime:float|int=2, proxima:Proxima=Proxima()):
        self.waitingTime = waitingTime
        self.__proxima = proxima

    @staticmethod
    def sheetLinkModifier(link:str) -> str:
        return link

    @staticmethod
    def pageLinkModifier(link:str) -> str:
        return link
    

    async def __process(self, sheetslinks:list):
        async with aiohttp.ClientSession() as session:

            sheetsData = await asyncio.gather(
                *[
                    self.__getOrWait(session, self.sheetLinkModifier(link),
                        self.getPagesFromSheet
                    ) for link in sheetslinks
                ]
            )

            pagesData = await asyncio.gather(
                *[
                    self.__getOrWait(session, self.pageLinkModifier(link),
                    self.getResultFromPage) for claster in sheetsData for link in claster
                ]
            )
        return pagesData


    def getResults(self, sheetslinks:list) -> list:
        return asyncio.run(self.__process(sheetslinks))

    def getTrueResults(self, sheetslinks:list) -> list:
        return [obj for obj in asyncio.run(self.__process(sheetslinks)) if obj]

    async def __getOrWait(self, session, link:str, func=lambda res: res) -> str:
        status = 500
        result = ''
        while status != 200:
            try:
                async with session.get(link, proxy=self.__proxima.getProxy()) as response:
                    status = response.status
                    if status == 200:
                        result = await response.text()
            except: pass
            await asyncio.sleep(self.waitingTime)

        return func(result, link)