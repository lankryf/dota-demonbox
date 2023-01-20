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

from tools.Workplace.Workplace import Workplace
from tools.Workplace.Command import Command

from tools.Matches.getter import Escorenews

def refresh(wp:Workplace, cmd:Command):
    wp.hog.info("Starting refreshing.")
    if 'b' in cmd.flags:
        wp.bar.backup()
        wp.hog.ok("Backuped.")
    
    getter = Escorenews(wp.config.getint("processing", "threadCount"))
    pageNow = 0
    matches = []
    work = True
    while work:
        pageNow +=1
        getter.loadInput(pageNow)
        for match in getter.flow():
            if wp.bar.matchIdByLink(match.link):
                work = False
                wp.hog.info(f"Match link {match.link} already in database. Upload has been stoped.")
                break
            matches.append(match)
            wp.hog.ok(f"Match link {match.link} will be uploaded.")
    
    if len(matches):
        wp.hog.info("Writing to database.")
        matches.reverse()
        for match in wp.hog.progressbar(matches, len(matches), "WRITING"):
            wp.bar.matchAdd(match)
    
        wp.bar.commit()
        wp.hog.info(f"Commited, {len(matches)} matches have been uploaded.")
    else:
        wp.hog.info(f"Already up to date.")
    wp.hog.done("Refreshed.")
