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


class Proxima:
    def __init__(self, proxies:list[str] = []):
        self.__proxies = proxies
        if self.isEmpty():
            self.getProxy = lambda: None
        else:
            self.reset()
    
    def __len__(self) -> int:
        return len(self.__proxies)

    @staticmethod
    async def __checkProxy(session, linkForCheck:str, proxy:str) -> bool:
        result = False
        try:
            async with session.get(linkForCheck, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    result = True
        except: pass
        return proxy, result
    
    async def __checkAllProxies(self, linkForCheck:str):
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(
                *[
                    self.__checkProxy(
                        session, linkForCheck, proxy
                    ) for proxy in self.__proxies
                ]
            )

    def checkNonWorking(self, linkForCheck:str) -> list[str]:
        return [
            proxy for proxy, working in asyncio.run(self.__checkAllProxies(linkForCheck)) if not working
        ]
    
    def setWorkingOnly(self, linkForCheck:str) -> None:
        self.__proxies = [
            proxy for proxy, working in asyncio.run(self.__checkAllProxies(linkForCheck)) if working
        ]

    def isEmpty(self) -> bool:
        return not self.__proxies

    def reset(self):
        self.__generator = (proxy for proxy in self.__proxies)
    
    def getProxy(self) -> str:
        try:
            obj = next(self.__generator)
        except:
            self.reset()
            obj = next(self.__generator)
        return obj
