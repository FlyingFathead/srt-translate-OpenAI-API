# extract_and_format_subtitles.py

# Script to Extract and Format Subtitles from an SRT File via Command Line
# This script will read an SRT file provided as a command-line argument and 
# output the subtitles in the specified shorthand format.

import pysrt
import sys

def extract_and_format_subtitles(input_file_path):
    # Load the subtitle file
    subs = pysrt.open(input_file_path)
    
    # Prepare the output list
    formatted_subs = []
    
    # Iterate over subtitle objects
    for sub in subs:
        # Clean and format the subtitle text
        cleaned_text = sub.text.replace('\n', ' ')  # Replace newlines with spaces
        formatted_text = f"[{sub.index}] {cleaned_text}"
        formatted_subs.append(formatted_text)
    
    # Join all formatted subtitles into a single string with new lines
    output_text = "\n".join(formatted_subs)
    
    # Output to a text file
    output_file_path = input_file_path.replace('.srt', '_formatted.txt')
    with open(output_file_path, 'w') as f:
        f.write(output_text)
    
    print(f"Formatted subtitle file created successfully: {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py path_to_file.srt")
        sys.exit(1)
    input_file_path = sys.argv[1]
    extract_and_format_subtitles(input_file_path)
