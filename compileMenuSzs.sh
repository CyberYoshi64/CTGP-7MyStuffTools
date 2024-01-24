#!/bin/bash

CCWD="$PWD"

cd "$CCWD/modded/CTGP-7.sarc.edit"
for i in $(find * | grep .bclim); do
    bclimtool -evfp $i ../CTGP-7.sarc.d/$i.png
done

cd "$CCWD/modded/menu.szs.edit"
for i in *.bclim; do
    bclimtool -evfp $i ../menu.szs.d/$i.png
done

cd "$CCWD/modded/race.szs.edit"
for i in *.bclim; do
    bclimtool -evfp $i ../race.szs.d/$i.png
done

cd "$CCWD/modded/common.szs.edit"
for i in *.bclim; do
    bclimtool -evfp $i ../common.szs.d/$i.png
done

cd "$CCWD/modded"
cp -f CTGP-7.sarc CTGP-7-m.sarc
yaz0dec menu.szs
mv menu.szs_0.dec menu.sarc
yaz0dec race.szs
mv race.szs_0.dec race.sarc
yaz0dec common.szs
mv common.szs_0.dec common.sarc

cd $CCWD
./sarctool.py -u modded/menu.sarc modded/menu.szs.edit --no-sfnt
./sarctool.py -u modded/race.sarc modded/race.szs.edit --no-sfnt
./sarctool.py -u modded/common.sarc modded/common.szs.edit --no-sfnt
./sarctool.py -u modded/CTGP-7-m.sarc modded/CTGP-7.sarc.edit --no-sfnt --mergedup

yaz0enc modded/menu.sarc
yaz0enc modded/race.sarc
yaz0enc modded/common.sarc

mv modded/menu.sarc.yaz0 /data/0/data/Citra/sdmc/CTGP-7/gamefs/UI/menu.szs
mv modded/race.sarc.yaz0 /data/0/data/Citra/sdmc/CTGP-7/gamefs/UI/race.szs
mv modded/common.sarc.yaz0 /data/0/data/Citra/sdmc/CTGP-7/gamefs/UI/common.szs
mv modded/CTGP-7-m.sarc /data/0/data/Citra/sdmc/CTGP-7/resources/CTGP-7.sarc
