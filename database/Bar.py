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
from database.models.Characters import Characters
from database.migrations import migrations

class Databar(Characters):
    def __init__(self, path="data.db"):
        self._conn = sqlite3.connect(path)
        self._cur = self._conn.cursor()
    
    def migrate(self):
        for migration in migrations:
            self._cur.execute(migration)
    
    def close(self):
        self._conn.commit()
        self._conn.close()
    
    