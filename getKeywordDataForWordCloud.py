read_file = open("dataResults/keyWordsResult.txt", "r")

write_file = open("dataResults/keyWordsCloud.txt", "w")

a = False
for line in read_file.readlines():
    word_and_amount = line.split(" : ")
    print(word_and_amount)
    if a:
        print((word_and_amount[0].replace(" ", "~")+" ") *
              int(word_and_amount[1]), file=write_file)
    else:
        a = True
read_file.close()
write_file.close()
