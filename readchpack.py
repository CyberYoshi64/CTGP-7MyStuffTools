#!/usr/bin/python3

import ctgp7tools
from ctgp7tools.misc.gameEnum import *
import os, sys
from ioHelper import IOHelper
from glob import glob

import shutil

shutil.rmtree("temp", True)
c = ctgp7tools.mystuff.character.v2.Character(
    sys.argv[1]
)

print("Config: ",c.cfgkeys)
print("Driver: ",len(c.driver))
print("Karts: ",len(c.karts))
print("Has stdWingColor? ",c.stdWingColor)
print("Has thankyou_anim? ",c.thankyou_anim)
print("Sounds: ",len(c.sounds))