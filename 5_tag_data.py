import os
import re
from gr_nlp_toolkit import Pipeline

def main():
    folder = "./data/full_interviews_clean/"
    out_folder = "./data/tagged_dataset/"

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    nlp = Pipeline("pos")

    for file in os.listdir(folder):
        fileName = os.fsdecode(file)
        if fileName.endswith(".txt"):
            continue

        speakers = dict()
        with open(folder+file, 'r', encoding="UTF-8") as f:
            for line in f.readlines():
                text = re.match(r"\s*?\\item\[(.*?)\](.*)\n", line)
                try:
                    data = ""
                    tagged = nlp(text.group(2))
                    for token in tagged.tokens:
                        data = data + token.text + "." + token.upos
                        morph_tags = [token.feats[key] for key in token.feats.keys()]
                        tags = ""
                        for tag in morph_tags:
                            if tag == "_":
                                continue
                            else:
                                tags = tags  + "." + tag
                        data = data + tags + " "
                    if text.group(1).lower() in speakers:
                        speakers[text.group(1).lower()].append(data)
                    else:
                        speakers[text.group(1).lower()] = [data]
                except:
                    continue

        for speaker in speakers:
            with open(out_folder + fileName.split("-")[1] + "_" + speaker.replace(".", "").strip() + ".txt", 'w', encoding="UTF-8") as fout:
                for line in speakers[speaker]:
                    fout.write(line + "\n")


if __name__ == "__main__":
    main()