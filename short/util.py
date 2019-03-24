import os
import commands
import sys
import re
#-----find only file in current dir:p
def findfile(p):
    File = []
    # if p is a file
    if os.path.isfile(p):
        File.append(os.path.abspath(p))
        File.sort()
        return File
    # p is a director
    if os.path.isdir(p):
        for i in os.listdir(p):
            if os.path.isfile(i):
                File.append(os.path.join(os.path.abspath(p), i))
        File.sort()
        return File
    # p is a string, such as *.cxx
    s = p.replace("*", "[a-zA-Z0-9]*")
    pattern = re.compile(s)
    for i in os.listdir("."):
        if pattern.match(i):
            File += findfile(i)
        File.sort()
        return File
    return File


def findtype(files, type = '.txt'):
    # the function to select the files whose type is txt
    txt = []
    for i in files:
        tp=os.path.splitext(i)[1]
        if(tp==type):
            txt.append(i)
    return txt
#-----find .c .cxx in files list
#--------end of function-------------------------------#
mypath=os.getcwd()
path=os.listdir('.')
#-----find all file in path 'p'
def findfiler(p):
    file=[]
    if os.path.isfile(p):
        file.append(os.path.abspath(p))
    else:
        path=[]
        for i in os.listdir(p):
            path.append(p+'/'+i)
        for i in path:
            file.extend(findfiler(i))
        file.sort()
    return file
#-----end-------#
#-------end-----------#

class heprm:
    def __init__(self):
        self._opt=[]
        self._arv=[]
        self._stat=''
        self._ids=[]
        self._keyword='XXXX'
    def _getopt(self):
        for i in range(1, len(sys.argv)):
            if '-' in sys.argv[i]:
                self._opt.append(sys.argv[i])
            else:
                self._arv.append(sys.argv[i])
    def _getkey(self):
        self._getopt()
        if len(self._arv)>0:
            self._keyword=self._arv[0]
    def _qstat(self):
        self._getkey()
        self._stat = commands.getoutput('hep_q -u ')
    def _getids(self):
        self._qstat()
        lines = self._stat.splitlines()
        key = self._keyword.replace("*", "[a-zA-Z0-9]*")
        pattern = re.compile(key)
        for i in lines:
            if pattern.findall(i) and not "JOBID" in i:
                ID = float(i.split()[0])
                # print ID
                self._ids.append(int(ID)) 
    def run(self):
        self._getids()
        for i in self._ids:
            os.system('hep_rm '+str(i))

def shrun(files):
    """ 
    Running all bash and cpp files 
    """
    mypath=os.getcwd()
    f=open('runSH.sh','w')
    f.write('#!/bin/bash\n')
    for i in files:
        path=os.path.split(i)[0]
        file=os.path.split(i)[1]
        name=os.path.splitext(i)[0]
        f.write('cd '+path+'\n')
        f.write("sh "+file+'\n')
    f.write('rm -f runSH.sh\n')
    f.close()
    os.chdir(mypath)
    print( mypath)
    os.system("chmod +x runSH.sh")
    os.system('source '+mypath+'/'+'runSH.sh')


def rootrun(files):
    """
    ls all cpp file recursively, and process one by one with "root -l -b -q"
    """
    mypath=os.getcwd()
    f=open('rootrun.sh', 'w')
    f.write('#!/bin/bash\n')
    for i in files:
        path=os.path.split(i)[0]
        file=os.path.split(i)[1]
        name=os.path.splitext(i)[0]
        f.write('cd '+path+'\n')
        f.write("root -l -b -q "+file+'\n')
    f.write('rm -f rootrun.sh\n')
    f.close()
    os.system("chmod +x rootrun.sh")
    os.system('source '+mypath+'/'+'rootrun.sh')
    os.system('rm -f rootrun.sh')

