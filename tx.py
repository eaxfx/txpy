#!/usr/bin/python3

# Iteratively create n frames where n=input.width
# Take column of pixels input.x from input frame i where i=newframe.x
#   and input.x = newframe.i

import os
import argparse
from PIL import Image

from multiprocessing.dummy import Pool

THREADS = 8

def buildframe(i):
    print('...frame', f'{i+1:04}', 'of', width)
    with Image.new('RGBA', (len(oldframes), height)) as nim:
        
        # Iteratively take columns from each input frame
        for j, oldframe in enumerate(oldframes):
            with Image.open(args.i+oldframe) as oim:
                col = oim.crop((i, 0, i+1, height))
                
            nim.paste(col, (j,0,j+1,height))
        
        nim.save(args.o+f'{i:04}.png')

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input directory', required=True)
parser.add_argument('-o', help='output name', required=True)

args = parser.parse_args()

# Append '/' to directory names if necessary
if(args.i[-1] != '/'):
    args.i += '/'
if(args.o[-1] != '/'):
    args.o += '/'

oldframes = os.listdir(args.i)

if oldframes == []:
    print('No frames found')
    exit(2)

os.makedirs(args.o, exist_ok=True)

pool = Pool(THREADS)

with Image.open(args.i+oldframes[0]) as f:
    width  = f.width 
    height = f.height

print('Processing')
pool.map(buildframe, range(width))
pool.close()
pool.join()

    
