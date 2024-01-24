from ctgp7tools.mystuff.character import v1
from ctgp7tools.misc.csarData import *
from ctgp7tools import vprint
from ctgp7tools.misc.sarc import SARC
from ctgp7tools.misc.gameEnum import *
from ctgp7tools.misc.cwav import CWAV
from ioHelper import IOHelper

import os, shutil

class Character:

    _DRIVER_ = ["driver.bcmdl", "driver_lod.bcmdl"]
    _EMBLEM_ = ["emblem.bcmdl", "emblem_lod.bcmdl"]
    _KART_PF = ["body_", "tire_", "wing_", "screw_"]
    _SND_FMT_ = "SND_{:02}_{:02}.bcwav"
    _SND_SPECIAL = ["SND_go.bcwav","SND_select.bcwav"]
    _SUFFIX_ = ".chpack"

    sarc = SARC()

    def __init__(self, path=None):
        if path:
            self.load(path)
    
    def load(self, path):
        with open(path, "rb") as f:
            self.sarc = SARC(IOHelper(f))
        
        if not self.sarc.hasFile("config.ini"):
            raise Exception("SARC doesn't contain 'config.ini'.")
        
        keys = self.sarc.getFile("config.ini").data.decode("utf-8","replace")
        keys = keys.split("\n")

        self.cfgkeys = {}
        for i in keys:
            if i.strip()=="": continue
            kn, *kv = i.split("::")
            self.cfgkeys[kn.strip()] = []
            for j in kv:
                self.cfgkeys[kn.strip()].append(j.strip())
        
        self.cfg_origChar = self.cfgkeys["origChar"][0]

        self.driver = []
        for i in self._DRIVER_:
            if self.sarc.hasFile(i):
                self.driver.append(i)
        
        self.karts = []
        
        for i in BodyNames:
            n = f"{self._KART_PF[0]}{i}.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)
            n = f"{self._KART_PF[0]}{i}_lod.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)
            n = f"{self._KART_PF[0]}{i}_shadow.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)

        for i in TireNames:
            n = f"{self._KART_PF[1]}{i}.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)
            n = f"{self._KART_PF[1]}{i}_lod.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)
            n = f"{self._KART_PF[1]}{i}_shadow.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)

        for i in WingNames:
            n = f"{self._KART_PF[2]}{i}.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)
            n = f"{self._KART_PF[2]}{i}_lod.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)

        for i in ScrewNames:
            n = f"{self._KART_PF[3]}{i}.bcmdl"
            if self.sarc.hasFile(n):
                self.karts.append(n)

        for i in self._EMBLEM_:
            if self.sarc.hasFile(i):
                self.karts.append(i)

        self.thankyou_anim = self.sarc.hasFile("thankyou_anim.bcmdl")
        self.stdWingColor = self.sarc.hasFile("stdWingColor.ips")

        charID = CharacterUINames.index(self.cfg_origChar)
        bcso = BCSAR_ORDER[charID]

        self.sounds = []
        for warc in range(bcso[0],bcso[0]+bcso[1]):
            for sid in range(len(CWAV_OFF[warc])):
                n = self._SND_FMT_.format(warc,sid)
                if self.sarc.hasFile(n):
                    self.sounds.append(n)
        
        if bcso[2]>0:
            warc = bcso[2]
            for sid in range(len(CWAV_OFF[warc])):
                n = self._SND_FMT_.format(warc,sid)
                if self.sarc.hasFile(n):
                    self.sounds.append(n)

        for i in self._SND_SPECIAL:
            if self.sarc.hasFile(i):
                self.sounds.append(i)
def v1GetIconAndConvertIfNeeded(name:str, ifmt:str, size:tuple, src:v1.Character, baseSize:int, hasBclimTool:bool):
    if not src.ui_assets.hasFile(name):
        raise Exception("File doesn't exist in source data")
    data = src.ui_assets.getFile(name).data
    if len(data) != baseSize and len(data) != (baseSize + 32): # CRYP
        if hasBclimTool:
            from PIL import Image
            print(f"## NOTE: {name}: Bad size - adjusting data!")
            vprint("Converting image data to PNG...")
            with open(os.path.join("temp","c.bclim"),"wb") as f:
                f.write(data)
            os.system("bclimtool -dvfp temp{0}c.bclim temp{0}c.png".format(os.sep))
            vprint("Manipulating image data...")
            im = Image.open(os.path.join("temp","c.png"))
            im.copy().resize(size).save(os.path.join("temp","d.png"))
            im.close()
            vprint("Creating and reading BCLIM...")
            os.system("bclimtool -cvtfp {1} temp{0}c.bclim temp{0}d.png".format(os.sep, ifmt))
            with open(os.path.join("temp","c.bclim"),"rb") as f:
                data = f.read()
        else:
            raise Exception("Bad file size - Ensure BCLIM is in proper format")
    return data

