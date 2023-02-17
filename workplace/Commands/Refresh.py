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

from .Common.CommandFather import *

from tools.Supplier.getters.Escorenews import Escorenews


class Refresh(Father):

    flags = ('b',)
    hints = {None: ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        wp.hog.info("Starting refreshing.")
        if 'b' in cmd.flags:
            wp.bar.backup()
            wp.hog.ok("Backuped.")
        
        getter = Escorenews(waitingTime=0.5)
        pageNow = 1
        done = False
        matches = [[]]
        while not done:
            wp.hog.info(f"Going to the page {pageNow}...")
            data = reversed(getter.getTrueResults((pageNow,)))
            for match in data:
                if wp.bar.matchIdByLink(match.link):
                    wp.hog.info(f"Match with link {match.link} is already in the database. Stopping...")
                    done = True
                    break
                matches[-1].append(match)
            matches.append([])
            pageNow += 1

        if not matches[0]:
            wp.hog.info("Database is already up to date.")
            return
    
        errors = 0
        numberOfMatches = 0
        for matchesGroup in reversed(matches):
            for match in reversed(matchesGroup):
                wp.hog.ok(f"Match with link {match.link} has been added.")
                added = wp.bar.matchAdd(match)
                if not added:
                    wp.hog.err(f'Match with link "{match.link}" is already in the database. There is error!')
                    errors += 1
                numberOfMatches += 1

        wp.hog.info(f"There are {numberOfMatches} matches have been added.")
        wp.hog.info(f"{errors} errors reported.")
        wp.bar.commit()
        wp.hog.ok("Commited.")
        wp.hog.done("Refreshed!")