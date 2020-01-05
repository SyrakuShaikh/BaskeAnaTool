#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from multiprocessing.pool import ThreadPool
import time
import logging
logger = logging.getLogger(__name__)

# from Bes.commands import getoutput as do
#-----small functions-----
def mkdir(s):
    if (not os.path.isdir(s)):
        os.makedirs(s)


#-----sub jobs with a given abs path
def hepsub(files):
    if len(files) > 0:
        mypath = os.getcwd()
        for i in files:
            path = os.path.split(i)[0]
            file = os.path.split(i)[1]
            name = os.path.splitext(i)[0]
            os.chdir(path)
            #f=open(name+'.sh','w')
            #f.write('#!/bin/bash\n')
            #f.write('cd '+ path+'\n')
            #f.write("source /afs/ihep.ac.cn/users/m/maxx/head/.b702p1\n")
            #f.write('boss.exe  '+file+'\n')
            #f.close()
            #os.system('chmod +x '+name+'.sh')
            #if '.sh' in file:
            #   os.system('chmod +x '+file)
            os.system('boss.condor   ' + file)
            #os.system('hep_sub  -g  physics '+name+'.sh')
        os.chdir(mypath)  #return to my work path


def shsub(files):
    if len(files) > 0:
        mypath = os.getcwd()
        for i in files:
            path = os.path.split(i)[0]
            file = os.path.split(i)[1]
            name = os.path.splitext(i)[0]
            os.chdir(path)
            os.system('chmod +x ' + file)
            os.system('hep_sub -g physics   ' + file)
        os.chdir(mypath)  #return to my work path


#---sub .C ---first mkdir a .sh
def csub(files):
    mypath = os.getcwd()
    for i in files:
        path = os.path.split(i)[0]
        file = os.path.split(i)[1]
        name = os.path.splitext(i)[0]
        os.chdir(path)
        f = open(name + '.sh', 'w')
        f.write('#!/bin/bash\n')
        f.write('cd ' + path + '\n')
        f.write('root -l -b -q ' + file + '\n')
        f.write('rm -f  ' + name + '.sh\n')
        f.close()
        os.system('chmod +x ' + name + '.sh')
        os.system('hep_sub -g physics ' + name + '.sh')
    os.chdir(mypath)


def shortsub(files):
    mypath = os.getcwd()
    for i in files:
        path = os.path.split(i)[0]
        file = os.path.split(i)[1]
        name = os.path.splitext(i)[0]
        os.chdir(path)
        f = open(name + '.sh', 'w')
        f.write('#!/bin/bash\n')
        f.write('cd ' + path + '\n')
        f.write('root -l -b -q ' + file + '\n')
        f.write('rm -f  ' + name + '.sh\n')
        f.close()
        os.system('chmod +x ' + name + '.sh')
        os.system('qsub -q shortq ' + name + '.sh')
    os.chdir(mypath)


def rootrun(files):
    mypath = os.getcwd()
    f = open('rootrun.sh', 'w')
    f.write('#!/bin/bash\n')
    for i in files:
        path = os.path.split(i)[0]
        file = os.path.split(i)[1]
        name = os.path.splitext(i)[0]
        f.write('cd ' + path + '\n')
        f.write("root -l -b -q " + file + '\n')
    f.write('rm -f rootrun.sh\n')
    f.close()
    os.chdir(mypath)
    print(mypath)
    os.system("chmod +x rootrun.sh")
    os.system('source ' + mypath + '/' + 'rootrun.sh')
    os.system('rm -f rootrun.sh')


def shrun(files):
    mypath = os.getcwd()
    f = open('runSH.sh', 'w')
    f.write('#!/bin/bash\n')
    for i in files:
        path = os.path.split(i)[0]
        file = os.path.split(i)[1]
        name = os.path.splitext(i)[0]
        f.write('cd ' + path + '\n')
        f.write("sh " + file + '\n')
    f.write('rm -f runSH.sh\n')
    f.close()
    os.chdir(mypath)
    print(mypath)
    os.system("chmod +x runSH.sh")
    os.system('source ' + mypath + '/' + 'runSH.sh')


# -----hep sub--
# ##################the class to make jobs
class subjobs(object):
    def setdstpath(self, dst, key=''):
        self._dst = dst
        files = os.listdir(self._dst)
        list.sort(files)
        self._s = []
        for i in files:
            if (('dst' in i) and (key in i)):
                self._s.append(i)

    def drop(self, dsts):
        self._bad = dsts

    def _drop(self):
        for i in self._bad:
            self._rm(i)

    def _rm(self, badst):
        for i in self._s:
            if badst in i:
                self._s.remove(i)

    def setjobpath(self, job):
        self._job = job
        if (not os.path.isdir(self._job)):
            os.makedirs(self._job)

    def setrootname(self, name):
        self.root = name

    def setrootpath(self, root):
        self._root = root
        if (not os.path.isdir(self._root)):
            os.makedirs(self._root)

    def setjobnum(self, n):
        self._n = n

    def __init__(self):
        self._dst = os.getcwd()
        self._job = os.getcwd()
        self._n = 1
        self._name = 'default'
        self.root = 'root'
        self._bad = []
        self._jobname = 'job'

    def _process(self, i, j):
        list.sort(self._s)
        dst = ''
        for k in range(i, j):
            dst += '\t"' + self._dst + '/' + self._s[k - 1] + '",\n'
        dst += '\t"' + self._dst + '/' + self._s[j - 1] + '"' + '\n'
        return dst

    def setbody(self, s):
        self._body = s

    def setname(self, name):
        self._name = name

    def setjobname(self, name):
        self._jobname = name

    def _creatjob(self, i, j, k):
        self._drop()
        _num = '%d' % k
        name = self._job + '/' + self._jobname + _num + '.txt'
        f = open(name, 'w')
        f.write(self._body)
        f.write(self._process(i, j))
        f.write('};\n')
        root = 'NTupleSvc.output={\n'
        root += '\t"' + self._name
        root += " DATAFILE = '" + self._root + '/' + self.root + _num + ".root'"
        root += " OPT = 'new'"
        root += " TYP = 'ROOT'\"\n"
        root += "};\n"
        f.write(root)
        f.close()
    def _MakeOneJob(self, args):
        self._creatjob(*args)

    def jobs(self):
        n = self._n
        self._tot = len(self._s)
        each = int(self._tot / n)
        logger.info("Total `.dst` files is {}".format(self._tot))
        logger.info("Each job contains {} `.dst` file \n".format(each))
        over = self._tot - each * n
        argsList = []
        t0 = time.time()
        for i in range(0, over):
            m = each + 1
            # self._creatjob(i * m + 1, (i + 1) * m, i)
            argsList.append((i * m + 1, (i + 1) * m, i))
        for i in range(over, n):
            m = each
            # self._creatjob(i * m + 1 + over, (i + 1) * m + over, i)
            argsList.append((i * m + 1 + over, (i + 1) * m + over, i))
        pool = ThreadPool(processes=10)
        pool.map(self._MakeOneJob, argsList)
        pool.close()
        t1 = time.time()
        logger.debug("Time: {0:.03f}".format(t1-t0))

