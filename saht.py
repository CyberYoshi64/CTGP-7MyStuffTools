#!/usr/bin/python3

from ctgp7tools.misc.sarc import SAHT
from ioHelper import IOHelper
from argparse import ArgumentParser

a = ArgumentParser()
a.add_argument("-s", "--saht", metavar="file", help="SAHT file")
a.add_argument("-t", "--text", metavar="file", help="Text file containing keys")
a.add_argument("-o", "--output", metavar="file", help="Output file (.saht/.txt)")
a.add_argument("-y", "--verify", metavar="type", default="remove", help="'remove'/'fix' bad keys in SAHT")
a.add_argument("-x", "--extract", action="store_true", help="Extract keys from SAHT")
a.add_argument("-a", "--append", action="store_true", help="Append keys to SAHT")
a.add_argument("-c", "--create", action="store_true", help="Create SAHT from keys")
a.add_argument("-r", "--remove", action="store_true", help="Remove keys from SAHT")
a.add_argument("-p", "--print", action="store_true", help="List SAHT keys")
a.add_argument("keys", nargs="*")

args = a.parse_args()

if not (args.extract or args.append or args.create or args.remove or args.print):
    a.error("A mode (-x/-a/-c/-r/-p) must be specified.")

if args.extract + args.append + args.create + args.remove + args.print != 1:
    a.error("-x/-a/-c/-r/-p cannot be combined.")

if not (args.create):
    with open(args.saht, "rb") as f:
        saht = SAHT(IOHelper(f))
        saht.verify("remove")

keys:list = args.keys

if args.extract:
    with open(args.output, "w", encoding="utf-8", errors="ignore", newline="\n") as f:
        f.write("#$SARCHash\n")
        l = []
        for k,n in saht.hashes.items():
            l.append(n)
        l.sort()
        for i in l:
            f.write(f"{i}\n")
    exit(0)

if args.print:
    for k,n in saht.hashes.items():
        print(n)
    exit(0)

with open(args.text, "rb") as f:
    kf = f.read()
    if kf[:4] == b'SAHT':
        s = SAHT(IOHelper(kf))
        s.verify("remove")
        for k,n in s.hashes.items():
            keys.append(n)
    else:
        kf = kf.decode("utf-8","replace").split("\n")
        kf.pop(0)
        try:
            while True: kf.remove("")
        except: pass
        keys += kf

if args.append:
    for i in keys:
        saht.add(i)
    with open(args.output, "wb") as f:
        saht.save(IOHelper(f))
    exit(0)

if args.remove:
    for i in keys:
        saht.remove(i)
    with open(args.output, "wb") as f:
        saht.save(IOHelper(f))
    exit(0)

if args.create:
    saht = SAHT()
    for i in keys:
        saht.add(i)
    with open(args.output, "wb") as f:
        saht.save(IOHelper(f))
    exit(0)
