import os
from syllabification import syllabify
import pandas as pd
import string

directory = "./data/tagged_dataset/"

def graphToPhon(word, phonRules):
    i = 1
    temp = word
    for rule in phonRules:
        if rule.split()[0] in temp:
            if i <= 37:
                temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
            else:
                temp = temp.replace(rule.split()[0], rule.split()[1].strip("\n").strip())
        i += 1
    return temp

def readPhonRules(path):
    rules = []
    with open(path, encoding="UTF-8") as ruleFile:
        for line in ruleFile:
            rules.append(line)
    return rules

def get_info(file):
    df = pd.read_csv(file)
    df["Informant_ID"] = df["Informant_ID"].apply(lambda x: '{0:0>3}'.format(x))
    return df

rules = readPhonRules("./phonRules.txt")
df = get_info("./speakerInfo.csv")

special_verbs = ["piɣa", "piɣes", "piɣe", "piɣan", "epiɣa", "epiɣes", "epiɣe", "epiɣan", "pira", 
                 "pires", "pire", "piran", "epira", "epires", "epire", "epiran"]

with open("output2.csv", 'w', encoding="UTF-8") as fout:
    for file in os.listdir(directory):
        id, initial = file.split(".")[0].split("_")
        if id not in df.Informant_ID.values:
            with open("missing_id.txt", 'a', encoding="UTF-8") as missing:
                missing.write(id + '\n')
            continue
        with open(directory+file, 'r', encoding="UTF-8") as f:
            for line in f.readlines():
                for tokens in line.split(" "):
                    if tokens[0] == '.':
                        continue
                    elif tokens[0] in string.whitespace:
                        continue
                    wordData = tokens.split(".")
                    orthography = wordData[0]
                    phon = graphToPhon(orthography, rules)
                    gloss = phon + "." + tokens.split('.', 1)[1]
                    if phon in special_verbs:
                        fout.write(str(id) + "," + str(initial) + "," + str(orthography) + "," + str(gloss) + "," + str(df.loc[df['Informant_ID'] == id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Origin'].item()).replace(", ", "/") + "\n")
                        