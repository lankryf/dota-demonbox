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

from tools.Workplace.Workplace import Workplace
from tools.Workplace.Command import Command

def fusion(wp:Workplace, cmd:Command):
    funcs = {
        "char": wp.bar.characterFusionAndDelete,
        "team": wp.bar.teamFusionAndDelete
    }
    
    if cmd.args[0] not in funcs:
        wp.hog.fatal(f"Type can be {','.join(funcs.keys())}, not {cmd.args[0]}")
        return
    
    if len(cmd.args) != 3:
        wp.hog.fatal(f"There must be 3 arguments ({len(cmd.args)} given)")
        return
    

    names = (int(arg) for arg in cmd.args[1:])
    
    
    try:
        names = list(names)
    except:
        wp.hog.fatal(f"Argument's type error.")
    else:
        for typeName in funcs:
            if cmd.args[0] == typeName:
                funcs[typeName](*names)
                wp.hog.ok(f"Fusion on {typeName} has been done.")
                break
        
        wp.bar.commit()
        wp.hog.ok("Commited.")