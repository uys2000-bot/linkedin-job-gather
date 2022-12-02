import re

##read Jobs
jobsFile = open("./data/dataTranslated.txt", "r")
jobsFile.read()
i = jobsFile.tell()
jobsFile.seek(0)

#read Keywords
myKeywordsFile = open("./data/keyWords.txt", "r")
myKeywords = [x.lower().replace("\n","") for x in myKeywordsFile.readlines()]
myKeywordsFile.close()
myKeywordDict = {}


#calculate keyword countswith lowering text and keywords
jobText = jobsFile.read().lower()
for keyWord in myKeywords:
    c = len(re.findall(r"\b("+re.escape(keyWord)+ r")\b", jobText))
    if c!=0: myKeywordDict[keyWord] = c
    

# sort keyword counts
sorted_values = sorted(myKeywordDict.values(), reverse=True) # Sort the values
sorted_dict = {}

for i in sorted_values:
    for k in myKeywordDict.keys():
        if myKeywordDict[k] == i:
            sorted_dict[k] = myKeywordDict[k]

f = open("dataResults/keyWordsResult.txt","w")
for key, value in sorted_dict.items():
    print(key, ":", value, file=f)
f.close()