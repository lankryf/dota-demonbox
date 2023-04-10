# Copyright 2023 LankryF

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the Lice>nse.

from .Common.CommandFather import *
from database.generators.matchesGenerator import matchesFlow
from Demon.DataFeeder import datasetFromMachesFlow
from Demon import Teacher
import torch
from tools.Termhog.types import Progressbar

class Inspect(Father):

    flags = ('b', 'f')
    hints = {None: (), "matches": (), "demon":(int,)}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        wp.hog.info(f"Starting inspection for {cmd.mode}.")
        match cmd.mode:
            case "matches":
                errors = []
                matchCount = wp.bar.matchCount()
                
                for match in Progressbar(matchesFlow(), matchCount, "INSPECTION"):
                    if len(match) == 0:
                        wp.hog.err(f"Empty match {match.id}")
                        errors.append(match.id)
                        continue
                    
                    for game in match:
                        if len(game.drafts) != 2:
                            wp.hog.err(f"Game {game.id} has {len(game.drafts)} drafts (must be 2)")
                            errors.append(match.id)
                            continue
                        
                        for n, draft in enumerate(game.drafts):
                            if len(draft) != 5:
                                wp.hog.err(f"Draft {n} from game {game.id} has {len(game.drafts)} characters (must be 5)")
                                errors.append(match.id)
                                continue

                wp.hog.info(f"{matchCount - len(errors)}/{matchCount} matches is ok.")
                wp.hog.info(f"We have {len(errors)} errors.")
                
                if 'b' in cmd.flags:
                    wp.bar.backup()
                    wp.hog.ok("Backuped.")
                
                if 'f' in cmd.flags:
                    wp.hog.info("Fixing.")
                    errors = set(errors)
                    for matchId in errors:
                        wp.bar.matchDelete(matchId)
                        wp.hog.ok(f"Match {matchId} has been deleted.")
                    wp.bar.commit()
                    wp.hog.ok("Commited.")

            case 'demon':
                start = cmd.args[0]

                if 'b' not in cmd.flags:
                    start = -start
                dataset = datasetFromMachesFlow(start)
                Teacher.test(wp.demon, dataset, torch.round)
        wp.hog.done("Inspection has been done.")
        wp.hog.progressEnding()