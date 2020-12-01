#!/usr/bin/env python
import gen
import os


def addSimor():
    name = ["Jpsi", "NewJpsi", "Psi2S", "4180", "705Jpsi", "Diy4180", "DIY705Jpsi"]
    simff = [
        "template/simJpsi.txt", "template/simNewJpsi.txt",
        "template/simPsi2S.txt", "template/sim4180.txt",
        "template/sim705Jpsi.txt", "template/simDiy4180.txt",
        "template/simDIY705Jpsi.txt"
    ]
    recff = [
        "template/recJpsi.txt", "template/recNewJpsi.txt",
        "template/recPsi2S.txt", "template/rec4180.txt",
        "template/rec705Jpsi.txt", "template/recDiy4180.txt",
        "template/recDIY705Jpsi.txt"
    ]

    for n, s, r in zip(name, simff, recff):
        g = gen.process(n, s, r)
        g.Make()


if __name__ == "__main__":
    if os.path.exists('.addDone'):
        exit(0)
    else:
        addSimor()
        os.system('touch .addDone')
