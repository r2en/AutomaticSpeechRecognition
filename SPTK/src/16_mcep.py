#coding:utf-8
import os
import sys
import subprocess
import pylab

def execute(cmd):
    subprocess.call(cmd,shell=True)
    print cmd

def draw_figure(dat_file, xlabel="", ylabel="", style="b-", lw=1):
    fp = open(dat_file, "r")
    x = []
    y = []
    for line in fp:
        line = line.rstrip()
        dat = line.split()
        x.append(float(dat[0]))
        y.append(float(dat[1]))
    pylab.plot(x, y, style, linewidth=lw)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.xlim(min(x), max(x))
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python 16_mcep.py [order of mel cepstrum]"
        exit()
    
    raw_file = sys.argv[1]
    order = int(sys.argv[2])

    alpha = 0.42

    prefix = raw_file.replace(".raw","")

    # Raw -> wav
    cmd = "sox -e signed-integer -c 1 -b 16 -r 16000 %s.raw %s.wav" % (prefix,prefix)
    execute(cmd)

    # pitch
    cmd = "x2x +sf %s.raw | pitch -a 1 > %s.pitch" % (prefix,prefix)
    execute(cmd)

    # draw figure
    cmd = "dmp +f %s.pitch > pitch.txt" % prefix
    execute(cmd)
    draw_figure("pitch.txt","frame","pitch")
    pylab.savefig("pitch.png")
    pylab.clf()
    os.remove("pitch.txt")

    # generate sound
    cmd = "excite -p 80 data.pitch | sopr -m 1000 | x2x +fs > source.raw"
    execute(cmd)
    cmd = "sox -e signed-integer -c 1 -b 16 -r 16000 source.raw source.wav"
    execute(cmd)
    cmd = "dmp +s source.raw > source.txt"
    execute(cmd)

    # draw sound
    draw_figure("source.txt","sample","amplitude")
    pylab.savefig("source.png")
    pylab.clf()
    os.remove("source.txt")

    # analyze cepstrum
    cmd = "x2x +sf < %s.raw | frame -l 400 -p 80 | window -l 400 -L 512 | mcep -l 512 -m %d -a %f > %s.mcep" % (prefix, order, alpha, prefix)
    execute(cmd)

    # draw log spectrum
    cmd = "x2x +sf < %s.raw | frame -l 400 -p 80 | bcut +f -l 400 -s 65 -e 65 | window -l 400 -L 512 | spec -l 512 | dmp +f > spec.txt" % prefix
    execute(cmd)
    draw_figure("spec.txt", style="b-")

    # convert from cepstrum to spectrum
    cmd = "bcut +f -n %d -s 65 -e 65 < %s.mcep | mgc2sp -m %d -a %f -g 0 -l 512 | dmp +f > mcep.txt" % (order, prefix, order, alpha)
    execute(cmd)
    draw_figure("mcep.txt","frequency bin", "log magnitude [db]",style="r-",lw=2)
    pylab.savefig("mcep.png")

    os.remove("spec.txt")
    os.remove("mcep.txt")

    # generate analistic compicated sound
    cmd = "excite -p 80 %s.pitch | mlsadf -m %d -a %f -p 80 %s.mcep | x2x +fs > %s.mcep.raw" % (prefix, order, alpha, prefix, prefix)
    execute(cmd)

    # convert wav file
    cmd = "sox -e signed-integer -c 1 -b 16 -r 16000 %s.mcep.raw %s.mcep.wav" % (prefix, prefix)
    execute(cmd)


