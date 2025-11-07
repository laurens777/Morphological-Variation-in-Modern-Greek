import os, re
from pathlib import Path

# set path to the directory containing the raw files
directory = "./data/full_interviews_raw/"
# set path to the directory where you want to store clean files
clean = "./data/full_interviews_clean/"

if not os.path.exists(clean):
    os.makedirs(clean)

for file in os.listdir(directory):
    if file.endswith('tex'):
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

                    # if line does not start with \item[] then we append it to the last line
                    if not re.search(r"\\item\[.*\]", line):
                        temp.write(" " + line)
                    else:
                        temp.write("\n" + line)
        Path("./temp.txt").rename(clean + file)

# this is to ignore first line of metadata and remove final metadata
# this needs to be reviewed as it may not always work
for file in os.listdir(clean):
    with open(clean+file, 'r', encoding="UTF-8") as fin:
        data = fin.read().splitlines(True)
    with open(clean+file, 'w', encoding="UTF-8") as fout:
        for line in data[1:]:
            line = re.sub(r"\\end\{xlist\} \\end\{document\}", "", line)
            fout.write(line)