# convert_back_to_original.py

# Script to Convert Shorthand Format Back to SRT via Command Line
# This script will take the shorthand text file provided as a command-line argument
# and convert it back into an SRT file with basic timing.

import pysrt
import sys
from datetime import timedelta

def create_srt_from_shorthand(input_file_path):
    subs = []
    
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.strip():
            # Extract the subtitle number and text
            number, text = line.strip().split('] ', 1)
            number = int(number.strip('['))
            
            # Create a new SubRipItem
            sub = pysrt.SubRipItem(index=number, text=text)
            sub.start = timedelta(seconds=(number - 1) * 5)  # Assuming each subtitle lasts 5 seconds
            sub.end = timedelta(seconds=number * 5 - 1)
            subs.append(sub)
    
    # Save the subtitles back into an SRT file
    output_file_path = input_file_path.replace('_formatted.txt', '_restored.srt')
    subs = pysrt.SubRipFile(items=subs)
    subs.save(output_file_path)
    
    print(f"SRT file created from shorthand format successfully: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py path_to_formatted.txt")
        sys.exit(1)
    input_file_path = sys.argv[1]
    create_srt_from_shorthand(input_file_path)