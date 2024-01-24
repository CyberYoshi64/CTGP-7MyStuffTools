#!/usr/bin/python3

import ctgp7tools
from ctgp7tools.misc.gameEnum import *
import os, sys
from ioHelper import IOHelper
from glob import glob

import argparse

# Root defaults to Citra (base install)
if os.name != "nt":
    root = os.path.expanduser("~/.local/share/citra-emu/sdmc/CTGP-7")
else:
    root = os.path.expandvars("%APPDATA%\\Citra\\sdmc\\CTGP-7")

myst = os.path.join(root, "MyStuff", "Characters")

prgwd = os.path.dirname(__file__)
assets = os.path.join(
    prgwd, "assets/romfs"
)

argp = argparse.ArgumentParser()
argp.add_argument("-r", "--root", metavar="dir", default=root, help="Alternative CTGP-7 root, defaults to standard Citra install")
argp.add_argument("-m", "--mystpath", metavar="dir", default="", help="Alternative MyStuff root, default is '(root)/MyStuff/Characters'")
argp.add_argument("-v", "--verbose", action="store_true", help="Output exactly what's being done")
argp.add_argument("-o", "--output", default="out/{}.chpack", help="Output path; for multiple characters, use '{}'.")
argp.add_argument("-d", "--dir", action="store_true", help="Output path is a folder")
argp.add_argument("-b", "--bclimtool", action="store_true", help="[Experiment] Modify bad BCLIM's using 'bclimtool' (https://github.com/dnasdw/bclimtool)")
argp.add_argument("-c", "--compress", "--combine-dup", action="store_true", help="Merge files with duplicate data")
argp.add_argument("characters", nargs="*", help="If specified, only convert specified characters")

arg = argp.parse_args()
ctgp7tools.VERBOSE = bool(arg.verbose)

root = arg.root
if arg.mystpath=="":
    myst = os.path.join(root, "MyStuff", "Characters")
else:
    myst = arg.mystpath

out:str = arg.output.replace("/",os.sep)
outIsDirectory = bool(arg.dir)

if not len(arg.characters):
    characters = glob("*/", root_dir=myst)
else:
    characters = arg.characters

if out.find("{}")<0 and len(characters)<2:
    argp.error("'{}' not specified; would overwrite data of this batch")

for i in characters:
    p = os.path.join(myst, i)
    if not os.path.exists(p) or not os.path.isdir(p):
        print("!! Not a directory, skipping: {}".format(p))
        continue

    name = i[i.rfind(os.sep,0,-1)+1:]
    if name[-1]==os.sep: name = name[:-1]
    print(name)
    c = ctgp7tools.mystuff.character.v1.Character(p)
    try:
        s = ctgp7tools.mystuff.character.v2.convertV1(
            src = c,
            bcsp = assets,
            hasBclimTool=arg.bclimtool
        )
        if outIsDirectory:
            os.makedirs(out.format(name),exist_ok=True)
            for j in s.sfat.nodes:
                with open(os.path.join(out.format(name), j.humanName), "wb") as f:
                    f.write(j.data)
        else:
            if out.find(os.sep)>=0:
                os.makedirs(out[:out.rfind(os.sep)].format(name),exist_ok=True)
            with open(out.format(name), "wb") as f:
                s.pack(
                    fd = IOHelper(f),
                    combineDup = arg.compress,
                    saveSFNT = False,
                    forcePad = None
                )
    except Exception as e:
        print(f"FAIL: {e}")