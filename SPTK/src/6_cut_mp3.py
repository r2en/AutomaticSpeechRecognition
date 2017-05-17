#coding: utf-8
import os
import sys

targetDir = u""
outputDir = u"./data"

if __name__ == "__main__":
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    for file in os.listdir(targetDir):
        if not file.endswith(".mp3"): continue
        mp3file = os.path.join(targetDir,file)
        rawfile = os.path.join(outputDir,file.replace(".mp3",".raw"))
        print mp3file, "=>", rawfile

        os.system("lame --respamle 16 -b 32 -a '%s' temp.mp3" % mp3file)
        os.system("lame --decode tmp.mp3 temp.wav")
        os.system("sox temp.wav temp.raw")

        size = os.path.getsize("temp.raw")

        numsample = size / 2

        fs = 16000
        period = 15
        center = numsample / 2
        start = center -fs * period
        end = center + fs * period

        if start < 0: start = 0
        if end > numsample - 1: end = numsample - 1
        os.system("bcut +s -s %d -e %d < '%s' > '%s'" % (start,end,"temp.raw",rawfile))

        os.remove("temp.mp3")
        os.remove("temp.wav")
        os.remove("temp.raw")
        