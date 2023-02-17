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
from tools.Supplier.types import Match
from workplace.Workplace import Workplace
from .DataFeeder import draftsCategorical, teamsCategorical, packInputs

__all__ = ["predictMatch"]

def predictMatch(match:Match) -> float:
    wp = Workplace()
    inps = packInputs(draftsCategorical(match[0], wp.bar.characterMaxId()+1), teamsCategorical(match, wp.bar.teamMaxId()+1))
    return wp.aimodel.predict(inps, verbose=0)