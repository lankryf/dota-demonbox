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
from sqlite3 import connect

def source(wp:Workplace, cmd:Command):
    wp.hog.info("Starting sourcing.")
    wp.bar.clearWithBackup()
    wp.hog.ok("Backuped and cleared.")
    tables = ["matches", "games", "drafts", "characters", "teams"]
    wp.hog.info(f"Opening {cmd.args[0]} database.")
    with connect(cmd.args[0]) as donor:
        donorcur = donor.cursor()
        
        for table in tables:
            donorcur.execute(f"SELECT * from {table}")
            for donorrow in donorcur:
                wp.bar.cur.execute(
                    f"INSERT INTO {table} VALUES({','.join('?' * len(donorrow))})",
                donorrow)
            wp.hog.ok(f"Table {table} has been copied.")
    wp.bar.commit()
    wp.hog.done("Sourcing has been done.")