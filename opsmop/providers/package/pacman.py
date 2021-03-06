# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from opsmop.providers.package.package import Package

TIMEOUT = 3600
VERSION_CHECK = "pacman -Q %s | awk '{print $2}'"
UPDATE_CACHE = "pacman -Syy"
INSTALL = "pacman -S --noconfirm {name}"
UNINSTALL = "pacman -R {name}"

class Pacman(Package):

    
    def _get_version(self):

        version_check = VERSION_CHECK % self.name
        output = self.test(version_check)
        if output is None:
            return None
        return output


    def get_default_timeout(self):

        return TIMEOUT

    def plan(self):

        super().plan()

    def _get_install_command(self):
        return INSTALL.format(name=self.name)

    def apply(self):

        which = None
        if self.should('update_cache'):
            self.do('update_cache')
            self.run(UPDATE_CACHE)
        if self.should('install'):
            self.do('install')
            which = self._get_install_command()
        elif self.should('upgrade'):
            self.do('upgrade')
            which = self._get_install_command()
        elif self.should('remove'):
            self.do('remove')
            which = UNINSTALL.format(name=self.name)

        if which:
            self.run(which)

        return self.ok()
