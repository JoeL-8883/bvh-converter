from __future__ import print_function, division
import sys
import csv
import argparse
import os
import io

from bvh_converter.bvhplayer_skeleton import process_bvhfile, process_bvhkeyframe

"""
Based on: http://www.dcs.shef.ac.uk/intranet/research/public/resmes/CS0111.pdf

Notes:
 - For each frame we have to recalculate from root
 - End sites are semi important (used to calculate length of the toe? vectors)
"""


def open_csv(filename, mode='r'):
    """Open a csv file in proper mode depending on Python version."""
    if sys.version_info < (3,):
        return io.open(filename, mode=mode+'b')
    else:
        return io.open(filename, mode=mode, newline='')
    

def main():
    parser = argparse.ArgumentParser(
        description="Extract joint location and optionally rotation data from BVH file format.")
    parser.add_argument("-i", "--filename", type=str, help='BVH file for conversion.')
    parser.add_argument("-f", "--foldername", type=str, help='Folder to output CSV files to.')
    parser.add_argument("-r", "--rotation", action='store_true', help='Write rotations to CSV as well.')
    args = parser.parse_args()

    file_in = args.filename
    folder = args.foldername
    do_rotations = args.rotation

    if folder:
        if not os.path.exists(folder):
            print("Error: folder {} not found.".format(folder))
            sys.exit(0)
        file_in = folder
    elif not os.path.exists(file_in):
        print("Error: file {} not found.".format(file_in))
        sys.exit(0)
    
    if folder:
        print("Output folder: {}".format(folder))
        
        # Iterate through each BvH file
        for bvh in os.listdir(folder):
            if bvh.endswith(".bvh"):
                
                # Get the directory of the file
                directory = os.path.join(folder, bvh)
                

    else:
        print("Input filename: {}".format(file_in))
        other_s = process_bvhfile(file_in)

    print("Analyzing frames...")
    for i in range(other_s.frames):
        new_frame = process_bvhkeyframe(other_s.keyframes[i], other_s.root,
                                        other_s.dt * i)
    print("done")
    
    file_out = file_in[:-4] + "_worldpos.csv"

    with open_csv(file_out, 'w') as f:
        writer = csv.writer(f)
        header, frames = other_s.get_frames_worldpos()
        writer.writerow(header)
        for frame in frames:
            writer.writerow(frame)
    print("World Positions Output file: {}".format(file_out))

    if do_rotations:
        file_out = file_in[:-4] + "_rotations.csv"
    
        with open_csv(file_out, 'w') as f:
            writer = csv.writer(f)
            header, frames = other_s.get_frames_rotations()
            writer.writerow(header)
            for frame in frames:
                writer.writerow(frame)
        print("Rotations Output file: {}".format(file_out))


if __name__ == "__main__":
    main()
