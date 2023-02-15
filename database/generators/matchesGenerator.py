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

from tools.Supplier.types import Match, Game
from database.Bar import Databar


def matchesFlow(start:int=0):
    """Yields matches from database

    Args:
        start (int, optional): Start from id (this id will be not included). Negative if start is relative to end. Defaults to 0.

    Yields:
        Match: Wow, it's a match
    """
    bar = Databar()

    if start < 0: # negative start number
        start = bar.matchMaxId() + start

    bar.cur.execute('''
        SELECT matches.link, matches.team1_id,
            matches.team2_id, matches.match_id,
            games.result, games.game_id,
            drafts.team, drafts.character_id
        
        FROM matches, games, drafts 
        
        ON matches.match_id > ? AND drafts.game_id = games.game_id
            AND games.match_id = matches.match_id''', (start,))

    for match in matchesFromCur(bar.cur):
        yield match


def matchById(_id:int) -> Match:
    """Get single match by id without troubles

    Args:
        _id (int): Match's id

    Returns:
        Match: Wow, it is a single match
    """

    bar = Databar()

    bar.cur.execute('''
        SELECT matches.link, matches.team1_id,
            matches.team2_id, matches.match_id,
            games.result, games.game_id,
            drafts.team, drafts.character_id
        
        FROM matches, games, drafts 
        
        ON matches.match_id == ? AND drafts.game_id = games.game_id
            AND games.match_id = matches.match_id''', (_id,))

    try:
        return next(matchesFromCur(bar.cur))
    except: return None


def matchesFromCur(cur):
    """Slave function for matches' generators

    Args:
        cur (cursor): sqlite cursor

    Yields:
        Match: match
    """
    # first
    first = next(cur)
    match = Match.empty(*first[:4])
    game = Game.empty(*first[4:6])
    game.drafts[first[6]].addCharacter(first[7])
    
    # other
    for row in cur:
        if row[5] != game.id:
            match.addGame(game)
            game = Game.empty(*row[4:6])
        
        game.drafts[row[6]].addCharacter(row[7])
        
        if row[3] != match.id:
            yield match
            match = Match.empty(*row[:4])
    
    match.addGame(game)
    yield match