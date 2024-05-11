import os
import random
import shutil
import threading
import time
from filesplit.split import Split


def createHugeFiles(file1, file2, totalSize, chunkSize):
    start = time.time()
    if not os.path.isfile(file1):
        with open(file1, "w") as file:
            for i in range(int(totalSize / chunkSize)):
                chunk = [str(random.randint(0, 32767)) for j in range(chunkSize)]
                file.write("\n".join(chunk) + "\n")
                print(f"Huge1 {i / (totalSize / chunkSize)}")

    if not os.path.isfile(file2):
        with open(file2, "w") as file:
            for i in range(int(totalSize / chunkSize)):
                chunk = [str(random.randint(0, 32767)) for j in range(chunkSize)]
                file.write("\n".join(chunk) + "\n")
                print(f"Huge2 {i / (totalSize / chunkSize)}")

    end = time.time()
    total = end - start
    if total > 0.0001:
        print(f"{total:.4f} seconds: Time to create {totalSize} rand, in chunks of {chunkSize}")
    else:
        print("Huge Files Existed")


def emptyDirectory(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Failed to delete {path}. Reason: {e}")


def adder(inFile1, inFile2, outFile):
    file1 = open(inFile1, "r")
    file2 = open(inFile2, "r")
    file3 = open(outFile, "w")

    array1 = file1.readlines()
    array2 = file2.readlines()

    for i in range(len(array1)):
        file3.write(str(int(array1[i]) + int(array2[i])) + "\n")

    file1.close()
    file2.close()
    file3.close()


def runThreaded(directory, file1, file2, outFile):
    os.chdir(directory)
    t1 = threading.Thread(target=adder, args=(file1, file2, outFile))
    t1.start()
    t1.join()


def addFilesThreaded(inFile1, inFile2, outName, size):
    writeDir = os.getcwd()
    workingDir = writeDir + "\\temp"
    emptyDirectory(workingDir)
    threads = 10

    start = time.time()
    file1 = open(inFile1, "r")
    Split(inFile1, workingDir).bylinecount(size / threads)
    file1.close()
    file2 = open(inFile2, "r")
    Split(inFile2, workingDir).bylinecount(size / threads)
    file2.close()

    numFiles = int((len(next(os.walk(workingDir))[2]) - 1) / 2)

    for i in range(1, numFiles + 1):
        runThreaded(workingDir, f"hugefile1_{str(i)}.txt", f"hugefile1_{str(i)}.txt", f"newFile{i}.txt")

    with open(outName, "w") as output:
        for filename in os.scandir(workingDir):
            if "newFile" in filename.name:
                with open(filename, "r") as temp:
                    array = temp.readlines()
                    for j in range(len(array)):
                        output.write(str(array[j]))

    os.replace(workingDir + f"\\{outName}", writeDir + f"\\{outName}")
    emptyDirectory(workingDir)
    end = time.time()
    total = end - start
    print(f"{total:.4f} seconds: Time to create and run {threads} threads")


def main():
    numRandom = 1000000000
    chunks = int(numRandom / 1000)
    hugefile1 = "hugefile1.txt"
    hugefile2 = "hugefile2.txt"
    outfile = "totalfile.txt"

    createHugeFiles(hugefile1, hugefile2, numRandom, chunks)
    addFilesThreaded(hugefile1, hugefile2, outfile, numRandom)


main()
