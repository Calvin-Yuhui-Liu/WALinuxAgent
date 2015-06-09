#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.4+ and Openssl 1.0+
#

import platform
import os
import re
import pwd
import shutil
import tempfile
import subprocess
import socket
import array
import struct
import fcntl
import time
import base64
import azurelinuxagent.logger as logger
import azurelinuxagent.utils.fileutil as fileutil
import azurelinuxagent.utils.shellutil as shellutil
import azurelinuxagent.utils.textutil as textutil
from azurelinuxagent.utils.osutil.default import DefaultOSUtil

class CoreOSOSUtil(DefaultOSUtil):
    def __init(self):
        super(CoreOSOSUtil, self).__init__()
        self.configPath = '/usr/share/oem/waagent.conf'

    def IsSysUser(self, userName):
       #User 'core' is not a sysuser
       if userName == 'core':
           return False
       return super(CoreOSOSUtil, self).isSysUser(userName)

    def IsDhcpEnabled(self):
        return True
    
    def StartNetwork(self) :
        return shellutil.Run("systemctl start systemd-networkd", chk_err=False)
        
    def RestartInterface(self, iface):
        Run("systemctl restart systemd-networkd")

    def RestartSshService(self):
        return shellutil.Run("systemctl restart sshd", chk_err=False)

    def StopDhcpService(self):
        return shellutil.Run("systemctl stop systemd-networkd", chk_err=False)

    def StartDhcpService(self):
        return shellutil.Run("systemctl start systemd-networkd", chk_err=False)

    def GetDhcpProcessId(self):
        ret= shellutil.RunGetOutput("pidof systemd-networkd")
        return ret[1] if ret[0] == 0 else None
    
    def OnDeprovisionStart(self):
        print "WARNING! /etc/machine-id will be removed."

    def OnDeprovision(self):
        fileutil.RemoveFiles('/etc/machine-id')

    def TranslateCustomData(self, data):
        return base64.b64decode(data)


