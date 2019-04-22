#!/usr/bin/env python3
# Deskpower - simple way to script upower events

# Copyright (C) 2019 Aidan Williams
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser

import subprocess
import os

import gi
gi.require_version('GLib', '2.0')
from gi.repository import GLib

from pydbus import SystemBus


class Action:
    def __init__(self, command, use_floats=False):
        self.command = command
        self.use_floats = use_floats

    def execute(self, device_properties):
        for key, value in device_properties.items():
            os.environ[f'DP_{key.upper()}'] = str(int(value) if type(value) is float 
                                                  and not self.use_floats else value)
        
        subprocess.Popen(self.command, shell=True)

configdir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
config = configparser.ConfigParser()

file = open(f'{configdir}/deskpower/actions.ini', "r")
config.read_file(file)

file.close()

batt_actions = []
adapter_actions = []

for action in config:
    if not action == "DEFAULT":
        act = Action(config[action].get('Command', ''), config[action].getboolean("UseFloats", False))
        if config[action]["EventType"] == "Battery":
            batt_actions.append(act)
        elif config[action]["EventType"] == "Adapter":
            adapter_actions.append(act)
        elif config[action]["EventType"] == "All":
            adapter_actions.append(act)
            batt_actions.append(act)

bus = SystemBus()
device = bus.get('.UPower', bus.get('.UPower').GetDisplayDevice())

def handle_property_change(interface, properties, args):
    dev_props = device.GetAll("org.freedesktop.UPower.Device")
    # for key, value in dev_props.items():
    #     # shell scripts don't play too nicely with floats
    #     os.environ[f'DP_{key.upper()}'] = str(int(value) if type(value) is float else value)
    
    # check if is state change
    if 'State' in properties:
        for action in adapter_actions:
            action.execute(dev_props)
    elif 'Percentage' in properties:
        for action in batt_actions:
            action.execute(dev_props)

device.PropertiesChanged.connect(handle_property_change)

def main():
    GLib.MainLoop().run()

if __name__ == '__main__':
    main()
