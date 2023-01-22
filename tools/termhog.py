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
    def __init__(self, termhogConfig:dict) -> None:
        screen = curses.initscr()
        self.rows, self.cols = screen.getmaxyx()
        self.history = []
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        self.__logo = termhogConfig["logo"]
        self.__initColors(termhogConfig["colors"])
        self.__initWins()
    
    
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
        """Waits for the user to press any button

        Args:
            what (str): displayed reason
        """
        self.info(f"Press any button to {what} ...")
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


    def progressbar(self, iterable, iterLen:int, processName:str="PROCESS", start:int=None):
        return Progressbar(self.wins["process"], iterable, iterLen, processName, start)

    def progressEnding(self):
        self.pressEnterTo("continue")
        self.displayLogo()

    def input(self, allowEmpty:bool=False) -> str:
        """Takes string data from user

        Args:
            allowEmpty (bool, optional): True if result can be empty. Defaults to False.

        Returns:
            str: string from user
        """
        win = self.wins["input"]
        win.move(0, 0)
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



class Progressbar:
        def __init__(self, win:curses.window, iterable, iterLen:int, processName:str, start:int=None):
            self.__win = win
            self.__width  = win.getmaxyx()[1]-2
            self.__name = processName
            self.__iterLen = iterLen
            self.__iterable = iterable
            self.__barNow = 1
            self.__oneStep = iterLen / self.__width
            
            self.__draw()
            
            self.__start = 1
            if start is not None:
                self.__start += start
                self.__makeStep(start)
            
        
        def __draw(self):
            self.__win.erase()
            self.__win.border()
            self.__win.addstr(0, 1, self.__name)
            self.__win.addstr(2, 1, f"0{' ' * (len(str(self.__iterLen))-1)}/{self.__iterLen}")
            self.__drawBar(".", 2)

        def __drawBar(self, symb:str, colorPair:int):
            self.__win.addstr(1, 0, f"[{symb*self.__width}]", curses.color_pair(colorPair))
            self.__win.refresh()
        
        def __moveBar(self, newBarPosition:int):
            self.__win.addstr(1, self.__barNow, "#"*(newBarPosition - self.__barNow), curses.color_pair(2))
            self.__barNow = newBarPosition

        def __done(self):
            self.__win.addstr(2, 1, str(self.__iterLen))
            self.__win.addstr(2, self.__width-3, "DONE", curses.color_pair(4))
            self.__drawBar("#", 2)

        def __makeStep(self, n:int):
            newBarPosition = int(n // self.__oneStep)
            if newBarPosition > self.__barNow:
                self.__moveBar(newBarPosition)
            self.__win.addstr(2, 1, str(n))
            self.__win.refresh()
        
        def __iter__(self):
            for n, i in enumerate(self.__iterable, self.__start):
                yield i
                self.__makeStep(n)
            
            self.__done()
        
        def withEnumerate(self):
            """_summary_

            Yields:
                int: Enumerating from 1
                any: Current object
            """
            for n, i in enumerate(self.__iterable, self.__start):
                yield n, i
                self.__makeStep(n)
            
            self.__done()
