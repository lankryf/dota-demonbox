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

def stringsInside(text:str, start:str, end:str, funcForInsides=lambda x: x) -> list[str]:
    """Gets text inside patterns (start, end) without including patterns.
    Has transformation functioin for each result inside list.

    Args:
        text (str): Source text
        start (str): Start text patern 
        end (str): End text patern
        funcForInsides (function, optional): Transformation functioin. Defaults to lambdax:x.

    Returns:
        list[str]: List of results
    """
    return [funcForInsides(t.split(end, 1)[0]) for t in text.split(start)[1:]]