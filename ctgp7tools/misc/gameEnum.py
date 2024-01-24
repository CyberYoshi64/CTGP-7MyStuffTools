from enum import Enum

class CharacterEnum(Enum):
    Bowser = 0
    DonkeyKong = 1
    Daisy = 2
    HoneyQueen = 3
    Koopa = 4
    Luigi = 5
    Lakitu = 6
    Mii = 7
    Mii_Female = 8
    Mario = 9
    MetalMario = 10
    Peach = 11
    Rosalina = 12
    ShyGuy = 13
    Toad = 14
    Wiggler = 15
    Wario = 16
    Yoshi = 17
    Maximum = 18

CharacterNames = [
    "bowser",
    "donkey",
    "daisy",
    "honeyQueen",
    "koopaTroopa",
    "luigi",
    "lakitu",
    "",
    "",
    "mario",
    "metal",
    "peach",
    "rosalina",
    "sh_red",
    "toad",
    "wiggler",
    "wario",
    "yoshi"
]
CharacterUINames = [
    "bw",
    "dk",
    "ds",
    "hq",
    "kt",
    "lg",
    "lk",
    "mim",
    "mif",
    "mr",
    "mtl",
    "pc",
    "rs",
    "sh",
    "td",
    "wig",
    "wr",
    "ys"
]
BodyNames = [
    "std",
    "rally",
    "rbn",
    "egg",
    "dsh",
    "cuc",
    "kpc",
    "boat",
    "hny",
    "sabo",
    "gng",
    "pipe",
    "trn",
    "cld",
    "race",
    "jet",
    "gold"
]
TireNames = [
    "std",
    "big",
    "small",
    "race",
    "classic",
    "sponge",
    "gold",
    "wood",
    "bigRed",
    "mush"
]
WingNames = [
    "std",
    "para",
    "umb",
    "flower",
    "basa",
    "met",
    "gold"
]
ScrewNames = [
    "std"
]
SpecialPartsDriver = [
    CharacterEnum.Daisy.value,
    CharacterEnum.Rosalina.value,
    CharacterEnum.HoneyQueen.value
]
BodyUINames = [
    "std",
    "rally",
    "rib",
    "egg",
    "dsh",
    "cuc",
    "kpc",
    "bot",
    "hny",
    "sab",
    "gng",
    "pip",
    "trn",
    "cld",
    "rac",
    "jet",
    "gld"
]
TireUINames = [
    "std",
    "big",
    "small",
    "rac",
    "cls",
    "spg",
    "gld",
    "wod",
    "red",
    "mus"
]
WingUINames = [
    "std",
    "par",
    "umb",
    "flw",
    "bas",
    "met",
    "gld"
]