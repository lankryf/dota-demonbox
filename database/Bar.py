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


import sqlite3
from datetime import datetime

from database.migrations import migrations

from database.models.Characters import *
from database.models.Teams import *
from database.models.Matches import *


class Databar(Characters, Teams, Matches):
    def __init__(self, path, backupsFolder="database/backups"):
        self.__path = path
        self.__backupsFolder = backupsFolder
        
        self.__initConnectionAndCursor()
    
    
    def __initConnectionAndCursor(self):
        self.__conn = sqlite3.connect(self.__path)
        self.__cur = self.__conn.cursor()
    
    
    def backup(self) -> None:
        """Backups database to backupsFolder with timestamp
        """
        self.__conn.commit()
        backup = sqlite3.connect(self.__backupsFolder + datetime.now().strftime("/%d-%m-%y_%H-%M-%S.db"))
        self.__conn.backup(backup)
        backup.close()
    
    
    def clearWithBackup(self):
        """Generates backup, clears database, migrate tables
        """
        self.backup()
        self.__conn.close()
        with open(self.__path, "w") as _:
            pass
        self.__initConnectionAndCursor()
        self.migrate()
        

    @property
    def cur(self):
        return self.__cur


    def migrate(self):
        """Migrates all from migrations.py
        """
        for migration in migrations:
            self.__cur.execute(migration)
    
    def commit(self):
        self.__conn.commit()
    
    def close(self):
        """Commit and close
        """
        self.__conn.commit()
        self.__conn.close()