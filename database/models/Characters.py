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
    def characterIdByName(self, name:str) -> int|None:
        """"Returns character's id (if exists) by name

        Args:
            name (str): Character's name

        Returns:
            int|None: If characterId does not exist returns None
        """
        self.cur.execute("SELECT character_id FROM characters_names WHERE name==? LIMIT 1", (name,))
        result = self.cur.fetchall()
        return result[0][0] if result else None
    
    def characterIdAnyways(self, name:str) -> int:
        """Returns characters's id anyways, if it does not exist creates character

        Args:
            name (str): Character's name

        Returns:
            int: Character's id
        """
        charId = self.characterIdByName(name)
        if charId:
            return charId
        
        charId = self.characterAdd()
        self.characterAddName(charId, name)
        return charId
    
    
    def characterAdd(self, tinyName:str=None, color:int=None) -> int:
        """Adds character to the database

        Args:
            tinyName (str, optional): Name's tiny form, will be used for search. Defaults to None.
            color (int, optional): Color of the character's name. Defaults to None.

        Returns:
            int: Character's id
        """
        self.cur.execute("INSERT INTO characters(tiny_name, color) VALUES(?,?) RETURNING character_id", (tinyName, color))
        return self.cur.fetchall()[0][0]


    def characterAddName(self, characterId:int, name:str) -> None:
        """Adds character's name to the database

        Args:
            characterId (int): Character's id
            name (str): Name that should be added
        """
        self.cur.execute("INSERT INTO characters_names(character_id, name) VALUES(?,?)", (characterId, name))


    def characterFusionAndDelete(self, oldCharId:int, newCharId:int) -> None:
        """Deletes character from database and gives it's names to another

        Args:
            oldCharId (int): Id of character that should be deleted
            newCharId (int): Id of character that will take names
        """
        for table in ('characters_names', 'drafts'):
            self.cur.execute(f"UPDATE {table} SET character_id = ? WHERE character_id == ?", (newCharId, oldCharId))
        self.cur.execute("DELETE FROM characters WHERE character_id = ?", (oldCharId,))