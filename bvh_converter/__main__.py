from __future__ import print_function, division
import sys
import csv
import argparse
import os
import io
import time

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
    
<<<<<<< HEAD
def process(other_s, file_in):
=======

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
>>>>>>> 70cbc0ab253499600250fdaad43b7ff4ec855c31
    for i in range(other_s.frames):
        new_frame = process_bvhkeyframe(other_s.keyframes[i], other_s.root,
                                        other_s.dt * i)
    
    # Create an output folder if there isn't one
    if not os.path.exists("output"):
        os.makedirs("output")
    
    file_out = "output/" + file_in.split("/")[-1][:-4] + ".csv"
    with open_csv(file_out, 'w') as f:
        writer = csv.writer(f)
        header, frames = other_s.get_frames_worldpos()
        writer.writerow(header)
        for frame in frames:
            writer.writerow(frame)

def main():
    parser = argparse.ArgumentParser(
        description="Extract joint location and optionally rotation data from BVH file format.")
    parser.add_argument("-f", "--filename", type=str, help='BVH file for conversion.')
    parser.add_argument("-d", "--foldername", type=str, help='Folder to output CSV files to.')
    parser.add_argument("-r", "--rotation", action='store_true', help='Write rotations to CSV as well.')
    args = parser.parse_args()

    file_in = args.filename
    folder_in = args.foldername
    corrupted = []

    if folder_in:
        if not os.path.exists(folder_in):
            print("Error: folder {} not found.".format(folder_in))
            sys.exit(0)

        print("Output folder: {}".format(folder_in))
        counter = 0
        for bvh in os.listdir(folder_in):
            bvh_dir = os.path.join(folder_in, bvh)
            try: 
                other_s = process_bvhfile(bvh_dir)
                process(other_s, bvh_dir)
                print(bvh_dir)
                counter += 1
            # Deleted corrupted(?) files
            except StopIteration:
                number = os.path.splitext(os.path.basename(bvh_dir))[0]
                print(f"File  {number} is corrupted.")
                corrupted.append(number)
                if os.path.exists(bvh_dir):
                    os.remove(bvh_dir)
                continue
        
        print("Conversion finished.")
        print(f"{len(corrupted)} Corrupted files")
        print(f"{counter} Files converted")
        print(corrupted)
    else:
        if not os.path.exists(file_in):
            print("Error: file {} not found.".format(file_in))
            sys.exit(0)
        print("Output file: {}".format(file_in))
        
        other_s = process_bvhfile(file_in)
        process(other_s, file_in)

    
if __name__ == "__main__":
    main()
