#!/usr/bin/python3

# txpy by eax

# Iteratively create n frames where n=input.width
# Take column of pixels input.x from input frame i where i=newframe.x
#   and input.x = newframe.i

import os
import argparse
from PIL import Image

from multiprocessing.dummy import Pool

THREADS   = 12
CHUNKSIZE = 4

# Parameter c: tuple (index #, filename)
def getline(c):
    with Image.open(args.i+c[1]) as oim:
        if args.d == 'r':
            line = oim.crop((c[0], 0, c[0]+1, height))
        elif args.d == 'l':
            line = oim.crop((width-c[0], 0, width-c[0]+1, height))
        elif args.d == 'd':
            line = oim.crop((0, c[0], width, c[0]+1))
        elif args.d == 'u':
            line = oim.crop((0, height-c[0], width, height-c[0]+1))
    return line

def buildframe(i):
    print('...frame', f'{i+1:04} of', frange[-1], end='\r')
    
    if args.d == 'r' or args.d == 'l':
        dimensions = (len(oldframes), height)
    elif args.d == 'd' or args.d == 'u':
        dimensions = (width, len(oldframes))
    
    with Image.new('RGBA', dimensions) as nim:
        # Iteratively take lines from each input frame
        cols = [(i,frame) for frame in oldframes]
        
        with Pool(THREADS) as pool:
            coldata = pool.map(getline, cols, CHUNKSIZE)
        
        for j, x in enumerate(coldata):
            if args.d == 'r':
                nim.paste(x, (j,0,j+1,height))
            elif args.d == 'l':
                nim.paste(x, (width-j,0,width-j+1,height))
            elif args.d == 'd':
                nim.paste(x, (0,j,width,j+1))
            elif args.d == 'u':
                nim.paste(x, (0,height-j,width,height-j+1))
            
        nim.save(args.o+f'{i:04}.png')

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input directory', required=True)
parser.add_argument('-o', help='output directory', required=True)
parser.add_argument('-s', help='skip n frames', type=int, default=0)
parser.add_argument('-d', help='direction (left/right/up/down)', 
                    choices=['l','r','u','d'], default='r')

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

if args.d == 'r' or args.d == 'l':
    frange = range(args.s, width)
elif args.d == 'd' or args.d == 'u':
    frange = range(args.s, height)
    
print('Processing')
for i in frange:
    buildframe(i)

    
