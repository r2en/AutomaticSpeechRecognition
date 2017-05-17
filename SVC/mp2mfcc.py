#coding:utf-8
import os
import sys

def mp3ToRaw(mp3File, rawFile):
    os.system("lame --resample 16 -b 32 -a '%s' temp.mp3" % mp3File)
    os.system("lame --decode temp.mp3 temp.wav")
    os.system("sox temp.wav %s" % rawFile)
    os.remove("temp.mp3")
    os.remove("temp.wav")

def calcNumSample(rawFile):
    filesize = os.path.getsize("temp.raw")
    numsample = filesize / 2
    return numsample

def extractCenter(inFile, outFile, period):
    numsample = calcNumSample(inFile)
    fs = 16000
    center = numsample / 2
    start = center - fs * period
    end = center + fs * period
    if start < 0: start = 0
    if end > numsample - 1: end = numsample - 1
    os.system("bcut +s -s %d -e %d < '%s' > '%s'" \
              % (start, end, "temp.raw", rawFile))


def calcMFCC(rawFile, mfccFile):
    os.system("x2x +sf < '%s' | frame -l 400 -p 160 | mfcc -l 400 -f 16 -n 40 -m 19 -E > '%s'"
              % (rawFile, mfccFile))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: python mp2mfcc.py [mp3dir] [mfccdir] [rawdir]"
        sys.exit()

    mp3Dir = sys.argv[1]
    mfccDir = sys.argv[2]
    rawDir = sys.argv[3]

    if not os.path.exists(mfccDir):
        os.mkdir(mfccDir)
    if not os.path.exists(rawDir):
        os.mkdir(rawDir)

    for file in os.listdir(mp3Dir):
        if not file.endswith(".mp3"): continue
        mp3File = os.path.join(mp3Dir, file)
        mfccFile = os.path.join(mfccDir, file.replace(".mp3", ".mfc"))
        rawFile = os.path.join(rawDir, file.replace(".mp3", ".raw"))

        try:
            mp3ToRaw(mp3File, "temp.raw")
            extractCenter("temp.raw", rawFile, 15)
            calcMFCC(rawFile, mfccFile)
            print "%s => %s" % (mp3File, mfccFile)
            os.remove("temp.raw")
        except:
            continue