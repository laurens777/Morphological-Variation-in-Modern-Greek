import os, re

# set directory for input and output
directory = "./data/full_interviews_clean/"
extracts = "./data/full_interviews_extracts/"
# set initials for researchers that should be ignored when extracting text
interviewers = ["ερ", "ερ2", "res", "res1", "res2", "ΧΧ", "χχ"]

if not os.path.exists(extracts):
    os.makedirs(extracts)

for file in os.listdir(directory):
    if file.endswith(".txt"):
        continue
    speakers = {}
    sp_id = file.split("-")[1]
    with open(directory+file, 'r', encoding="UTF-8") as f:
        for line in f:
            match = re.match(r"\\item\[(.*?)\](.*)", line)
            if not match.group(1).lower().replace(".", "") in speakers:
                speakers[match.group(1).lower().replace(".", "")] = [match.group(2)]
            else:
                speakers[match.group(1).lower().replace(".", "")].append(match.group(2))

    for speaker in speakers:
        if speaker in interviewers:
            continue
        else:
            with open(extracts + sp_id + "_" + speaker.replace(".", "") + ".txt", 'w', encoding="UTF-8") as fout:
                for line in speakers[speaker]:
                    fout.write(line.lstrip() + "\n")
