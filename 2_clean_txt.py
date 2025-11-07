import os, re
from pathlib import Path

# set path to the directory containing the raw files
directory = "./data/full_interviews_raw/"
# set path to the directory to store clean files
clean = "./data/full_interviews_clean/"

if not os.path.exists(clean):
    os.makedirs(clean)

for file in os.listdir(directory):
    if file.endswith('txt'):
        with open("temp.txt", "w", encoding="UTF-8") as temp:
            with open(directory+file, 'r', encoding="UTF-8") as f:
                for line in f:
                    # remove leading whitespace
                    line = line.lstrip()
                    # remove newline characters
                    line = line.replace("\n", "")

                    line = line.replace(".", ". ")
                    line = line.replace(",", ", ")
                    line = line.replace("!", "! ")
                    line = line.replace("?", "? ")
                    line = line.replace("  ", " ")
                    line = line.replace(" .", ".")
                    line = line.replace(" ,", ",")
                    line = line.replace(" !", "!")
                    line = line.replace(" ?", "?")

                    # if line does not start with speaker initials followed by equals sign append line to previous line
                    if not re.search(r".?.?\=", line):
                        temp.write(" " + line)
                    else:
                        temp.write("\n" + line)
        Path("./temp.txt").rename(clean + file)