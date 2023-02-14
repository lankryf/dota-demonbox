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

class Progressbar:
        def __init__(self, win:curses.window, iterable, iterLen:int, processName:str, start:int=None, step:int=1, borders=True):
            self.__win = win
            self.__width  = win.getmaxyx()[1]-2
            self.__name = processName
            self.__iterable = iterable
            self.__barNow = 1
            self.__iterLen = iterLen // step
            self.__progressbarStep = self.__iterLen / self.__width
            self.__start = 1

            self.__draw(borders)

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


class Menu:
    def __init__(self, win:curses.window):
        self.__win = win
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
    
    
    
class Termhog:
    def __init__(self, termhogConfig:dict) -> None:
        screen = curses.initscr()
        self.rows, self.cols = screen.getmaxyx()
        self.history = []
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()
        self.adjust(termhogConfig)
        self.__initWins()

    
    def adjust(self, termhogConfig:dict) -> None:
        self.__logo = termhogConfig["logo"]
        self.__initColors(termhogConfig["colors"])
        self.__borders = termhogConfig["borders"]

    
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


    def progressbar(self, iterable, iterLen:int, processName:str="PROCESS", start:int=None, step:int=1) -> Progressbar:
        return Progressbar(self.wins["process"], iterable, iterLen, processName, start, step, self.__borders)

    def menu(self) -> Menu:
        return Menu(self.wins["gen"])

    def progressEnding(self):
        self.pressEnterTo("continue")
        self.displayLogo()