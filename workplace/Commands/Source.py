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

from workplace.Commands.Common.CommandFather import *

from tools.BackupsNerd import BackupsNerd
from sqlite3 import connect

class Source(Father):

    flags = ()
    hints = {None: (), "from": (None,)}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        wp.hog.info("Starting sourcing.")
        wp.bar.clearWithBackup()
        wp.hog.ok("Backuped and cleared.")
        
        tables = ["teams", "teams_names",
                "characters","characters_names",
                "matches", "games", "drafts"]
        
        if cmd.mode == 'from':
            donorfile = cmd.args[0]
        else:
            bnerd = BackupsNerd(wp.config['database']['backupsFolder'])
            donorfile = bnerd.lastMarked()
            if not donorfile:
                wp.hog.fatal("There are no marked backups!")
                return


        wp.hog.info(f"Opening {donorfile} database.")
        with connect(donorfile) as donor:
            donorcur = donor.cursor()
            
            for table in wp.hog.progressbar(tables, len(tables), "SOURCING"):
                donorcur.execute(f"SELECT * from {table}")
                for donorrow in donorcur:
                    wp.bar.cur.execute(
                        f"INSERT INTO {table} VALUES({','.join('?' * len(donorrow))})",
                    donorrow)
                wp.hog.ok(f"Table {table} has been copied.")
        wp.bar.commit()
        wp.hog.done("Sourcing has been done.")
        wp.hog.progressEnding()