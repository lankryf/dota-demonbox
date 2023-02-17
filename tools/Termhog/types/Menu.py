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

import curses
from ..Termhog import Termhog

class Menu:
    def __init__(self):
        self.__win = Termhog().wins["gen"]
        self.__rows, _ = self.__win.getmaxyx()
        self.__active = False
        
    def __call__(self) -> str:
        result = self.value
        self.clear()
        return result
        
    def loadMenu(self, menuList:list[str]) -> None:
        self.clear()
        self.__menuList = menuList
        self.__now = 0
        self.__page = 0
        self.__active = True
        self.__draw()
        
    def clear(self):
        self.__active = False
        self.__menuList = []
        self.__maxRow = 0
        self.__win.erase()
        self.__win.refresh()
    
    def __draw(self):
        menuPage = self.__now // self.__rows
        if menuPage != self.__page:
            self.__page = menuPage
            self.__win.erase()
        nowFirstOnPage = menuPage*self.__rows
        now = self.__now % self.__rows
        names = self.__menuList[nowFirstOnPage:nowFirstOnPage+self.__rows]
        self.__maxRow = len(names) - 1 
        for number, name in enumerate(names):
            if number == now:
                self.__win.addstr(number, 0, name, curses.color_pair(7))
                continue
            try:
                self.__win.addstr(number, 0, name)
            except:
                print(f"---{name}")
        self.__win.refresh()
    
    def down(self):
        if self.__now < self.__maxRow:
            self.__now += 1
            self.__draw()
        
    def up(self):
        if self.__now:
            self.__now -= 1
            self.__draw()
        
    @property
    def value(self) -> str:
        if self.__menuList:
            return self.__menuList[self.__now]
    
    @property
    def active(self) -> bool:
        return self.__active
    
    @property
    def height(self):
        return self.__rows