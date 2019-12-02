import maya.cmds as mc
import ADCtrl as ac, ADUtils as au

reload(ac)

class Build:
    def __init__(self,
                 nostrilJnt,
                 earJnt,
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
                 objectFolMesh,
                 sideRGT,
                 sideLFT,
                 side,
                 headCtrl,
                 headUpCtrl,
                 headLowCtrl
                 ):

        # check position
        pos = mc.xform(nostrilJnt, ws=1, q=1, t=1)[0]

        nostrilCtrl = ac.Control(matchPos=nostrilJnt,
                                      prefix='nostril',
                                      shape=ac.JOINT, groupsCtrl=['','Offset'],
                                      ctrlSize=scale * 0.5,
                                      ctrlColor='yellow', lockChannels=['v'], side=side)

        cheekUpCtrl = ac.Control(matchPos=cheekUpJnt,
                                      prefix='cheekUp',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='yellow', lockChannels=['v'], side=side)

        cheekDownCtrl = ac.Control(matchPos=cheekDownJnt,
                                        prefix='cheekDown',
                                        shape=ac.JOINT, groupsCtrl=[''],
                                        ctrlSize=scale * 1.0,
                                        ctrlColor='yellow', lockChannels=['v'], side=side)

        eyebrowInCtrl = ac.Control(matchPos=eyebrowInJnt,
                                        prefix='eyebrowIn',
                                        shape=ac.CUBE, groupsCtrl=[''],
                                        ctrlSize=scale * 0.5,
                                        ctrlColor='blue', lockChannels=['v'], side=side)

        eyebrowMidCtrl = ac.Control(matchPos=eyebrowMidJnt,
                                         prefix='eyebrowMid',
                                         shape=ac.CUBE, groupsCtrl=[''],
                                         ctrlSize=scale * 0.5,
                                         ctrlColor='blue', lockChannels=['v'], side=side)

        eyebrowOutCtrl = ac.Control(matchPos=eyebrowOutJnt,
                                         prefix='eyebrowOut',
                                         shape=ac.CUBE, groupsCtrl=[''],
                                         ctrlSize=scale * 0.5,
                                         ctrlColor='blue', lockChannels=['v'], side=side)

        eyebrowCtrl = ac.Control(matchPos=eyebrowInJnt,
                                 matchPosTwo=eyebrowOutJnt,
                                 prefix='eyebrows',
                                 shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                 ctrlSize=scale * 3.0,
                                 ctrlColor='yellow', lockChannels=['v'], side=side)

        browInCtrl = ac.Control(matchPos=browInJnt,
                                     prefix='browIn',
                                     shape=ac.JOINT, groupsCtrl=[''],
                                     ctrlSize=scale * 0.4,
                                     ctrlColor='red', lockChannels=['v'], side=side)

        browMidCtrl = ac.Control(matchPos=browMidJnt,
                                      prefix='browMid',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 0.4,
                                      ctrlColor='red', lockChannels=['v'], side=side)

        browOutCtrl = ac.Control(matchPos=browOutJnt,
                                      prefix='browOut',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 0.4,
                                      ctrlColor='red', lockChannels=['v'], side=side)

        eyelidPinchCtrl = ac.Control(matchPos=eyelidPinchJnt,
                                      prefix='eyelidPinch',
                                      shape=ac.JOINT, groupsCtrl=[''],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='blue', lockChannels=['v'], side=side)

        earCtrl = ac.Control(matchPos=earJnt,
                                      prefix='ear',
                                      shape=ac.CUBE, groupsCtrl=[''],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='blue', lockChannels=['v'], side=side)


    # ==================================================================================================================
    #                                            ASSIGNING THE INSTANCE NAME
    # ==================================================================================================================

        self.nostrilCtrl = nostrilCtrl.control
        self.nostrilCtrlGrp = nostrilCtrl.parentControl[0]
        self.nostrilCtrlOffset = nostrilCtrl.parentControl[1]

        self.cheekUpCtrl = cheekUpCtrl.control
        self.cheekUpCtrlGrp = cheekUpCtrl.parentControl[0]

        self.cheekDownCtrl = cheekDownCtrl.control
        self.cheekDownCtrlGrp = cheekDownCtrl.parentControl[0]

        self.eyebrowInCtrl = eyebrowInCtrl.control
        self.eyebrowInCtrlGrp = eyebrowInCtrl.parentControl[0]

        self.eyebrowMidCtrl = eyebrowMidCtrl.control
        self.eyebrowMidCtrlGrp = eyebrowMidCtrl.parentControl[0]

        self.eyebrowOutCtrl = eyebrowOutCtrl.control
        self.eyebrowOutCtrlGrp = eyebrowOutCtrl.parentControl[0]

        self.eyebrowCtrl = eyebrowCtrl.control
        self.eyebrowCtrlGrp = eyebrowCtrl.parentControl[0]

        self.browInCtrl = browInCtrl.control
        self.browInCtrlGrp = browInCtrl.parentControl[0]

        self.browMidCtrl = browMidCtrl.control
        self.browMidCtrlGrp = browMidCtrl.parentControl[0]

        self.browOutCtrl = browOutCtrl.control
        self.browOutCtrlGrp = browOutCtrl.parentControl[0]

        self.eyelidPinchCtrl = eyelidPinchCtrl.control
        self.eyelidPinchCtrlGrp = eyelidPinchCtrl.parentControl[0]

        self.earCtrl = earCtrl.control
        self.earCtrlGrp = earCtrl.parentControl[0]

    # ==================================================================================================================
    #                                           EYEBROW CONTROLLER SETUP
    # ==================================================================================================================
        mc.parent(self.eyebrowInCtrlGrp, self.eyebrowMidCtrlGrp, self.eyebrowOutCtrlGrp,
                  self.eyebrowCtrl)

    # GROUPING FOR OFFSET
        mc.select(cl=1)
        self.ctrlGrpEyebrowInCenter = mc.group(em=1, n='eyebrowInCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpEyebrowInCenter = mc.group(em=1, n='eyebrowInCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpEyebrowInCenter, self.ctrlGrpEyebrowInCenter)

        mc.select(cl=1)
        self.ctrlGrpEyebrowMidCenter = mc.group(em=1, n='eyebrowMidCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpEyebrowMidCenter = mc.group(em=1, n='eyebrowMidCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpEyebrowMidCenter, self.ctrlGrpEyebrowMidCenter)

        mc.select(cl=1)
        self.ctrlGrpEyebrowOutCenter = mc.group(em=1, n='eyebrowOutCtrlCenter' + side + '_grp')
        self.ctrlOffsetGrpEyebrowOutCenter = mc.group(em=1, n='eyebrowOutCtrlOffsetCenter' + side + '_grp')
        mc.parent(self.ctrlOffsetGrpEyebrowOutCenter, self.ctrlGrpEyebrowOutCenter)

    # CREATE GROUP CORESPONDENT THE JOINTS
        au.createParentTransform(listparent=['', 'Offset'], object=nostrilJnt, matchPos=nostrilJnt, prefix='nostril', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=cheekUpJnt, matchPos=cheekUpJnt, prefix='cheekUp', suffix='_jnt', side=side)
        self.cheekDownJntGrp = au.createParentTransform(listparent=[''], object=cheekDownJnt, matchPos=cheekDownJnt, prefix='cheekDown', suffix='_jnt', side=side)
        eyebrowInGrp = au.createParentTransform(listparent=['', 'Offset'], object=eyebrowInJnt, matchPos=eyebrowInJnt, prefix='eyebrowIn', suffix='_jnt', side=side)
        eyebrowMidGrp = au.createParentTransform(listparent=['', 'Offset'], object=eyebrowMidJnt, matchPos=eyebrowMidJnt, prefix='eyebrowMid', suffix='_jnt', side=side)
        eyebrowOutGrp = au.createParentTransform(listparent=['', 'Offset'], object=eyebrowOutJnt, matchPos=eyebrowOutJnt, prefix='eyebrowOut', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=browInJnt, matchPos=browInJnt, prefix='browIn', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=browMidJnt, matchPos=browMidJnt, prefix='browMid', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=browOutJnt, matchPos=browOutJnt, prefix='browOut', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=eyelidPinchJnt, matchPos=eyelidPinchJnt, prefix='eyelidPinch', suffix='_jnt', side=side)

    # EYBROW MAIN OFFSET GRP JOINT TRANSFORM
        eyebrowInMain = self.mainGroupBindConnection(name='eyebrowIn', side=side, objectParent=eyebrowInGrp[0])
        eyebrowMidMain = self.mainGroupBindConnection(name='eyebrowMid', side=side, objectParent=eyebrowMidGrp[0])
        eyebrowOutMain = self.mainGroupBindConnection(name='eyebrowOut', side=side, objectParent=eyebrowOutGrp[0])

    # SHIFTING PARENT JOINT TO MAIN OFFSET GRP EYEBROW
        mc.parent(eyebrowInGrp[1], eyebrowInMain)
        mc.parent(eyebrowMidGrp[1], eyebrowMidMain)
        mc.parent(eyebrowOutGrp[1], eyebrowOutMain)

    # CONTROLLER ACCORDING THE FOLLICLE
        object = [self.nostrilCtrlGrp, self.cheekDownCtrlGrp, self.cheekUpCtrlGrp,  self.eyebrowInCtrlGrp, self.eyebrowMidCtrlGrp,
                  self.eyebrowOutCtrlGrp, self.browInCtrlGrp, self.browMidCtrlGrp, self.browOutCtrlGrp, self.eyelidPinchCtrlGrp]

        self.follicleTransformAll=[]
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            self.follicleTransformAll.append(follicleTransform)

    # SCALE CONSTRAINT
        mc.scaleConstraint(headCtrl,  self.follicleTransformAll[0])
        mc.scaleConstraint(headLowCtrl, self.follicleTransformAll[1])
        for b in self.follicleTransformAll[2:]:
            mc.scaleConstraint(headUpCtrl, b)


    # FLIPPING THE CONTROLLER
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
            mc.setAttr(self.eyelidPinchCtrlGrp + '.scaleX', -1)
            mc.setAttr(self.ctrlGrpEyebrowInCenter+ '.scaleX', -1)
            mc.setAttr(self.ctrlGrpEyebrowMidCenter+ '.scaleX', -1)
            mc.setAttr(self.ctrlGrpEyebrowOutCenter+ '.scaleX', -1)
            mc.setAttr(self.earCtrlGrp+ '.scaleX', -1)
            mc.setAttr(self.eyebrowCtrlGrp+ '.scaleX', -1)

            self.reverseNode(self.nostrilCtrl, nostrilJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.cheekUpCtrl, cheekUpJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.cheekDownCtrl, cheekDownJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowInCtrl, eyebrowInJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowMidCtrl, eyebrowMidJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowOutCtrl, eyebrowOutJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browInCtrl, browInJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browMidCtrl, browMidJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.browOutCtrl, browOutJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.eyelidPinchCtrl, eyelidPinchJnt, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowCtrl, eyebrowInMain, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowCtrl, eyebrowMidMain, sideRGT, sideLFT, side)
            self.reverseNode(self.eyebrowCtrl, eyebrowOutMain, sideRGT, sideLFT, side)

            au.connectAttrScale(self.nostrilCtrl, nostrilJnt)
            au.connectAttrScale(self.cheekUpCtrl, cheekUpJnt)
            au.connectAttrScale(self.cheekDownCtrl, cheekDownJnt)
            au.connectAttrScale(self.eyebrowInCtrl, eyebrowInJnt)
            au.connectAttrScale(self.eyebrowMidCtrl, eyebrowMidJnt)
            au.connectAttrScale(self.eyebrowOutCtrl, eyebrowOutJnt)
            au.connectAttrScale(self.browInCtrl, browInJnt)
            au.connectAttrScale(self.browMidCtrl, browMidJnt)
            au.connectAttrScale(self.browOutCtrl, browOutJnt)
            au.connectAttrScale(self.eyelidPinchCtrl, eyelidPinchJnt)
            au.connectAttrScale(self.eyebrowCtrl, eyebrowInMain)
            au.connectAttrScale(self.eyebrowCtrl, eyebrowMidMain)
            au.connectAttrScale(self.eyebrowCtrl, eyebrowOutMain)

        else:
            au.connectAttrObject(self.nostrilCtrl, nostrilJnt)
            au.connectAttrObject(self.cheekUpCtrl, cheekUpJnt)
            au.connectAttrObject(self.cheekDownCtrl, cheekDownJnt)
            au.connectAttrObject(self.eyebrowInCtrl, eyebrowInJnt)
            au.connectAttrObject(self.eyebrowMidCtrl, eyebrowMidJnt)
            au.connectAttrObject(self.eyebrowOutCtrl, eyebrowOutJnt)
            au.connectAttrObject(self.browInCtrl, browInJnt)
            au.connectAttrObject(self.browMidCtrl, browMidJnt)
            au.connectAttrObject(self.browOutCtrl, browOutJnt)
            au.connectAttrObject(self.eyelidPinchCtrl, eyelidPinchJnt)
            au.connectAttrObject(self.eyebrowCtrl, eyebrowInMain)
            au.connectAttrObject(self.eyebrowCtrl, eyebrowMidMain)
            au.connectAttrObject(self.eyebrowCtrl, eyebrowOutMain)

    # CONSTRAINT EARS
        mc.parentConstraint(self.earCtrl, earJnt, mo=1)
        mc.scaleConstraint(self.earCtrl, earJnt, mo=1)

    # EYEBROW EXCEPTION PARENTING CTRL
        mc.delete(mc.pointConstraint(self.eyebrowCtrl, self.ctrlGrpEyebrowInCenter))
        mc.delete(mc.pointConstraint(self.eyebrowCtrl, self.ctrlGrpEyebrowMidCenter))
        mc.delete(mc.pointConstraint(self.eyebrowCtrl, self.ctrlGrpEyebrowOutCenter))

        # grouping to follicle
        mc.parent(self.ctrlGrpEyebrowInCenter,  self.follicleTransformAll[3])
        mc.parent(self.ctrlGrpEyebrowMidCenter,  self.follicleTransformAll[4])
        mc.parent(self.ctrlGrpEyebrowOutCenter,  self.follicleTransformAll[5])

        # regrouping to offset grp
        mc.parent(self.eyebrowInCtrlGrp, self.ctrlOffsetGrpEyebrowInCenter)
        mc.parent(self.eyebrowMidCtrlGrp, self.ctrlOffsetGrpEyebrowMidCenter)
        mc.parent(self.eyebrowOutCtrlGrp, self.ctrlOffsetGrpEyebrowOutCenter)

        # connect attr
        au.connectAttrObject(self.eyebrowCtrl, self.ctrlOffsetGrpEyebrowInCenter)
        au.connectAttrObject(self.eyebrowCtrl, self.ctrlOffsetGrpEyebrowMidCenter)
        au.connectAttrObject(self.eyebrowCtrl, self.ctrlOffsetGrpEyebrowOutCenter)

    def reverseNode(self, object, targetJnt, sideRGT, sideLFT, side):
        if sideRGT in targetJnt:
            newName = targetJnt.replace(sideRGT, '')
        elif sideLFT in targetJnt:
            newName = targetJnt.replace(sideLFT, '')
        else:
            newName = targetJnt

        transMdn = mc.createNode('multiplyDivide', n=au.prefixName(newName)+'Trans'+ side+ '_mdn')
        mc.connectAttr(object+'.translate', transMdn+'.input1')
        mc.setAttr(transMdn+'.input2X', -1)
        mc.connectAttr(transMdn+'.output', targetJnt +'.translate')

        rotMdn = mc.createNode('multiplyDivide', n=au.prefixName(newName)+'Rot' + side+'_mdn')
        mc.connectAttr(object+'.rotate', rotMdn+'.input1')
        mc.setAttr(rotMdn+'.input2Y', -1)
        mc.setAttr(rotMdn+'.input2Z', -1)
        mc.connectAttr(rotMdn+'.output', targetJnt+'.rotate')

    def mainGroupBindConnection(self, name, side, objectParent):
        # EYBROW MAIN OFFSET GRP JOINT TRANSFORM
        eyebrowMainBindGrp = mc.group(em=1, n=name+'Main' + side + '_grp')
        eyebrowMainBindOffset = mc.group(em=1, n=name+'MainOffset' + side + '_grp', p=eyebrowMainBindGrp)
        mc.delete(mc.parentConstraint(self.eyebrowCtrl, eyebrowMainBindGrp))

        mc.parent(eyebrowMainBindGrp, objectParent)

        return eyebrowMainBindOffset