#!/usr/bin/python3

# Iteratively create n frames where n=input.width
# Take column of pixels input.x from input frame i where i=newframe.x
#   and input.x = newframe.i

import os
import argparse
from PIL import Image

from multiprocessing.dummy import Pool

THREADS   = 12
CHUNKSIZE = 4

def getcol(c):
    with Image.open(args.i+c[1]) as oim:
        col = oim.crop((c[0], 0, c[0]+1, height))
    return col
    

def buildframe(i):
    print('...frame', f'{i+1:04} of', width, end='\r')
    with Image.new('RGBA', (len(oldframes), height)) as nim:
        # Iteratively take columns from each input frame
        cols = [(i,frame) for frame in oldframes]
        
        with Pool(THREADS) as pool:
            coldata = pool.map(getcol, cols, CHUNKSIZE)
        
        for j, x in enumerate(coldata):
            nim.paste(x, (j,0,j+1,height))
            
        nim.save(args.o+f'{i:04}.png')

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input directory', required=True)
parser.add_argument('-o', help='output directory', required=True)
parser.add_argument('-s', help='skip n frames', type=int, default=0)

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

with Image.open(args.i+oldframes[0]) as f:
    width  = f.width 
    height = f.height

print('Processing')
for i in range(args.s, width):
    buildframe(i)

    