def convertV1(src:v1.Character, bcsp, hasBclimTool=False):
    """
    `src` — v1 Character object
    
    `bcsp` — Path to BCSAR / extData (romfs:/Sound)

    `hasBclimTool` — use bclimtool to adjust graphics if they're bad
    """
    cr = src.charRoot
    charID = CharacterUINames.index(src.cfg_origChar)
    isShyGuy = src.cfg_origChar[:2]=="sh"
    charMainName = "sh_red" if isShyGuy else src.cfg_origChar
    sarc = SARC()

    os.makedirs("temp", exist_ok=True)

    sarc.setFile("config.ini", os.path.join(cr, "config.ini"), True)
    sarc.setFile("stdWingColor.ips", os.path.join(cr, "stdWingColor.ips"))
    if isShyGuy:
        sarc.setFile("driver.bcmdl", os.path.join(cr, "Driver", "sh", f"sh_red.bcmdl"))
        sarc.setFile("driver_lod.bcmdl", os.path.join(cr, "Driver", "sh_lod", f"sh_lod_red.bcmdl"))
        sarc.setFile("emblem.bcmdl", os.path.join(cr, "Kart", "Emblem", f"emblem_sh", f"emblem_sh.bcmdl"))
        sarc.setFile("emblem_lod.bcmdl", os.path.join(cr, "Kart", "Emblem", f"emblem_sh_lod", f"emblem_sh_lod.bcmdl"))
    else:
        sarc.setFile("driver.bcmdl", os.path.join(cr, "Driver", charMainName, f"{charMainName}.bcmdl"))
        sarc.setFile("driver_lod.bcmdl", os.path.join(cr, "Driver", f"{charMainName}_lod", f"{charMainName}_lod.bcmdl"))
        sarc.setFile("emblem.bcmdl", os.path.join(cr, "Kart", "Emblem", f"emblem_{charMainName}", f"emblem_{charMainName}.bcmdl"))
        sarc.setFile("emblem_lod.bcmdl", os.path.join(cr, "Kart", "Emblem", f"emblem_{charMainName}_lod", f"emblem_{charMainName}_lod.bcmdl"))

    for i in BodyNames:
        p = [f"body_{i}.bcmdl", os.path.join(cr, "Kart", "Body", f"body_{i}", f"body_{i}_{charMainName}.bcmdl")]
        sarc.setFile(*p)
        if not sarc.hasFile(p[0]):
            p = [f"body_{i}.bcmdl", os.path.join(cr, "Kart", "Body", f"body_{i}", f"body_{i}.bcmdl")]
            sarc.setFile(*p)
        p = [f"body_{i}_lod.bcmdl", os.path.join(cr, "Kart", "Body", f"body_{i}_lod", f"body_{i}_lod_{charMainName}.bcmdl")]
        sarc.setFile(*p)
        if not sarc.hasFile(p[0]):
            p = [f"body_{i}_lod.bcmdl", os.path.join(cr, "Kart", "Body", f"body_{i}_lod", f"body_{i}_lod.bcmdl")]
            sarc.setFile(*p)
        p = [f"body_{i}_shadow.bcmdl", os.path.join(cr, "Kart", "Body", f"body_{i}_shadow", f"body_{i}_shadow.bcmdl")]
        sarc.setFile(*p)

    for i in TireNames:
        p = [f"tire_{i}.bcmdl", os.path.join(cr, "Kart", "Tire", f"tire_{i}", f"tire_{i}.bcmdl")]
        sarc.setFile(*p)
        p = [f"tire_{i}_lod.bcmdl", os.path.join(cr, "Kart", "Tire", f"tire_{i}_lod", f"tire_{i}_lod.bcmdl")]
        sarc.setFile(*p)
        p = [f"tire_{i}_shadow.bcmdl", os.path.join(cr, "Kart", "Tire", f"tire_{i}_shadow", f"tire_{i}_shadow.bcmdl")]
        sarc.setFile(*p)

    for i in WingNames:
        p = [f"wing_{i}.bcmdl", os.path.join(cr, "Kart", "Wing", f"wing_{i}", f"wing_{i}_{charMainName}.bcmdl")]
        sarc.setFile(*p)
        if not sarc.hasFile(p[0]):
            p = [f"wing_{i}.bcmdl", os.path.join(cr, "Kart", "Wing", f"wing_{i}", f"wing_{i}.bcmdl")]
            sarc.setFile(*p)
        p = [f"wing_{i}_lod.bcmdl", os.path.join(cr, "Kart", "Wing", f"wing_{i}_lod", f"wing_{i}_lod_{charMainName}.bcmdl")]
        sarc.setFile(*p)
        if not sarc.hasFile(p[0]):
            p = [f"wing_{i}.bcmdl", os.path.join(cr, "Kart", "Wing", f"wing_{i}_lod", f"wing_{i}_lod.bcmdl")]
            sarc.setFile(*p)

    for i in ScrewNames:
        p = [f"screw_{i}.bcmdl", os.path.join(cr, "Kart", "Screw", f"screw_{i}", f"screw_{i}.bcmdl")]
        sarc.setFile(*p)
        p = [f"screw_{i}_lod.bcmdl", os.path.join(cr, "Kart", "Screw", f"screw_{i}_lod", f"screw_{i}_lod.bcmdl")]
        sarc.setFile(*p)

    if src.ui_assets != None:
        p = "Thankyou3D.szs/{0}/{0}.bcmdl".format(src.cfg_origChar)
        if src.ui_assets.hasFile(p):
            sarc.setFile("thankyou_anim.bcmdl", src.ui_assets.getFile(p).data)

        try:
            data = v1GetIconAndConvertIfNeeded(
                f"UI/menu.szs/select_{CharacterNames[charID]}.bclim",
                "RGBA4444", (64,64), src, 0x2028, hasBclimTool
            )
            sarc.setFile("select.bclim", data)
        except Exception as e:
            print("!! WARNING: select.bclim is unusable. Reason: "+str(e))

        try:
            data = v1GetIconAndConvertIfNeeded(
                f"UI/race.szs/map_{CharacterNames[charID]}_r90.bclim",
                "RGBA4444", (32,32), src, 0x828, hasBclimTool
            )
            sarc.setFile("maprace.bclim", data)
        except Exception as e:
            print("!! WARNING: maprace.bclim is unusable. Reason: "+str(e))

        try:
            data = v1GetIconAndConvertIfNeeded(
                f"UI/race.szs/rank_{CharacterNames[charID]}_r90.bclim",
                "RGBA8888", (22,22), src, 0x1028, hasBclimTool
            )
            sarc.setFile("rankrace.bclim", data)
        except Exception as e:
            print("!! WARNING: rankrace.bclim is unusable. Reason: "+str(e))

        try:
            try:
                data = v1GetIconAndConvertIfNeeded(
                    f"UI/menu.szs/rank_{CharacterNames[charID]}.bclim",
                    "RGBA8888", (22,22), src, 0x1028, hasBclimTool
                )
            except Exception as e:
                print("!! UI.sarc/UI/menu.szs/rank_*.bclim unusable, using from trophy.szs instead: {}".format(e))
                data = v1GetIconAndConvertIfNeeded(
                    f"UI/trophy.szs/rank_{CharacterNames[charID]}.bclim",
                    "RGBA8888", (22,22), src, 0x1028, hasBclimTool
                )
            sarc.setFile("rankmenu.bclim", data)
        except Exception as e:
            print("!! WARNING: rankmenu.bclim is unusable. Reason: "+str(e))
    
    if "bcsarSoundData" in src.sounds:
        shutil.copyfile(
            os.path.join(bcsp, "ctr_dash.bcsar"),
            os.path.join("temp","ctr_dash.bcsar")
        )
    if "menuSoundData" in src.sounds:
        shutil.copyfile(
            os.path.join(bcsp, "extData", "GRP_VO_MENU.bcgrp"),
            os.path.join("temp","menu.bcgrp")
        )
    if "voiceSoundData" in src.sounds:
        shutil.copyfile(
            os.path.join(bcsp, "extData", f"GRP_VO_{src.cfg_origChar.upper()}_GOL.bcgrp"),
            os.path.join("temp","voice.bcgrp")
        )
    
    src.patchSound(
        os.path.join("temp","ctr_dash.bcsar"),
        os.path.join("temp","menu.bcgrp"),
        os.path.join("temp","voice.bcgrp")
    )

    bcso = BCSAR_ORDER[charID]

    if "bcsarSoundData" in src.sounds:
        with open(os.path.join("temp","ctr_dash.bcsar"),"rb") as f:
            for warc in range(bcso[0], bcso[0]+bcso[1]):
                for sid in range(len(CWAV_OFF[warc])):
                    f.seek(CWAV_OFF[warc][sid])
                    cw = CWAV(f)
                    sarc.setFile(
                        "SND_{:02}_{:02}.bcwav".format(warc, sid),
                        cw.data
                    )
            if isShyGuy:
                warc = bcso[3]
                sid = 0
                for p in ["SND_select.bcwav","SND_go.bcwav"]:
                        f.seek(CWAV_OFF[warc][sid])
                        cw = CWAV(f)
                        sarc.setFile(p, cw.data)
                        sid += 1
    
    if not isShyGuy:
        if "voiceSoundData" in src.sounds:
            warc = bcso[2]
            if warc>0:
                with open(os.path.join("temp","voice.bcgrp"),"rb") as f:
                    for sid in range(len(CWAV_OFF[warc])):
                        f.seek(CWAV_OFF[warc][sid])
                        cw = CWAV(f)
                        sarc.setFile(
                            "SND_{:02}_{:02}.bcwav".format(warc, sid),
                            cw.data
                        )

        if "menuSoundData" in src.sounds:
            warc = "menu"
            sid = bcso[3]
            if sid>=0:
                with open(os.path.join("temp","menu.bcgrp"),"rb") as f:
                    for p in ["SND_select.bcwav","SND_go.bcwav"]:
                        f.seek(CWAV_OFF[warc][sid])
                        cw = CWAV(f)
                        sarc.setFile(p, cw.data)
                        sid += 1

    return sarc