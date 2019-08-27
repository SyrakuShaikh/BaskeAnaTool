import util
from util import jobCandidates
from SubJob import hep
_USAGE = '''
Usage:  [option] [files or directory]
Option: 
    -help get help
    -c type="c, C, cpp, cc"
        1) make bash job,  into which the follow command will be wrote, 
             `root -l -b -q [the file]`
        2) change the authority: `chmod +x [the file].sh`
        3) submit: `hep_sub -g physics [the file].sh`

    -sh change the authority of those files, then submit all of them to the
        server.

    -txt submit all BOSS job files which end with `.txt`, to the server.
       the submit command is `boss.condor`

    -py type="py" 
        1) make bash job,  into which the follow command will be wrote, 
             `python [the file]`
        2) same as -c mode
    -r recursively

Assign special submit and execute commands or special file type
    ie. sub="hep_sub"
        require all jobs must be submitted by such way
    
    ie. exe="latex"
        make bash file, and write the execute command into the bash file

    ie. type="tex,h"
        separate by ','

    warn: no blank space at both sides of '='

Files or Directory
    1) regular expression:
       "a*txt", "a?", "a."
    2) a file
    3) a directory
    4) the default: current directory "."
'''
class hepsub(jobCandidates):
    def __init__(self):
        jobCandidates.__init__(self)
        self._Uasge = _USAGE
    def run(self):
        self._prepare()
        #print self._jobList
        #sub="...", define the sub commands
        # exe="...", define the way to execute the file
        # if exe in the diy, then the bash file will be made
        if 'exe' in self._diy.keys():
            #the sub is not set, we set the subway is 'hep_sub -g physics'
            if not 'sub' in self._diy.keys():
                self._diy['sub'] = 'hep_sub -g physics '
            hep.SubDIY(self._jobList, self._diy['exe'], self._diy['sub'])
            return
        # if the subway is specially setted, but the exe way maybe not setted
        # we will sub the jobs direclly once exe not setted
        if 'sub' in self._diy.keys():
            if not 'exe' in self._diy.keys():
                hep.Sub(self._jobList, self._diy['sub'])
            else:
                hep.SubDIY(self._jobList, self._diy['exe'], self._diy['sub'])
            return
        if 'type' in self._diy.keys():
            # the exe way is usually setted, if not set is as 'root -l -b -q'
            # if the sub way is boss.condor, sub it directly
            if not 'sub' in self._diy.keys():
                self._diy['sub'] = "hep_sub -g physics"
            if not 'exe' in self._diy.keys():
                self._diy['exe'] = 'root -l -b -q'
            hep.SubDIY(self._jobList, self._diy['exe'], self._diy['sub'])
            return
        hep.smartSub(self._jobList)

test = hepsub()
test.run()
