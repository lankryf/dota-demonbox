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

migrations = (
'''CREATE TABLE IF NOT EXISTS "characters" (
	"character_id"	INTEGER NOT NULL,
	"tiny_name"		TEXT DEFAULT NULL,
	"color"			INT DEFAULT NULL,
	PRIMARY KEY("character_id" AUTOINCREMENT)
);
''',

'''CREATE TABLE IF NOT EXISTS "characters_names" (
    "character_name_id"	INTEGER NOT NULL,
	"character_id"	REFERENCES characters (character_id) ON DELETE CASCADE ON UPDATE CASCADE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("character_name_id" AUTOINCREMENT)
);
''',

'''CREATE TABLE IF NOT EXISTS "drafts" (
	"draft_id"	INTEGER NOT NULL UNIQUE,
	"game_id"	REFERENCES games (game_id) ON DELETE CASCADE,
	"team"	INTEGER NOT NULL,
	"character_id"	REFERENCES characters (character_id) ON UPDATE CASCADE,
	PRIMARY KEY("draft_id" AUTOINCREMENT) 
);
''',

'''CREATE TABLE IF NOT EXISTS "matches" (
	"match_id"	INTEGER NOT NULL UNIQUE,
	"link"	TEXT NOT NULL UNIQUE,
	"team1_id"	REFERENCES teams (team_id) ON UPDATE CASCADE,
	"team2_id"	REFERENCES teams (team_id) ON UPDATE CASCADE,
	PRIMARY KEY("match_id" AUTOINCREMENT)
);
''',

'''CREATE TABLE IF NOT EXISTS "games" (
	"game_id"	INTEGER NOT NULL UNIQUE,
	"match_id"	REFERENCES matches (match_id) ON DELETE CASCADE,
	"result"	INTEGER NOT NULL,
	PRIMARY KEY("game_id" AUTOINCREMENT)
);
''',

'''CREATE TABLE IF NOT EXISTS "teams" (
	"team_id"	INTEGER NOT NULL,
	"tiny_name"	TEXT DEFAULT NULL,
	PRIMARY KEY("team_id" AUTOINCREMENT)
);
''',

'''CREATE TABLE IF NOT EXISTS "teams_names" (
	"team_name_id"	INTEGER NOT NULL,
	"team_id"	REFERENCES teams (team_id) ON DELETE CASCADE ON UPDATE CASCADE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("team_name_id" AUTOINCREMENT)
);
'''
)