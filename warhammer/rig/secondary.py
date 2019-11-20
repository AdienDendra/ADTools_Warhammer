import maya.cmds as mc
import ADCtrl as ac

reload(ac)

class Build:
    def __init__(self,
                 nostrilJnt,
                 cheekUpJnt,
                 cheekDownJnt,
                 eyebrowInJnt,
                 eyebrowMidJnt,
                 eyebrowOutJnt,
                 browInJnt,
                 browMidJnt,
                 browOutJnt,
                 eyelidPinchJnt,
                 scale,
                 side
                 ):

        # check position
        pos = mc.xform(nostrilJnt, ws=1, q=1, t=1)[0]

        nostrilCtrl = ac.Control(matchPos=nostrilJnt,
                                      prefix='nostril',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 0.5,
                                      ctrlColor='yellow', lockChannels=['v'], side=side)

        self.nostrilCtrl = nostrilCtrl.control
        self.nostrilCtrlGrp = nostrilCtrl.parentControl[0]

        cheekUpCtrl = ac.Control(matchPos=cheekUpJnt,
                                      prefix='cheekUp',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='yellow', lockChannels=['v'], side=side)

        self.cheekUpCtrl = cheekUpCtrl.control
        self.cheekUpCtrlGrp = cheekUpCtrl.parentControl[0]

        cheekDownCtrl = ac.Control(matchPos=cheekDownJnt,
                                        prefix='cheekDown',
                                        shape=ac.JOINT, groupsCtrl=[''],
                                        ctrlSize=scale * 1.0,
                                        ctrlColor='yellow', lockChannels=['v'], side=side)

        self.cheekDownCtrl = cheekDownCtrl.control
        self.cheekDownCtrlGrp = cheekDownCtrl.parentControl[0]

        eyebrowInCtrl = ac.Control(matchPos=eyebrowInJnt,
                                        prefix='eyebrowIn',
                                        shape=ac.CUBE, groupsCtrl=[''],
                                        ctrlSize=scale * 0.5,
                                        ctrlColor='blue', lockChannels=['v'], side=side)

        self.eyebrowInCtrl = eyebrowInCtrl.control
        self.eyebrowInCtrlGrp = eyebrowInCtrl.parentControl[0]

        eyebrowMidCtrl = ac.Control(matchPos=eyebrowMidJnt,
                                         prefix='eyebrowMid',
                                         shape=ac.CUBE, groupsCtrl=[''],
                                         ctrlSize=scale * 0.5,
                                         ctrlColor='blue', lockChannels=['v'], side=side)

        self.eyebrowMidCtrl = eyebrowMidCtrl.control
        self.eyebrowMidCtrlGrp = eyebrowMidCtrl.parentControl[0]

        eyebrowOutCtrl = ac.Control(matchPos=eyebrowOutJnt,
                                         prefix='eyebrowOut',
                                         shape=ac.CUBE, groupsCtrl=[''],
                                         ctrlSize=scale * 0.5,
                                         ctrlColor='blue', lockChannels=['v'], side=side)

        self.eyebrowOutCtrl = eyebrowOutCtrl.control
        self.eyebrowOutCtrlGrp = eyebrowOutCtrl.parentControl[0]

        eyebrowCtrl = ac.Control(matchPos=eyebrowInJnt,
                                 matchPosTwo=eyebrowOutJnt,
                                 prefix='eyebrows',
                                 shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                 ctrlSize=scale * 3.0,
                                 ctrlColor='yellow', lockChannels=['v'], side=side)

        self.eyebrowCtrl = eyebrowCtrl.control
        self.eyebrowCtrlGrp = eyebrowCtrl.parentControl[0]

        browInCtrl = ac.Control(matchPos=browInJnt,
                                     prefix='browIn',
                                     shape=ac.JOINT, groupsCtrl=[''],
                                     ctrlSize=scale * 0.4,
                                     ctrlColor='red', lockChannels=['v'], side=side)

        self.browInCtrl = browInCtrl.control
        self.browInCtrlGrp = browInCtrl.parentControl[0]

        browMidCtrl = ac.Control(matchPos=browMidJnt,
                                      prefix='browMid',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 0.4,
                                      ctrlColor='red', lockChannels=['v'], side=side)

        self.browMidCtrl = browMidCtrl.control
        self.browMidCtrlGrp = browMidCtrl.parentControl[0]

        browOutCtrl = ac.Control(matchPos=browOutJnt,
                                      prefix='browOut',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 0.4,
                                      ctrlColor='red', lockChannels=['v'], side=side)

        self.browOutCtrl = browOutCtrl.control
        self.browOutCtrlGrp = browOutCtrl.parentControl[0]

        eyelidPinchCtrl = ac.Control(matchPos=eyelidPinchJnt,
                                      prefix='eyelidPinch',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='blue', lockChannels=['v'], side=side)

        self.eyelidPinchCtrl = eyelidPinchCtrl.control
        self.eyelidPinchCtrlGrp = eyelidPinchCtrl.parentControl[0]

    # flipping the controller
        if pos <0:
            mc.setAttr(self.nostrilCtrlGrp+ '.scaleX', -1)
            mc.setAttr(self.cheekUpCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.cheekDownCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.eyebrowInCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.eyebrowMidCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.eyebrowOutCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browInCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browMidCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.browOutCtrlGrp + '.scaleX', -1)

        mc.parentConstraint(self.nostrilCtrl, nostrilJnt)
        mc.parentConstraint(self.cheekUpCtrl, cheekUpJnt)
        mc.parentConstraint(self.cheekDownCtrl, cheekDownJnt)
        mc.parentConstraint(self.eyebrowInCtrl, eyebrowInJnt)
        mc.parentConstraint(self.eyebrowMidCtrl, eyebrowMidJnt)
        mc.parentConstraint(self.eyebrowOutCtrl, eyebrowOutJnt)
        mc.parentConstraint(self.browInCtrl, browInJnt)
        mc.parentConstraint(self.browMidCtrl, browMidJnt)
        mc.parentConstraint(self.browOutCtrl, browOutJnt)
        mc.parentConstraint(self.eyelidPinchCtrl, eyelidPinchJnt)

        mc.scaleConstraint(self.nostrilCtrl, nostrilJnt)
        mc.scaleConstraint(self.cheekUpCtrl, cheekUpJnt)
        mc.scaleConstraint(self.cheekDownCtrl, cheekDownJnt)
        mc.scaleConstraint(self.eyebrowInCtrl, eyebrowInJnt)
        mc.scaleConstraint(self.eyebrowMidCtrl, eyebrowMidJnt)
        mc.scaleConstraint(self.eyebrowOutCtrl, eyebrowOutJnt)
        mc.scaleConstraint(self.browInCtrl, browInJnt)
        mc.scaleConstraint(self.browMidCtrl, browMidJnt)
        mc.scaleConstraint(self.browOutCtrl, browOutJnt)
        mc.scaleConstraint(self.eyelidPinchCtrl, eyelidPinchJnt)

        mc.parent(self.eyebrowInCtrlGrp, self.eyebrowMidCtrlGrp, self.eyebrowOutCtrlGrp,
                  self.eyebrowCtrl)