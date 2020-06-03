#!/usr/bin/python3

# Iteratively create n frames where n=input.width
# Take column of pixels input.x from input frame i where i=newframe.x
#   and input.x = newframe.i

import os
import argparse
from PIL import Image

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

with Image.open(args.i+oldframes[0]) as f:
    width  = f.width 
    height = f.height

print('Processing')
for i in range(width):
    print('...frame', f'{i+1:03}', 'of', width, end='\r')
    with Image.new('RGBA', (len(oldframes), height)) as nim:
        
        # Iteratively take columns from each input frame
        for j, oldframe in enumerate(oldframes):
            with Image.open(args.i+oldframe) as oim:
                col = oim.crop((i, 0, i+1, height))
                
                nim.paste(col, (j,0,j+1,height))
        
        nim.save(args.o+f'{i:03}.png') 
    
