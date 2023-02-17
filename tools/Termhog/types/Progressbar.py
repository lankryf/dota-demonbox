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

class Progressbar:
        def __init__(self, iterable, iterLen:int, processName:str, start:int=None, step:int=1):
            hog = Termhog()
            self.__win = hog.wins["process"]
            self.__width  = self.__win.getmaxyx()[1]-2
            self.__name = processName
            self.__iterable = iterable
            self.__barNow = 1
            self.__iterLen = iterLen // step
            self.__progressbarStep = self.__iterLen / self.__width
            self.__start = 1

            self.__draw(hog.borders)

            if start is not None:
                self.__start = start // step
                self.__makeStep(self.__start)
            
        
        def __draw(self, borders=True):
            self.__win.erase()
            if borders:
                self.__win.border()
            self.__win.addstr(0, 1, self.__name)
            self.__win.addstr(2, 1, f"0{' ' * (len(str(self.__iterLen))-1)}/{self.__iterLen}")
            self.__drawBar(".", 2)

        def __drawBar(self, symb:str, colorPair:int):
            self.__win.addstr(1, 0, f"[{symb*self.__width}]", curses.color_pair(colorPair))
            self.__win.refresh()
        
        def __moveBar(self, newBarPosition:int):
            if newBarPosition <= self.__width:
                self.__win.addstr(1, self.__barNow, "#"*(newBarPosition - self.__barNow), curses.color_pair(2))
                self.__barNow = newBarPosition

        def __done(self):
            self.__win.addstr(2, 1, str(self.__iterLen))
            self.__win.addstr(2, self.__width-3, "DONE", curses.color_pair(4))
            self.__drawBar("#", 2)

        def __makeStep(self, n:int):
            newBarPosition = int(n // self.__progressbarStep)
            if newBarPosition > self.__barNow:
                self.__moveBar(newBarPosition)
            self.__win.addstr(2, 1, str(n))
            self.__win.refresh()
        
        def __iter__(self):
            for n, i in enumerate(self.__iterable, self.__start):
                yield i
                self.__makeStep(n)
            
            self.__done()
