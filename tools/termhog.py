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

class TermHog:
    def __init__(self, colors:dict[dict[int]]):
        screen = curses.initscr()
        self.rows, self.cols = screen.getmaxyx()
        self.history = []
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        self.__initColors(colors)
        self.__initWins()
    
    
    def __initColors(self, colors:dict[dict]):
        for name in colors:
            curses.init_pair(colors[name]["id"],
                             colors[name]["fg"],
                             colors[name]["bg"])


    def __initWins(self):
        self.wins = {
            "main": curses.newwin(self.rows-4, self.cols//2-1, 1, 1),
            "input": curses.newwin(1, self.cols-2, self.rows-2, 1),
            "process": curses.newwin(self.rows//2-1, self.cols//2-2, 1, self.cols//2+1),
            "gen": curses.newwin(self.rows//2-2, self.cols//2-2, self.rows//2, self.cols//2+1)
        }
        self.wins["main"].scrollok(True)
        for win in self.wins:
            self.wins[win].border()
            self.wins[win].refresh()
        self.__winsSetup()
        
        
    def __winsSetup(self):
        self.wins["main"].scrollok(True)
    
    
    def __printFullColor(self, text:str, color:int) -> None:
        win = self.wins["main"]
        win.scroll()
        win.addstr(win.getmaxyx()[0]-1, 0, text, curses.color_pair(color))
        win.refresh()

    
    def __printWithIcon(self, icon:str, text:str, iconColor:int) -> None:
        win = self.wins["main"]
        win.scroll()
        win.addstr(win.getmaxyx()[0]-1, 0, icon, curses.color_pair(iconColor))
        win.addstr(text)
        win.refresh()
    
    
    def info(self, text:str) -> None:
        self.__printWithIcon(" ", text, 1)
    
    def ok(self, text:str) -> None:
        self.__printWithIcon(" ", text, 2)

    def err(self, text:str) -> None:
        self.__printWithIcon(" ", text, 3)

    def done(self, text:str) -> None:
        self.__printFullColor(" " + text, 4)

    def fatal(self, text:str) -> None:
        self.__printFullColor(" " + text, 5)

    def warn(self, text:str) -> None:
        self.__printFullColor(" " + text, 8)
    
    def exampleTest(self) -> None:
        text = "This is an example text."
        self.info(text)
        self.warn(text)
        self.ok(text)
        self.err(text)
        self.done(text)
        self.fatal(text)
    
    def input(self, allowEmpty:bool=False):
        win = self.wins["input"]
        result = ""
        
        while not result:
            ch = win.getch()
            while ch != 10:
                
                
                match ch:
                    
                    case 127:
                        if result:
                            win.delch(0, len(result)-1)
                            result = result[:-1]
                    
                    
                    
                    case _:
                        win.addch(ch)
                        result += chr(ch)
        
                        
                ch = win.getch()

            if allowEmpty:
                break

        win.erase()
        return result