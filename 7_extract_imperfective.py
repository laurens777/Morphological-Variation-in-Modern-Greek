import os
import pandas as pd
import re

def main():
    token_count = 0
    df = get_info("./speakerInfo2.csv")
    rules = readPhonRules("./phonRules.txt")

    with open("output_imperfective.csv", encoding="UTF-8", mode="w") as output:
        output.write("speaker_id,orthography,gloss,stem,gender,dialect_area,origin\n")

        for file in os.listdir("./data/"):
            fileName = os.fsdecode(file)
            speaker_id = fileName.split("_")[0]
            print(speaker_id)
            print(str(df.loc[df['Informant_ID'] == speaker_id, 'Dialect_Area'].item()))

            with open ("./data/" + file, "r", encoding="UTF-8") as f:
                dialectal_count = 0
                standard_count = 0
                text_data = f.readlines()
                for line in text_data:
                    tokens = line.split(" ")
                    for token in tokens:
                        data = token.split(".")
                        if "Past" in data and "Imp" in data and "Act" in data:
                            if re.search("ουσ.{1,3}$", data[0]):
                                phon = graphToPhon(data[0], rules)
                                gloss = phon + "." + token.split('.', 1)[1]
                                dialectal_count += 1
                                token_count += 1
                                output.write(str(speaker_id) + ","  + data[0] + "," + gloss + ",ουσ," + str(df.loc[df['Informant_ID'] == speaker_id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Origin'].item()).replace(", ", "/") + "\n")
                            elif re.search("αγ.{1,3}$", data[0]):
                                phon = graphToPhon(data[0], rules)
                                gloss = phon + "." + token.split('.', 1)[1]
                                standard_count += 1
                                token_count += 1
                                output.write(str(speaker_id) + "," + data[0] + "," + gloss + ",γ," + str(df.loc[df['Informant_ID'] == speaker_id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Origin'].item()).replace(", ", "/") + "\n")
                            elif re.search("υν.{1,3}$", data[0]):
                                phon = graphToPhon(data[0], rules)
                                gloss = phon + "." + token.split('.', 1)[1]
                                standard_count += 1
                                token_count += 1
                                output.write(str(speaker_id) + "," + data[0] + "," + gloss + ",ουν," + str(df.loc[df['Informant_ID'] == speaker_id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == speaker_id, 'Origin'].item()).replace(", ", "/") + "\n")

def get_info(file):
    df = pd.read_csv(file)
    df["Informant_ID"] = df["Informant_ID"].apply(lambda x: '{0:0>3}'.format(x))
    return df

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

if __name__ == "__main__":
    main()