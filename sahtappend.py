#!/usr/bin/python3

from ctgp7tools.misc.sarc import SAHT, SARC
from ctgp7tools.misc.csarData import CWAV_OFF
from ctgp7tools.misc.gameEnum import *
from ioHelper import IOHelper

try:
    with open("test.saht/HashTableC.saht","rb") as f:
        s = SAHT(IOHelper(f))
        if not s.verify("remove"):
            print("!! HashTable has bad keys!")
except Exception as e:
    print("HashTable.saht not found; grab it from EFE or CTR Studio.")
    print("Error: "+str(e))
    exit(1)

if True:
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

    from glob import glob
    for i in glob("*.szs",root_dir="/data/0/data/Citra/sdmc/CTGP-7/gamefs/Course/"):
        n = i[:-4]
        s.add(f"{n}_map.bclim")
        s.add(f"{n}_map2.bclim")
        s.add(f"{n}.bcmdl")
        s.add(f"{n}.kmp")
        s.add(f"{n}.kcl")
        s.add(f"{n}.div")
        s.add(f"{n}.bcfog")
        s.add(f"{n}.bclgt")
        s.add(f"{n}_ch0.bclgt")
        s.add(f"{n}_ch1.bclgt")
        s.add(f"{n}_ch2.bclgt")
        s.add(f"{n}_ch3.bclgt")
        s.add(f"{n}_ch4.bclgt")
        s.add(f"{n}_ch5.bclgt")

        s.add(f"{n}_TL.bclim")
        s.add(f"{n}_BL.bclim")
        s.add(f"{n}_TR.bclim")
        s.add(f"{n}_BR.bclim")

with open("CTGP-7HashTable.saht","wb") as f:
    s.save(IOHelper(f))