#!/usr/bin/python3

import os
import ctgp7tools
from ctgp7tools.misc.sarc import SARC, SAHT, SFATEntry
from argparse import ArgumentParser
from ioHelper import IOHelper
from glob import glob

vprint = ctgp7tools.vprint

a = ArgumentParser()
a.add_argument("sarc", help="SARC file")
a.add_argument("dir", help="Directory or other SARC")
a.add_argument("--saht", default="", help="SARC Hash Table to use incase of missing SFNT data")
a.add_argument("--mergedup",action="store_true",help="Merge duplicate data")
a.add_argument("--no-sfnt",action="store_false",help="Do not add file names in SFNT")
a.add_argument("--align", metavar="int", default="0", help="Force custom alignment")
a1 = a.add_argument_group("Mode")
a1.add_argument("-u","--update",action="store_true",help="Update files to SARC")
a1.add_argument("-c","--create",action="store_true",help="Delete SARC beforehand if it exists")
a1.add_argument("-x","--extract",action="store_true",help="Extract SARC to directory")
a1.add_argument("-v","--verbose",action="store_true",help="Say a lot that's done")
a1.add_argument("--saht-append",metavar="out",help="Append entries to SAHT when updating files in SARC")

arg = a.parse_args()

ctgp7tools.VERBOSE = arg.verbose

try:    alignment = int(arg.align,0)
except: alignment = None

argclash = arg.update + arg.extract

if not argclash:
    a.error("A mode (-u/-x) must be specified.")

if argclash > 1:
    a.error("Modes (-u/-x) cannot be combined.")

saht = SAHT()
if len(arg.saht) and os.path.exists(arg.saht):
    with open(arg.saht, "rb") as f:
        saht = SAHT(IOHelper(f))

if os.path.exists(arg.sarc) and not arg.create:
    with open(arg.sarc, "rb") as f:
        sarc = SARC(IOHelper(f), saht=saht)
else:
    sarc = SARC()

files = []
if os.path.exists(arg.dir):
    if os.path.isfile(arg.dir):
        raise Exception("Expected folder, not file: "+str(arg.dir))
    else:
        _files = glob("**",root_dir=arg.dir,recursive=True)
        for i in _files:
            if os.path.isfile(os.path.join(arg.dir, i)):
                files.append(i)
        del _files

if arg.extract:
    os.makedirs(arg.dir, exist_ok=False)
    for i in sarc.sfat.nodes:
        vprint(f"Extracting '{i.humanName}' ...")
        n = i.humanName.rfind("/")
        if n>0:
            os.makedirs(os.path.join(arg.dir, i.humanName[:n]),exist_ok=True)
        with open(os.path.join(arg.dir, i.humanName), "wb") as f:
            f.write(i.data)
    exit(0)

if arg.update:
    for i in files:
        n = i.replace("\\","/")
        with open(os.path.join(arg.dir, i),"rb") as f:
            if i[:2]=="0x":
                sarc.setFile(
                    int(i[:i.find(".")] if i.find(".")>0 else i,0),
                    f.read()
                )
            else:
                if arg.saht_append:
                    saht.add(n)
                sarc.setFile(n, f.read())

if arg.saht_append:
    with open(arg.saht_append,"wb") as f:
        saht.save(IOHelper(f))

with open(arg.sarc,"wb") as f:
    sarc.pack(
        fd = IOHelper(f),
        combineDup = arg.mergedup,
        saveSFNT = arg.no_sfnt,
        forcePad = alignment
    )