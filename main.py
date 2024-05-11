import os
import random



def createHugeFiles(totalSize, chunkSize):
    file1 = "hugefile1.txt"
    file2 = "hugefile2.txt"

    if not os.path.isfile(file1):
        with open(file1, "w") as file:
            for i in range(totalSize // chunkSize):
                chunk = [str(random.randint(0, 32767)) for j in range (chunkSize)]
                file.write("\n".join(chunk) + "\n")

    if not os.path.isfile(file2):
        with open(file2, "w") as file:
            for i in range(totalSize // chunkSize):
                chunk = [str(random.randint(0, 32767)) for j in range (chunkSize)]
                file.write("\n".join(chunk) + "\n")

createHugeFiles(1000000,100000)



