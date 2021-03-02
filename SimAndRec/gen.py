import SimAndRec
import os


class process:
    def __init__(self, name, simff, recff):
        self._name = name
        self._simff = simff
        self._recff = recff

    def AnA(self):
        ffName = "ana%s.py" % (self._name)
        pth = os.getcwd()
        self._simff = os.path.join(pth, self._simff)
        self._recff = os.path.join(pth, self._recff)
        f = open(ffName, 'w')
        ss = 'from SimAndRec import SimRecAna\n'
        ss += 'from SimAndRec import util\n'
        ss += "opt='''//test'''\n"
        ss += 'svc = SimRecAna.process("%s", "%s")\n'\
            % (self._simff, self._recff)
        ss += 'svc.SetOpt(opt)\n'
        ss += '''if len(util.getArv()) ==0:
    svc.Make()
    svc.Sub()
    exit(0)
elif '-make' in util.getArv() :
    svc.Make()
    exit(0)
        '''
        f.write(ss)
        f.close()

    def Make(self):
        self.AnA()
        ffName = "init%s.py" % (self._name)
        pth = os.getcwd()
        self._simff = os.path.join(pth, self._simff)
        self._recff = os.path.join(pth, self._recff)
        f = open(ffName, 'w')
        ss = 'import SimAndRec\n'
        ss += 'import util\n'
        ss += 'svc = SimAndRec.process("%s", "%s")\n' % (self._simff,
                                                         self._recff)
        if "705Jpsi" in self._simff:
            ss += '## 2009 round02 {-9947, 0, -10878} 224.04+-1.26M\n'
            ss += 'opt02 = ("RealizationSvc", "RunIdList", "{-9947, 0, -10878}", "=")\n'
            ss += '## 2012 round05 {-27255, 0, -28236} 1088.50+-4.23M\n'
            ss += 'opt05 = ("RealizationSvc", "RunIdList", "{-27255, 0, -28236}", "=")\n'
            ss += '## 2017-18 round11 {-52940, 0, -54976, -55861, 0, -56546}\n'
            ss += 'opt11 = ("RealizationSvc", "RunIdList", "{-52940, 0, -54976, -55861, 0, -56546}", "=")\n'
            ss += '## 2018-19 round12 {-56788, 0, -59015}  2017-19 8774.01+-39.33M\n'
            ss += 'opt12 = ("RealizationSvc", "RunIdList", "{-56788, 0, -59015}", "=")\n'
            ss += 'svc.SetOpt(*opt02)\n'
        elif "Diy4180" in self._simff:
            ss += 'opt = ("KKMC", "ThresholdCut", "3.625", "=")\n'
            ss += 'svc.SetOpt(*opt)\n'

        ss += '''if len(util.getArv()) == 0:
    svc.Make()
    svc.Sub()
    exit(0)
elif '-make' in util.getArv():
    svc.Make()
    exit(0)
        '''
        f.write(ss)
        f.close()
        setup_bash = ''
        for line in open("setup.sh").readlines():
            if "Sim%s" % (self._name) in line:
                continue
            setup_bash += line
        setup_bash += 'alias Sim%s="python ${SIMANDRECDIR}/init%s.py"' % (
            self._name, self._name)
        # print (setup_bash)
        f = open("setup.sh", 'w')
        f.write(setup_bash + '\n')
        f.close()

        setup_tcsh = ''
        for line in open("setup.csh").readlines():
            if "Sim%s" % (self._name) in line:
                continue
            setup_tcsh += line
        setup_tcsh += 'alias Sim%s "python ${SIMANDRECDIR}/init%s.py"' % (
            self._name, self._name)
        f = open("setup.csh", 'w')
        f.write(setup_tcsh + '\n')
        f.close()
        setup_zsh = ''
        for line in open("setup.zsh").readlines():
            if "Sim%s" % (self._name) in line:
                continue
            setup_zsh += line
        setup_zsh += 'alias Sim%s="python ${SIMANDRECDIR}/init%s.py"' % (
            self._name, self._name)
        # print (setup_bash)
        f = open("setup.zsh", 'w')
        f.write(setup_zsh + '\n')
        f.close()
