# compare_subtitles.py

import shutil
import pysrt
import sys

# Define the number of lines to display per comparison segment
LINES_PER_SEGMENT = 30

def print_horizontal_line(character='-', length=None):
    if length is None:
        length = shutil.get_terminal_size().columns
    line = character * length
    print(line)

def compare_subtitles(file_path_a, file_path_b, lines_per_segment):
    # Load subtitle files
    subs_a = pysrt.open(file_path_a)
    subs_b = pysrt.open(file_path_b)

    assert len(subs_a) == len(subs_b), "Subtitle entries do not match between files."

    for i in range(0, len(subs_a), lines_per_segment):
        print_horizontal_line('=')
        print(f"Comparison: Subtitles {i+1} to {min(i + lines_per_segment, len(subs_a))}")
        print_horizontal_line('=')

        for j in range(i, min(i + lines_per_segment, len(subs_a))):
            text_a = subs_a[j].text.replace('\n', ' | ')
            text_b = subs_b[j].text.replace('\n', ' | ')

            max_len = max(len(text_a), len(text_b))

            print(f"Original ({subs_a[j].index}):  {text_a.ljust(max_len)}")
            print(f"Translated ({subs_b[j].index}):  {text_b.ljust(max_len)}")
            print_horizontal_line('-')

        user_input = input("Press Enter to continue to the next segment (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_subtitles.py path/to/subtitle_a.srt path/to/subtitle_b.srt")
        sys.exit(1)

    file_path_a = sys.argv[1]
    file_path_b = sys.argv[2]

    compare_subtitles(file_path_a, file_path_b, LINES_PER_SEGMENT)
