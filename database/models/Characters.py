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


class Characters():
    def characterIdExists(self, name:str) -> int:
        """"Returns character's id (if exists) by name

        Args:
            name (str): Character's name

        Returns:
            int|None: If characterId does not exist returns None
        """
        self.cur.execute("SELECT character_id FROM characters WHERE name==? LIMIT 1", (name,))
        result = self.cur.fetchall()
        return result[0][0] if result else None
    
    def characterId(self, name:str) -> int:
        """Returns characters's id anyways, if it does not exist creates character

        Args:
            name (str): Character's name

        Returns:
            int: Character's id
        """
        charId = self.characterIdExists(name)
        return charId if charId else self.characterAdd(name)
    
    
    def characterAdd(self, name:str) -> int:
        """Add character to the database

        Args:
            name (str): Character's name

        Returns:
            int: Character's id
        """
        self.cur.execute("INSERT INTO characters(name) VALUES(?) RETURNING character_id", (name,))
        return self.cur.fetchall()[0][0]