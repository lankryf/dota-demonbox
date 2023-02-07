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

from os import listdir
from datetime import datetime

class BackupsNerd:
    def __init__(self, backupsFolderPath:str) -> None:
        self.__folderPath = backupsFolderPath

    def backupsList(self, nonMarked:bool=False) -> list[str]:
        condition = (lambda fileName: fileName.find('m.') != -1) \
            if not nonMarked else (lambda fileName: True)
        return [
            self.__folderPath + '/' + filename for filename in listdir(self.__folderPath) 
            if (not filename.startswith('.') and condition(filename))
        ]

    def lastMarked(self) -> str:
        backups = self.backupsList(nonMarked=False)
        backups.sort()
        return backups[-1] if backups else None
    

def backupName(end:str, marked:bool=False) -> str:
    """Generated backup's name with timestamp

    Args:
        end (str): End of backup name (type of file with dot like ".txt")
        marked (bool, optional): True if it is a marked backup. Defaults to False.

    Returns:
        str: Backup's name
    """
    return datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S{'m' if marked else ''}{end}")