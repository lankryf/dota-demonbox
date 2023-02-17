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

from tools.Supplier import Proxima

class Web(Father):

    flags = ('f')
    hints = {None: (), "proxycheck": ()}

    @staticmethod
    def body(wp:Workplace, cmd:Command):
        match cmd.mode:
            case None:
                wp.hog.info(f"Proxies: {wp.web.proxies}")
            
            case "proxycheck":
                proxima = Proxima(wp.web.proxies)
                nonworking, working = proxima.checkWorkingProxies("https://www.google.com")
                for proxy in nonworking:
                    wp.hog.err(f"Proxy {proxy} isn't working")
                wp.hog.info(f"Proxies that work {len(working)}/{len(working)+len(nonworking)}")

                if 'f' in cmd.flags:
                    wp.web.setProxies(working)
                    wp.web.save()
                    wp.hog.ok("Proxies have been fixed!")
                
                wp.hog.done("Proxy checking has been done.")