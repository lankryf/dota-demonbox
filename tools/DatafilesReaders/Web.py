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

from .Reader import Reader


class Web(Reader):
    def clear(self) -> None:
        """Clears web's data
        """
        self._data = {
            "proxies": []
        }
    
    def setProxies(self, proxyList:list[str]):
        self._data["proxies"] = proxyList