#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Bes import myfunction as m
from Bes.commands import getoutput as do
from Bes import hepsub
import os
from Bes.commands import getoutput
import logging
logger = logging.getLogger(__name__)
from multiprocessing.pool import ThreadPool
# from SubJob import hep
import glob
import time
class SubWithProcId(hepsub.hepsub):
    """
    path: hepsub.getPath()
       sub all jobs_%{ProcId}.txt in the fildor
    """
    def __init__(self):
        super(SubWithProcId, self).__init__()
    def getSubJobDir(self):
        dirList = os.listdir(self.getPath())
        logging.debug(dirList)
        logging.debug("self.getPath() = {}".format(
            self.getPath()))
        for  i in range(len(dirList)):
            dirList[i] = os.path.join(self.getPath().strip(), dirList[i])
        logging.debug(dirList)
        return dirList
    def _subJobInOneDir(self, aDir):
        logging.debug("cd {dir} ; boss.condor -n {Njobs} {JOB}".format(
            dir=aDir, Njobs=len(glob.glob(aDir+"/jobs_*.txt")), 
            JOB=r"jobs_%{ProcId}.txt"
            ))
        out = getoutput("cd {dir} ; boss.condor -n {Njobs} {JOB}".format(
            dir=aDir, Njobs=len(glob.glob(aDir+"/jobs_*.txt")), 
            JOB=r"jobs_%{ProcId}.txt"
            ))
        num = out.split()[-1]
        logging.debug(out)
        logger.debug("num = {}".format(num))
        return num
    def subAllJobs(self, jobsList):
        if not jobsList:
            logger.warning("no jobs")
            return 
        logger.debug("Please wait for some seconds!")
        t0 = time.time() 
        if len(jobsList) == 1:
            logger.info("Sub all Jobs in {}".format(jobsList[0]))
            self._subJobInOneDir(jobsList[0])
            return 
        t = ThreadPool(processes=20)
        numList = t.map(self._subJobInOneDir, jobsList)
        t.close()
        t1 = time.time() 
        logger.info("sub all jobs successful!")
        logger.info("Sub jobs consumes {0:.3f} s".format(t1 - t0))
        with open(self.getLog()+"/.id", 'w') as f:
            for i in numList:
                try:
                    float(i)
                    logger.info("job ID: {}".format(i))
                    f.write("{}\n".format(i))
                except Expection as e:
                    pass

    def sub(self):
        """
        overload the base function `sub`
        """
        self.subAllJobs(self.getSubJobDir())

    
if __name__ == "__main__":
    logger.debug("test the command")
    command = "cd {dir} ; boss.condor -n {Njobs} {JOB}".format(
            dir="~", 
            Njobs=len(os.listdir('.')), 
            JOB=r"jobs_%{ProcId}.txt"
            )
    logger.debug("the command is {}".format(command))


