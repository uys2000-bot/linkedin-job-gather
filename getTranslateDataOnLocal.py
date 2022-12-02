from langdetect import detect
from googletrans import Translator

open("./data/dataTranslated.txt", "w").close()
rawFile = open("./data/jobs", "r")
rawFile.read()
i = rawFile.tell()
rawFile.seek(0)

rawFile.readline()  # date

jobs = []
jobTexts = []
l = 0
while i > rawFile.tell():
    lang = "noLang"
    l2 = rawFile.readline()
    if l2 == "\n":
        continue
    if l2 == "--------------------------------------\n":
        jobs.append("".join(jobTexts))
        jobTexts = []
    else:
        jobTexts.append(l2)

translator = Translator()
for job in jobs:
    l = l+1
    file = open("./data/dataTranslated.txt", "a")
    jobText = ""
    w = 0
    for line in job.split("\n"):
        w = w+1
        wordTranslated = translator.translate(line, dest='en').text
        jobText = jobText + " " + wordTranslated

    print(str(l))
    print(jobText, file=file)
    file.close()
