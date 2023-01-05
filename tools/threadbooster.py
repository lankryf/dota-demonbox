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

from threading import Thread

class ThreadBooster:
    def __init__(self, threadsNumber:int):
        self.__threadsNumber = threadsNumber
        self.__inputs = []
        self.__results = []
        self.__threads = []


    def _addResult(self, data) -> None:
        self.__results.append(data)


    @property
    def results(self):
        return self.__results


    def __makeThreads(self, dose:list) -> None:
        self.__threads = [Thread(target=self.__class__.getResult, args=(self, d)) for d in dose]


    def __getInputsDose(self):
        dose = self.__inputs[:self.__threadsNumber]
        self.__inputs = self.__inputs[self.__threadsNumber:]
        return dose


    def __process(self):
        for thread in self.__threads:
            thread.start()
        for thread in self.__threads:
            thread.join()


    def findInput(self, *args):
        """Executes getInputs function with args, ready to process
        """
        self.__inputs = self.getInputs(*args)


    def __iter__(self):
        return self


    def __next__(self):
        dose = self.__getInputsDose()
        if dose:
            self.__results.clear()
            self.__makeThreads(dose)
            self.__process()
            return self.__results
        else:
            raise StopIteration()