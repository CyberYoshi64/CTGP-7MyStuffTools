"""
## CTGP-7 MyStuff Character

Version 1 (pre-1.5)
"""

from struct import pack, unpack_from, calcsize
from io import BytesIO, IOBase
from glob import glob
import os

from ioHelper import IOHelper
from ctgp7tools.path import * # type: ignore
from ctgp7tools.misc.ips import IPS # type: ignore
from ctgp7tools.misc.sarc import SARC # type: ignore
from ctgp7tools.misc.gameEnum import CharacterEnum

ConfigCharacters = [
    CharacterEnum.Bowser,
    CharacterEnum.DonkeyKong,
    CharacterEnum.Daisy,
    CharacterEnum.HoneyQueen,
    CharacterEnum.Koopa,
    CharacterEnum.Luigi,
    CharacterEnum.Lakitu,
    CharacterEnum.Mii,
    CharacterEnum.Mario,
    CharacterEnum.MetalMario,
    CharacterEnum.Peach,
    CharacterEnum.Rosalina,
    CharacterEnum.ShyGuy,
    CharacterEnum.Toad,
    CharacterEnum.Wiggler,
    CharacterEnum.Wario,
    CharacterEnum.Yoshi
]

class Config:
    """
    ## Character Manager Configuration
    
    Path: $ROOT/MyStuff/Characters/config.bin
    """

    _STRUCT_ = "<4sI??" + "32s"*len(ConfigCharacters)
    _MAGIC_ = b"CHSV"
    _VERSION_ = 2

    forcePatch = False
    """
    Forces the CTGP-7 modpack to refresh the gamefs

    NOTE: You can also create the following file to enable it regardless:
    $ROOT/config/forcePatch.flag
    """

    enableKarts = False
    """
    Enable custom kart patching

    After patching, this flag only replaces the MSBT text for the kart parts
    """

    characterNames = []

    def __init__(self, data=None):
        self.forcePatch = True
        self.enableKarts = True
        self.characterNames = []
        if data: self.load(data)
    
    def load(self, data):
        if isinstance(data, IOBase):
            rawData = data.read(calcsize(self._STRUCT_))
        elif type(data)==bytes:
            rawData = bytes(data)
        else:
            raise Exception("Input data not supported.")

        magic, version, self.forcePatch, self.enableKarts, *rawNames = \
            unpack_from(self._STRUCT_, rawData)
        
        if magic != self._MAGIC_:
            raise Exception("Incompatible file or bad file signature.")

        if version != 2:
            raise Exception(f"Incompatible version. Expected version 2, not {version}.")

        self.characterNames = []
        for i in rawNames:
            self.characterNames.append(i.decode("utf-8","replace").strip())
    
    def str(self):
        s = f"""CTGP-7 Character Manager Config [
    Force gamefs patch : {self.forcePatch}
    Enable custom karts: {self.enableKarts}
    Character Names:
"""
        for i in range(len(ConfigCharacters)):
            s += f"        {CharacterEnum(i).name.ljust(10)} : {self.characterNames[i]}\n"
        return s + "]"

class Character:
    
    cfgkeys = {}        # $CHARROOT/config.ini
    cfg_origChar = ""   # cfgkeys["origChar"][0]
    charRoot = ""

    driver = []         # $CHARROOT/Driver
    kart = []           # $CHARROOT/Kart/**
    sounds = []         # $CHARROOT/*SoundData.ips
    stdWingColor = None # $CHARROOT/stdWingColor.ips
    ui_assets = None    # $CHARROOT/UI.sarc
    
    def __init__(self, path=None):
        if path:
            self.load(path)
    
    def load(self, path):
        self.charRoot = path
        with open(os.path.join(path, "config.ini"), "r", encoding="utf-8", errors="replace") as f:
            keys = f.read()
        
        keys = keys.split("\n")

        self.cfgkeys = {}
        for i in keys:
            if i.strip()=="": continue
            kn, *kv = i.split("::")
            self.cfgkeys[kn.strip()] = []
            for j in kv:
                self.cfgkeys[kn.strip()].append(j.strip())
        
        self.cfg_origChar = self.cfgkeys["origChar"][0]

        self.driver = glob("**/*.*", root_dir=path+"/Driver", recursive=True)
        self.kart = glob("**/*.*", root_dir=path+"/Kart", recursive=True)
        sounds = glob("*SoundData.ips", root_dir=path)

        self.sounds = {}
        for i in sounds:
            with open(os.path.join(path,i), "rb") as f:
                self.sounds[i[:-4]] = f.read()
        
        uiPath = os.path.join(path, "UI.sarc")
        self.ui_assets = None
        if os.path.exists(uiPath):
            with open(uiPath, "rb") as f:
                self.ui_assets = SARC(IOHelper(f))

        self.stdWingColor = None
        try:
            with open(os.path.join(path, "stdWingColor.ips"), "rb") as f:
                self.stdWingColor = f.read()
        except: 
            pass

    def patchSound(self, bcsar:str, menugrp:str, voicegrp:str):
        if "bcsarSoundData" in self.sounds:
            with open(bcsar, "r+b") as f:
                IPS.patch(f, self.sounds["bcsarSoundData"])
        if "menuSoundData" in self.sounds:
            with open(menugrp, "r+b") as f:
                IPS.patch(f, self.sounds["menuSoundData"])
        if "voiceSoundData" in self.sounds:
            with open(voicegrp, "r+b") as f:
                IPS.patch(f, self.sounds["voiceSoundData"])
        