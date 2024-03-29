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

from workplace.Workplace import Workplace
from workplace.Command import Command


class Father:


    @classmethod
    def execute(cls, workplace:Workplace, command:Command) -> None:
        for flag in command.flags:
            if flag not in cls.flags:
                workplace.hog.fatal(f'Command "{command.name}" has no flag named "-{flag}"')
                return
        
        if command.mode not in cls.hints:
            workplace.hog.fatal(f'Command "{command.name}" has no mode named "{command.mode}"')
            return
        thisHints = cls.hints[command.mode]
        if len(command.args) != len(thisHints):
            workplace.hog.fatal(f'Command "{command.name}" must have {len(thisHints)} args. ({len(command.args)} given)"')
            return
        
        for n, hint in enumerate(thisHints):
            if type(hint) is type:
                if not command.argToType(n, hint):
                    workplace.hog.fatal(f"Argument number {n} must fit to type {hint}")
                    return
        
        cls.body(workplace, command)