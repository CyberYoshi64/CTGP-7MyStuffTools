#!/usr/bin/python3

import ctgp7tools
from ctgp7tools.misc.gameEnum import *
from ctgp7tools.misc.csarData import *
from ctgp7tools.misc.sarc import SARC, SAHT
import os, sys
from ioHelper import IOHelper
from glob import glob

try:
    import shutil
    haveBCLIM = shutil.which("bclimtool") is not None
except:
    haveBCLIM = False


def prepareSAHT():
    s = SAHT()

    for i in CWAV_OFF.keys():
        for j in range(len(CWAV_OFF[i])):
            if type(i) is int:
                s.getAddHash(f"SND_{i:02}_{j:02}.bcwav")

    s.getAddHash("SND_select.bcwav")
    s.getAddHash("SND_go.bcwav")
    s.getAddHash("config.ini")
    s.getAddHash("stdWingColor.ips")
    s.getAddHash("driver.bcmdl")
    s.getAddHash("driver_lod.bcmdl")
    s.getAddHash("emblem.bcmdl")
    s.getAddHash("emblem_lod.bcmdl")
    s.getAddHash("thankyou_anim.bcmdl")
    s.getAddHash("select.bclim")
    s.getAddHash("rankrace.bclim")
    s.getAddHash("rankmenu.bclim")
    s.getAddHash("maprace.bclim")

    for i in BodyNames:
        s.getAddHash(f"body_{i}.bcmdl")
        s.getAddHash(f"body_{i}_lod.bcmdl")
        s.getAddHash(f"body_{i}_shadow.bcmdl")

    for i in TireNames:
        s.getAddHash(f"tire_{i}.bcmdl")
        s.getAddHash(f"tire_{i}_lod.bcmdl")
        s.getAddHash(f"tire_{i}_shadow.bcmdl")

    for i in WingNames:
        s.getAddHash(f"wing_{i}.bcmdl")
        s.getAddHash(f"wing_{i}_lod.bcmdl")

    for i in ScrewNames:
        s.getAddHash(f"screw_{i}.bcmdl")
        s.getAddHash(f"screw_{i}_lod.bcmdl")
    return s

bclim = {
    "select.bclim": ("RGBA4444", (64,64), 0x2028),
    "maprace.bclim": ("RGBA4444", (32,32), 0x828),
    "rankmenu.bclim": ("RGBA8888", (22,22), 0x1028),
    "rankrace.bclim": ("RGBA8888", (22,22), 0x1028)
}

chpackFile = sys.argv[1]

s = prepareSAHT()
c = ctgp7tools.mystuff.character.v2.Character(
    chpackFile
)
if haveBCLIM:
    print("Found bclimtool, using it when needed.")

c.sarc.resolveHumanNames(s)

sarcChanges = False
wasSuccess = False
toRemove = []
toMove = []

# Bruteforce names to try rename otherwise known file names
for i in c.sarc.sfat.nodes:
    if not i.name in s.hashes.keys():
        wasSuccess = False
        for k,n in s.hashes.items():
            nn = n[:n.rfind(".")]
            if c.sarc.hashName(nn) == i.name:
                if c.sarc.hasFile(k):
                    toRemove.append((k, nn))
                    sarcChanges = wasSuccess = True
                    break
                toMove.append((i.name, k, n, nn))
                sarcChanges = wasSuccess = True
                break
            nn = n[:n.rfind(".")]+".bin"
            if c.sarc.hashName(nn) == i.name:
                if c.sarc.hasFile(k):
                    toRemove.append((k, nn))
                    sarcChanges = wasSuccess = True
                    break
                toMove.append((i.name, k, n, nn))
                sarcChanges = wasSuccess = True
                break
            
            for cn in CharacterUINamesFile:
                nn = n[:n.rfind(".")]+"_"+cn
                if c.sarc.hashName(nn) == i.name:
                    if c.sarc.hasFile(k):
                        toRemove.append((k, nn))
                        sarcChanges = wasSuccess = True
                        break
                    toMove.append((i.name, k, n, nn))
                    sarcChanges = wasSuccess = True
                    break
                nn = n[:n.rfind(".")]+"_"+cn+n[n.rfind("."):]
                if c.sarc.hashName(nn) == i.name:
                    if c.sarc.hasFile(k):
                        toRemove.append((k, nn))
                        sarcChanges = wasSuccess = True
                        break
                    toMove.append((i.name, k, n, nn))
                    sarcChanges = wasSuccess = True
                    break
                nn = n[:n.rfind("_lod.")]+"_"+cn+n[n.rfind("_lod."):]
                if c.sarc.hashName(nn) == i.name:
                    if c.sarc.hasFile(k):
                        toRemove.append((k, nn))
                        sarcChanges = wasSuccess = True
                        break
                    toMove.append((i.name, k, n, nn))
                    sarcChanges = wasSuccess = True
                    break
            if wasSuccess:
                break
        else:
            toRemove.append((k, "???"))
            sarcChanges = True

try:
    os.remove("temp/c.bclim")
    os.remove("temp/c.png")
    os.remove("temp/d.png")
    os.rmdir("temp")
except:
    pass

if True:
    for i in toRemove:
        print(f"Remove: {i[0]:08X}.bin ({i[1]})")
        c.sarc.sfat.remove(i[0])
    for i in toMove:
        print(f"Move: {i[0]:08X}.bin ({i[3]}) -> {i[2]}")
        k = c.sarc.sfat.getFile(i[0])
        k.name = i[1]
        k.humanName = i[2]

for i in c.sarc.sfat.nodes:
    if i.humanName in bclim.keys():
        if len(i.data) != bclim[i.humanName][2] and len(i.data) != bclim[i.humanName][2] + 32:
            if haveBCLIM:
                print(f"Corrected image: {i.humanName}")
                from PIL import Image
                os.makedirs("temp", exist_ok=True)
                with open(os.path.join("temp","c.bclim"),"wb") as f:
                    f.write(i.data)
                os.system("bclimtool -dvfp temp{0}c.bclim temp{0}c.png".format(os.sep))
                im = Image.open(os.path.join("temp","c.png"))
                im.copy().resize(bclim[i.humanName][1]).save(os.path.join("temp","d.png"))
                im.close()
                os.system("bclimtool -cvtfp {1} temp{0}c.bclim temp{0}d.png".format(os.sep, bclim[i.humanName][0]))
                with open(os.path.join("temp","c.bclim"),"rb") as f:
                    i.data = f.read()
                sarcChanges = True
            else:
                print(f"!! Cannot fix file {i.humanName}!")

if sarcChanges:
    print("!! Changes were made to the file.")
    try:
        if input("Do you want to overwrite the file? [yN]")[:1].upper()=="Y":
            try: os.remove(chpackFile+".old")
            except: pass
            try: os.rename(chpackFile, chpackFile+".old")
            except: pass
            with open(chpackFile, "wb") as f:
                c.sarc.pack(IOHelper(f), combineDup=True, saveSFNT=False, forcePad=None)
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("An error has occured while saving - changes were discarded")
        print(e)
        try: os.rename(chpackFile+".old", chpackFile)
        except: pass