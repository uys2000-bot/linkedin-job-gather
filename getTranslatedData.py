import psycopg2


db = psycopg2.connect(user = "emleuqybvzquao",
                      password = "f78c61f960a8be501257d6274abf0ff0392430724de5a7c8bf44424e3d401cdf",
                      host = "ec2-3-216-167-65.compute-1.amazonaws.com",
                      port = "5432",
                      database = "d7391nts0md52f")
c = db.cursor()
c.execute("SELECT * FROM jobs;")

liste = c.fetchall()
f = open("data/dataTranslated.txt", "w")
for i in liste:
    print(i,file=f)
f.close()
db.commit()

