import os
import pandas as pd
import string
import re

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

def syllabify(line,star=True): # can handle multi-word lines including white space
    """
    line is a phonological string that can include spaces (multi-word line)
    star is True (default) or False; if True, illegal syllables are preceded
        by an asterisk -- easy to detect but causing mismatches when join()'ed
    debug is True or False (default); when True, cases extensive information
        about the syllables to be returned (onsets, codas, misses etc.)
    the result is a list of phonological string fragments corresponding
        to the syllables of line
    star and debug are keyword arguments
    """
    with open("clusters.txt", encoding="utf-8", mode="r") as clusterFile:
        clustlist = [c.strip() for c in clusterFile.readlines()]

    syllables=[]
    if star:
        stst=u'*'
    else:
        stst=u''
    while (len(line)>0):
        m= re.search("\s*[έάίύόeaiuo\s]\s*", line)
        if (m!=None):
            vowelpos=m.start()
            nextpos=m.end()
            cons=line[:vowelpos].strip()
            vowel=line[vowelpos:nextpos].strip()
            if (vowelpos>0):
                if (len(vowel)<1 and len(cons)>0): # white space, consonant coda
                    try: 
                        syllables.append(syllables.pop()+cons)
                    except IndexError: # pop failure
                        syllables.append(stst+cons)                      
                elif (len(cons)>1): # cluster
                    if (cons in clustlist): # legal onset
                        syllables.append(cons+vowel)
                    elif (len(cons)>2): # 3+ consonants
                        if (cons[1:] in clustlist): # singleton coda
                            try:
                                syllables.append(syllables.pop()+cons[0])
                                syllables.append(cons[1:]+vowel)
                            except IndexError: # pop failure
                                syllables.append(stst+cons+vowel)
                        elif ((len(cons)==3) or (cons[2:] in clustlist)): # two-consonant cluster coda
                            try:
                                newsyl=syllables.pop()+cons[:2]
                                syllables.append(stst+newsyl)
                                syllables.append(cons[2:]+vowel)
                            except IndexError: # pop failure
                                syllables.append(stst+cons+vowel)
                        else:
                            syllables.append(stst+cons+vowel)
                    else: # two consonants, illegal onset
                        try:
                            syllables.append(syllables.pop()+cons[0])
                            syllables.append(cons[1]+vowel)
                        except IndexError: # pop failure
                            syllables.append(stst+cons+vowel)
                elif (len(cons+vowel)>0): # single consonant onset
                    syllables.append(cons+vowel)
            elif (len(vowel)>0): # vowel at 0
                syllables.append(vowel)
            line=line[nextpos:]
        else: # no vowel or whitespace found
            if (len(line)==1): # single-consonant leftovers!
                try:
                    syllables.append(syllables.pop()+line)
                except IndexError:
                    syllables.append(stst+line)
            else: # more leftovers...
                try:
                    finalsyl=stst+syllables.pop()+line
                    syllables.append(finalsyl)
                except IndexError:
                    syllables.append(stst+line)
            line=u""
    return (syllables)

rules = readPhonRules("./phonRules.txt")
df = get_info("./speakerInfo2.csv")

with open("output_final.csv", 'w', encoding="UTF-8") as fout:
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
                    if "Past" in wordData:
                        syllables = syllabify(phon)
                        if len(syllables) == 3:
                            if syllables[0][0] not in "iaeou":
                                fout.write(str(id) + "," + str(initial) + "," + str(orthography) + "," + str(gloss) + "," + str(df.loc[df['Informant_ID'] == id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Origin'].item()).replace(", ", "/") + "\n")
                        if len(syllables) >= 4:
                            # print(word)
                            if syllables[0][0] not in "iaeou":
                                fout.write(str(id) + "," + str(initial) + "," + str(orthography) + "," + str(gloss) + "," + str(df.loc[df['Informant_ID'] == id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Origin'].item()).replace(", ", "/") + "\n")
                            elif syllables[0][0] == "e":
                                fout.write(str(id) + "," + str(initial) + "," + str(orthography) + "," + str(gloss) + "," + str(df.loc[df['Informant_ID'] == id, 'Gender'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Dialect_Area'].item()) + "," + str(df.loc[df['Informant_ID'] == id, 'Origin'].item()).replace(", ", "/") + "\n")