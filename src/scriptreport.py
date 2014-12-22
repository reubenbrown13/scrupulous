import characterreport
import config
import pdf
import pml
import scenereport
import screenplay
import util

class ScriptReport:
    def __init__(self, sp):
        self.sp = sp
        self.sr = scenereport.SceneReport(sp)
        self.cr = characterreport.CharacterReport(sp)

    def generate(self):
        tf = pml.TextFormatter(self.sp.cfg.paperWidth,
                               self.sp.cfg.paperHeight, 15.0, 12)

        ls = self.sp.lines

        total = len(ls)
        tf.addText("%5d Lines in Screenplay" % total)

        tf.addSpace(2.0)

        for t in config.getTIs():
            cnt = sum([1 for line in ls if line.lt == t.lt])
            tf.addText("        %13s  %4d (%d%%)" % (t.name, cnt,
                                                      util.pct(cnt, total)))

        tf.addSpace(4.0)

        intLines = sum([si.lines for si in self.sr.scenes if
                        util.upper(si.name).startswith("INT.")])
        extLines = sum([si.lines for si in self.sr.scenes if
                        util.upper(si.name).startswith("EXT.")])

        tf.addText("%d%% Interior / %d%% Exterior Scenes" % (
            util.pct(intLines, intLines + extLines),
            util.pct(extLines, intLines + extLines)))

        tf.addSpace(4.0)

        tf.addText("Scene Length in Lines: %d Max / %.2f Avg." % (
            self.sr.longestScene, self.sr.avgScene))

        # lengths of action elements
        actions = []

        # length of current action element
        curLen = 0

        for ln in ls:
            if curLen > 0:
                if ln.lt == screenplay.ACTION:
                    curLen += 1

                    if ln.lb == screenplay.LB_LAST:
                        actions.append(curLen)
                        curLen = 0
                else:
                    actions.append(curLen)
                    curLen = 0
            else:
                if ln.lt == screenplay.ACTION:
                    curLen = 1

        if curLen > 0:
            actions.append(curLen)

        tf.addSpace(4.0)

        # avoid divide-by-zero
        if len(actions) > 0:
            maxA = max(actions)
            avgA = sum(actions) / float(len(actions))
        else:
            maxA = 0
            avgA = 0.0

        tf.addText("Action Length in Lines: %d Max / %.2f Avg." % (
            maxA, avgA))

        tf.addSpace(4.0)

        tf.addText("%d Speaking Characters" % len(self.cr.cinfo))

        return pdf.generate(tf.doc)
