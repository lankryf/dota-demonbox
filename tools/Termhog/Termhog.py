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
from tools.metaclasses import Singleton

class Termhog(metaclass=Singleton):
    def setup(self, termhogTheme:dict) -> None:
        screen = curses.initscr()
        self.rows, self.cols = screen.getmaxyx()
        self.history = []
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        self.setTheme(termhogTheme)
        self.__initWins()

    
    def setTheme(self, termhogTheme:dict) -> None:
        self.__logo = termhogTheme["logo"]
        self.__initColors(termhogTheme["colors"])
        self.__borders = termhogTheme["borders"]

    @property
    def borders(self):
        return self.__borders
    
    def __initColors(self, colors:dict[dict]) -> None:
        for name in colors:
            curses.init_pair(colors[name]["id"],
                             colors[name]["fg"],
                             colors[name]["bg"])


    def __initWins(self):
        self.wins = {
            "main": curses.newwin(self.rows-4, self.cols//2-1, 1, 1),
            "input": curses.newwin(1, self.cols-2, self.rows-2, 1),
            "process": curses.newwin(3, self.cols//2-2, 1, self.cols//2+1),
            "gen": curses.newwin(self.rows-8, self.cols//2-2, 5, self.cols//2+1)
        }
        self.wins["main"].scrollok(True)
        for win in self.wins:
            # self.wins[win].border()
            self.wins[win].refresh()
        self.__winsSetup()
        
        
    def __winsSetup(self):
        self.wins["main"].scrollok(True)
        self.wins["main"].nodelay(True)
        self.wins["input"].keypad(True)
    
    
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
    
    def getchIterator(self):
        win = self.wins["input"]
        win.move(0, 0)
        ch = win.getch()
        while ch != 10:
            yield ch
            ch = win.getch()
        win.erase()
    
    def info(self, text:str) -> None:
        self.__printWithIcon("[i] ", text, 1)
    
    def ok(self, text:str) -> None:
        self.__printWithIcon("[K] ", text, 2)

    def err(self, text:str) -> None:
        self.__printWithIcon("[R] ", text, 3)

    def done(self, text:str) -> None:
        self.__printFullColor("[D] " + text, 4)

    def fatal(self, text:str) -> None:
        self.__printFullColor("[F] " + text, 5)

    def warn(self, text:str) -> None:
        self.__printFullColor("[W] " + text, 8)
    
    def space(self, spaces:int=1):
        """Makes indent with empty lines

        Args:
            spaces (int, optional): Number of empty lines. Defaults to 1.
        """
        win = self.wins["main"]
        win.scroll(spaces)
        win.refresh()
        
    def clear(self):
        """Clears main window
        """
        win = self.wins["main"]
        win.erase()
        win.refresh()
    
    def proportion(self, name1:str, name2:str, name1Percent:float|int) -> None:
        win = self.wins['process']
        win.erase()
        name1Percent = round(name1Percent, 3)
        width  = win.getmaxyx()[1]
        win.addstr(0, 0, f'{name1Percent}%', curses.color_pair(11))
        win.addstr(0, width-7, f"{round(100-name1Percent, 3)}%", curses.color_pair(10))
        name1BarWidth = int(width*name1Percent/100)
        win.addstr(1, 0, f"{'█'*width}", curses.color_pair(10))
        win.addstr(1, 0, f"{'█'*name1BarWidth}", curses.color_pair(11))
        win.addstr(2, 0, name1, curses.color_pair(11))
        win.addstr(2, width - len(name2)-1, name2, curses.color_pair(10))
        win.refresh()
    
    def displayLogo(self) -> None:
        win = self.wins["process"]
        win.erase()
        try:
            win.addstr(0, 0, self.__logo, curses.color_pair(7))
        except: pass
        win.refresh()
    
    def exampleTest(self) -> None:
        """Prints all message types
        """
        text = "This is an example text."
        self.info(text)
        self.warn(text)
        self.ok(text)
        self.err(text)
        self.done(text)
        self.fatal(text)
    
    def pressEnterTo(self, what:str) -> None:
        """Waits for the user to press enter

        Args:
            what (str): displayed reason
        """
        self.info(f"Press Enter to {what} ...")
        while self.wins["input"].getch() != 10:
            pass
    
    def wantToStopProcess(self) -> bool:
        """Says if user wants to stop process

        Returns:
            bool: True if user wants to stop process, else False
        """
        if self.wins["main"].getch() == 24:
            return True
        return False

    def progressEnding(self):
        self.pressEnterTo("continue")
        self.displayLogo()