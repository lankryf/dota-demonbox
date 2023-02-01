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

from workplace.Command import Command, CommandFactory
import curses


class Advisor:
    
    def getHint(self, cmd:CommandFactory, menu):
        

        def suitableList(wholeList:list[str], requirement:str) -> list[str]:
            return [name for name in wholeList if name[:len(requirement)] == requirement]

        menu.clear()
        menuList = []
        try:
            match cmd.inputStage():
                case 0:
                    # command
                    menuList = suitableList(self.commandsNames, cmd.last)

                case 1:
                    # mode
                    commandinfo = cmd.nameWithMode
                    menuList = suitableList([ commandinfo[0] + ':' + mode for mode in list(self.commands[commandinfo[0]].hints.keys()) if mode], cmd.last)

                case 2:
                    # arg
                    commandinfo = cmd.nameWithMode
                    hints = self.commands[commandinfo[0]].hints[commandinfo[1]]
                    argIndex = len(cmd.argNow)
                    if argIndex < len(hints):
                        hint = hints[argIndex]
                        if hint is not None:
                            if isinstance(hint, tuple):
                                menuList = hint
                            else:
                                menuList = self.bar.searchFullNames(cmd.last, hint, menu.height)

                case 3:
                    # flag
                    menuList = suitableList(['-' + flag for flag in self.commands[cmd[0]].flags], cmd.last)
            
        except:
            pass
        
        menu.loadMenu(menuList)
        
    
    def inputCommand(self) -> Command:
        win = self.hog.wins["input"]
        win.move(0, 0)
        cmd = CommandFactory()
        menu = self.hog.menu()
        self.getHint(cmd, menu)
        
        while cmd.isEmpty():
            ch = win.getch()
            while ch != 10:
                match ch:
                    
                    case 9:
                        self.getHint(cmd, menu)
                    
                    case curses.KEY_DOWN:
                        menu.down()
                    
                    case curses.KEY_UP:
                        menu.up()
                    
                    case curses.KEY_RIGHT:
                        hint = menu()
                        if hint:
                            cmd.setLast(hint)
                            win.addstr(0, 0, str(cmd))
                    
                    case curses.KEY_BACKSPACE:
                        if not cmd.isEmpty():
                            win.delch(0, cmd.stringLenght()-1)
                            cmd.delCharFromEnd()
                            self.getHint(cmd, menu)
                    
                    case _:
                        win.addch(ch)
                        cmd.addChar(chr(ch))
                        self.getHint(cmd, menu)
                
                ch = win.getch()

        win.erase()
        return cmd.produceCommand()