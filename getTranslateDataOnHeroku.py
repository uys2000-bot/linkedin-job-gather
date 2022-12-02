from googletrans import Translator
from time  import  sleep
import psycopg2


db = psycopg2.connect(user = "emleuqybvzquao",
                      password = "f78c61f960a8be501257d6274abf0ff0392430724de5a7c8bf44424e3d401cdf",
                      host = "ec2-3-216-167-65.compute-1.amazonaws.com",
                      port = "5432",
                      database = "d7391nts0md52f")
c = db.cursor()
c.execute("DROP TABLE IF EXISTS jobs")
c.execute("CREATE TABLE jobs(id SERIAL PRIMARY KEY, text TEXT NOT NULL);")
db.commit()
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
    jobText = ""
    w = 0
    for line in job.split("\n"):
        w = w+1
        wordTranslated = translator.translate(line, dest='en').text
        jobText = jobText + " " + wordTranslated

    print(str(l))
    jobText = jobText.replace("'","")
    c.execute(f"INSERT INTO jobs(text) VALUES('{jobText}');")
    db.commit()

while True:
    sleep(1000)