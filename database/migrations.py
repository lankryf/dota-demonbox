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

migrations = [
'''CREATE TABLE "characters" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''',

'''CREATE TABLE "drafts" (
	"id"	INTEGER NOT NULL UNIQUE,
	"game_id"	INTEGER NOT NULL,
	"team"	INTEGER NOT NULL,
	"character_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''',

'''CREATE TABLE "games" (
	"id"	INTEGER NOT NULL UNIQUE,
	"team1_id"	INTEGER NOT NULL,
	"team2_id"	INTEGER NOT NULL,
	"result"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
''',

'''CREATE TABLE "teams" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
'''
]