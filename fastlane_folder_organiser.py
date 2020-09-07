#!/usr/bin/env python3
import sys
import os
import shutil

if len(sys.argv) != 2:
    print("Usage: {} path_to_screenshot_root".format(sys.argv[0]))
    exit(-1)
    
exit("this script has hardcoded paths. Please confirm its source code before running it.")

# You have been warned.
dst = "/Users/gerjo/gerard_uses_hardcoded_paths"


# The objective is to rearrange screenshots as downloaded via fastlane
# deliver. This script will bundle them into a folder per device.
for lang_dir in os.listdir(sys.argv[1]):
    lang_root = os.path.join(sys.argv[1], lang_dir)
    
    if os.path.isdir(lang_root):
    
        for image_name in os.listdir(lang_root):
            image_file = os.path.join(lang_root, image_name)
            filename, extension = os.path.splitext(image_file)
            
            device = "_".join(filename.split("_")[1:-1])
            index = filename.split("_")[-1]
            
            dst_image = "{dst}/{lang_dir}/{device}/{index}{extension}".format(
                dst=dst,lang_dir=lang_dir,device=device,index=index,extension=extension
            )
            
            os.makedirs(os.path.dirname(dst_image), exist_ok=True)
            
            print("copying {} -> {}".format(image_file, dst_image))
            shutil.copyfile(image_file, dst_image)