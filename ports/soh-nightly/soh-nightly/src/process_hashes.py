#!/bin/env/python3
# This ugly script uses mappings from https://github.com/HarbourMasters/Shipwright/blob/ef8fa17e7c748362cafea73132a1e84fe209733b/soh/soh/Extractor/Extract.cpp#L611
# to generate the metadata needed to generate OTR files. Game files are
# required to run the script. This byte swapping script is also needed:
# https://github.com/Brawl345/N64Swap
# The data is outputted in a format that can be pasted straight into otrgen.
# Any missing data can be copied from the previous version of otrgen.

import sys
import subprocess
import os

supported_hashes = ["328a1f1beba30ce5e178f031662019eb32c5f3b5",
"cfbb98d392e4a9d39da8285d10cbef3974c2f012",
"0227d7c0074f2d0ac935631990da8ec5914597b4",
"f46239439f59a2a594ef83cf68ef65043b1bffe2",
"cee6bc3c2a634b41728f2af8da54d9bf8cc14099",
"079b855b943d6ad8bd1eb026c0ed169ecbdac7da",
"50bebedad9e0f10746a52b07239e47fa6c284d03",
"cfecfdc58d650e71a200c81f033de4e6d617a9f6",
"ad69c91157f6705e8ab06c79fe08aad47bb57ba7",
"d3ecb253776cd847a5aa63d859d8c89a2f37b364",
"41b3bdc48d98c48529219919015a1af22f5057c2",
"c892bbda3993e66bd0d56a10ecd30b1ee612210f",
"dbfc81f655187dc6fefd93fa6798face770d579d",
"fa5f5942b27480d60243c2d52c0e93e26b9e6b86",
"b82710ba2bd3b4c6ee8aa1a7e9acf787dfc72e9b",
"8b5d13aac69bfbf989861cfdc50b1d840945fc1d",
"0769c84615422d60f16925cd859593cdfa597f84",
"2ce2d1a9f0534c9cd9fa04ea5317b80da21e5e73",
"dd14e143c4275861fe93ea79d0c02e36ae8c6c2f"]

mapping = {}
mapping["OOT_PAL_GC"] = 0x09465AC3
mapping["OOT_PAL_MQ"] = 0x1D4136F3
mapping["OOT_PAL_GC_DBG1"] = 0x871E1C92 # 03-21-2002 build
mapping["OOT_PAL_GC_DBG2"] = 0x87121EFE # 03-13-2002 build
mapping["OOT_PAL_GC_MQ_DBG"] = 0x917D18F6
mapping["OOT_PAL_10"] = 0xB044B569
mapping["OOT_PAL_11"] = 0xB2055FBD
mapping["OOT_NTSC_US_GC"] = 0xF3DD35BA
mapping["OOT_NTSC_JP_GC"] = 0xF611F4BA
mapping["OOT_NTSC_JP_GC_CE"] = 0xF7F52DB8
mapping["OOT_NTSC_US_MQ"] = 0xF034001A
mapping["OOT_NTSC_JP_MQ"] = 0xF43B45BA
mapping["OOT_NTSC_10"] = 0xEC7011B7
mapping["OOT_NTSC_11"] = 0xD43DA81F
mapping["OOT_NTSC_12"] = 0x693BA2AE

mapping = dict((v,k) for k,v in mapping.items())

mapping2 = {}
mapping2["OOT_PAL_GC"] = "GC_NMQ_PAL_F"
mapping2["OOT_PAL_MQ"] = "GC_MQ_PAL_F"
mapping2["OOT_PAL_GC_DBG1"] = "GC_NMQ_D"
mapping2["OOT_PAL_GC_MQ_DBG"] = "GC_MQ_D"
mapping2["OOT_PAL_10"] = "N64_PAL_10"
mapping2["OOT_PAL_11"] = "N64_PAL_11"
mapping2["OOT_NTSC_US_GC"] = "GC_NMQ_NTSC_U"
mapping2["OOT_NTSC_JP_GC"] = "GC_NMQ_NTSC_J"
mapping2["OOT_NTSC_JP_GC_CE"] = "GC_NMQ_NTSC_J_CE"
mapping2["OOT_NTSC_US_MQ"] = "GC_MQ_NTSC_U"
mapping2["OOT_NTSC_JP_MQ"] = "GC_MQ_NTSC_J"
mapping2["OOT_NTSC_10"] = "N64_NTSC_10"
mapping2["OOT_NTSC_11"] = "N64_NTSC_11"
mapping2["OOT_NTSC_12"] = "N64_NTSC_12"

dirname = "./z64"

hash_mappings = []
dir_mappings = []

for filename in os.listdir(dirname):
    if not filename.endswith('.z64'):
        continue

    print(filename+ ":")
    result = subprocess.run(['shasum', dirname+'/'+filename], stdout=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    bits = out.split()
    shasum = bits[0]
    print("z64: ", shasum)

    result = subprocess.run(["python", "./n64swap.py", dirname+'/'+filename, "rom.v64"])
    result = subprocess.run(['shasum', 'rom.v64'], stdout=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    bits = out.split()
    shasum_v = bits[0]
    print("v64: ", shasum_v)
    hash_mappings.append("    %s) ROMHASH=%s ;;" % (shasum_v, shasum))

    result = subprocess.run(["python", "./n64swap.py", dirname+'/'+filename, "rom.n64"])
    result = subprocess.run(['shasum', 'rom.n64'], stdout=subprocess.PIPE)
    out = result.stdout.decode('ascii')
    bits = out.split()
    shasum_n = bits[0]
    print("n64: ", shasum_n)
    hash_mappings.append("    %s) ROMHASH=%s ;;" % (shasum_n, shasum))

    result = subprocess.run(['xxd', '-p', '-l4', '-s16', dirname+'/'+filename], stdout=subprocess.PIPE)
    crc32 = result.stdout.decode('ascii').strip()
    print(crc32)
    int_crc = int(crc32, 16)
    name1 = mapping[int_crc]
    name2 = mapping2[name1]
    print(name1)
    print(name2)
    if "NMQ" in name2:
        otrname = 'oot.otr'
    elif "MQ" in name2:
        otrname = 'oot-mq.otr'
    else:
        otrname = 'oot.otr'
    dir_mappings.append('    %s) ROM=%s; OTRNAME="%s" ;;' % (shasum, name2, otrname))

    supported_hashes.remove(shasum)

print()

for m in hash_mappings:
    print(m)

for m in dir_mappings:
    print(m)


print('Unprocessed hashes - need to be added manually:')
print(supported_hashes)
