import maya.cmds as mc
from warhammer.rig import eyelid as el
import ADCtrl as ct, ADUtils as au


reload(el)
reload(ct)
reload(au)

class Eyelid:
    def __init__(self, crvUp,
                 crvDown,
                 headUpJoint,
                 eyeballJnt,
                 prefixEyeball,
                 prefixEyeballAim,
                 scale,
                 side,
                 directionLid01,
                 directionLid02,
                 positionEyeAimCtrl,
                 eyeballAimMainCtrl
                 ):

        worldUpObject = mc.spaceLocator(n='eyeballWorldObj'+side+'_loc')[0]
        mc.delete(mc.parentConstraint(eyeballJnt, worldUpObject))
        value = mc.getAttr(worldUpObject + '.translateY')
        mc.setAttr(worldUpObject + '.translateY', value + (10 * scale))
        mc.parentConstraint(headUpJoint, worldUpObject, mo=1)
        self.worldUpObject = worldUpObject

        # EYELID UP LFT
        self.eyelidUp = el.Build(crv=crvUp,
                                 worldUpObject=worldUpObject,
                                 eyeballJnt=eyeballJnt,
                                 scale=1,
                                 directionLip01=directionLid01,
                                 directionLip02=directionLid02,
                                 side=side,
                                 ctrlColor='yellow',
                                 controllerLidDown=False)

        self.eyelidDown = el.Build(crv=crvDown,
                                   worldUpObject=worldUpObject,
                                   eyeballJnt=eyeballJnt,
                                   scale=1,
                                   directionLip01=directionLid01,
                                   directionLip02=directionLid02,
                                   side=side,
                                   ctrlColor='yellow',
                                   controllerLidDown=True)

        # BLINK SETUP
        blink = self.blinkSetup(eyeballJnt=eyeballJnt, prefixEyeball=prefixEyeball,
                                prefixEyeballAim=prefixEyeballAim, crvUp=crvUp,
                                crvDown=crvDown, scale=scale, side=side, eyelidUp=self.eyelidUp,
                                eyelidDown=self.eyelidDown, positionEyeAimCtrl=positionEyeAimCtrl,
                                worldUpObject=worldUpObject,
                                eyeballAimMainCtrl=eyeballAimMainCtrl,
                                controllerBind03OffsetCtrlUp=self.eyelidUp.controllerBind03OffsetCtrl,
                                controllerBind03OffsetCtrlDown=self.eyelidDown.controllerBind03OffsetCtrl,
                                jointBind03GrpAllUp=self.eyelidUp.jointBind03GrpAll,
                                jointBind03GrpAllDown=self.eyelidDown.jointBind03GrpAll,
                                jointBind03GrpOffsetDown=self.eyelidUp.jointBind03GrpOffset,
                                jointBind03GrpOffsetUp=self.eyelidDown.jointBind03GrpOffset)

        #PARENT TO GRP
        mc.parent(self.eyelidUp.jointGrp, self.eyelidUp.locatorGrp,
                  self.eyelidUp.curvesGrp, self.eyelidUp.jointGrp,
                  self.eyelidDown.jointGrp, self.eyelidDown.locatorGrp,
                  self.eyelidDown.curvesGrp, self.eyelidDown.jointGrp,  blink
                  )


    # ==================================================================================================================
    #                                                  CORNER CONTROLLER
    # ==================================================================================================================
        # controller in corner
        lidCornerCtrlIn = self.cornerCtrl(matchPosOne=self.eyelidUp.jnt01,
                                          matchPosTwo=self.eyelidDown.jnt01,
                                          prefix='eyelidCornerIn',
                                          scale=scale,
                                          side=side)

        # controller in corner
        lidCornerCtrlOut = self.cornerCtrl(matchPosOne=self.eyelidUp.jnt05,
                                           matchPosTwo=self.eyelidDown.jnt05,
                                           prefix='eyelidCornerOut',
                                           scale=scale,
                                           side=side)

        pos = mc.xform(lidCornerCtrlOut[0], ws=1, q=1, t=1)[0]
        if pos > 0:
            # parent constraint corner grp bind jnt
            au.connectAttrTransRot(lidCornerCtrlIn[0], self.eyelidUp.jointBind01Grp[1])
            au.connectAttrTransRot(lidCornerCtrlIn[0], self.eyelidDown.jointBind01Grp[1])
            au.connectAttrTransRot(lidCornerCtrlOut[0], self.eyelidUp.jointBind05Grp[1])
            au.connectAttrTransRot(lidCornerCtrlOut[0], self.eyelidDown.jointBind05Grp[1])
        else:
            self.cornerReverseNode(lidCornerCtrl=lidCornerCtrlOut[0], side=side, lidCornerName='lidCornerOut',
                                   targetUp=self.eyelidUp.jointBind05Grp[1], targetDown=self.eyelidDown.jointBind05Grp[1])

            self.cornerReverseNode(lidCornerCtrl=lidCornerCtrlIn[0], side=side, lidCornerName='lidCornerIn',
                                   targetUp=self.eyelidUp.jointBind01Grp[1], targetDown=self.eyelidDown.jointBind01Grp[1])

        mc.parent(self.eyelidUp.controllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(self.eyelidDown.controllerBindGrpZro01, lidCornerCtrlIn[0])
        mc.parent(self.eyelidUp.controllerBindGrpZro05, lidCornerCtrlOut[0])
        mc.parent(self.eyelidDown.controllerBindGrpZro05, lidCornerCtrlOut[0])

        mc.parent(self.eyelidUp.bindJntGrp, self.eyelidDown.bindJntGrp,  self.eyelidUp.grpDrvCtrl, self.eyelidDown.grpDrvCtrl,
                  lidCornerCtrlIn[1], lidCornerCtrlOut[1], self.eyeballCtrl.control)

    def cornerReverseNode(self, lidCornerCtrl, side, lidCornerName='', targetUp='', targetDown=''):
        transRev = mc.createNode('multiplyDivide', n=lidCornerName + 'Trans' + side + '_mdn')
        rotRev = mc.createNode('multiplyDivide', n=lidCornerName+ 'Rot' + side + '_mdn')
        mc.connectAttr(lidCornerCtrl + '.translate', transRev + '.input1')
        mc.setAttr(transRev + '.input2X', -1)

        mc.connectAttr(lidCornerCtrl + '.rotate', rotRev + '.input1')
        mc.setAttr(rotRev + '.input2Y', -1)
        mc.setAttr(rotRev + '.input2Z', -1)

        mc.connectAttr(transRev + '.output', targetUp + '.translate')
        mc.connectAttr(rotRev + '.output', targetUp + '.rotate')
        mc.connectAttr(transRev + '.output', targetDown + '.translate')
        mc.connectAttr(rotRev + '.output', targetDown + '.rotate')

    def cornerCtrl(self, matchPosOne, matchPosTwo, prefix, scale, side):
        cornerCtrl = ct.Control(matchPos=matchPosOne, matchPosTwo=matchPosTwo,
                                prefix=prefix,
                                shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset'],
                                ctrlSize=scale * 0.3,
                                ctrlColor='blue', lockChannels=['v', 's'], side=side)

        # check position
        pos = mc.xform(cornerCtrl.control, ws=1, q=1, t=1)[0]

        # flipping the controller
        if pos < 0:
            mc.setAttr(cornerCtrl.parentControl[0] + '.scaleX', -1)

        self.control = cornerCtrl.control
        self.parentControlZro = cornerCtrl.parentControl[0]
        self.parentControlOffset = cornerCtrl.parentControl[1]

        return cornerCtrl.control, cornerCtrl.parentControl[0]

    def blinkSetup(self, eyeballJnt, prefixEyeball, prefixEyeballAim, crvUp, crvDown, scale,
                   side, eyelidUp, eyelidDown, positionEyeAimCtrl, worldUpObject, eyeballAimMainCtrl,
                   controllerBind03OffsetCtrlUp, controllerBind03OffsetCtrlDown, jointBind03GrpAllUp, jointBind03GrpAllDown,
                   jointBind03GrpOffsetDown, jointBind03GrpOffsetUp):

        # ==============================================================================================================
        #                                             EYEBALL CONTROLLER
        # ==============================================================================================================

        eyballGrp = au.createParentTransform(listparent=['Zro', 'Offset'], object=eyeballJnt, matchPos=eyeballJnt,
                                             prefix='eyeball',
                                             suffix='_jnt', side=side)

        self.eyeballCtrl = ct.Control(matchPos=eyeballJnt,
                                      prefix=prefixEyeball,
                                      shape=ct.JOINTPLUS, groupsCtrl=['Zro', 'Offset'],
                                      ctrlSize=scale * 2,
                                      ctrlColor='blue', lockChannels=['v', 's'], side=side, connect=['connectMatrixAll'])


        # ADD ATTRIBUTE
        au.addAttribute(objects=[self.eyeballCtrl.control], longName=['eyelidDegree'], niceName=[' '], at="enum",
                        en='Eyelid Degree', cb=True)

        self.eyelidPos = au.addAttribute(objects=[self.eyeballCtrl.control], longName=['eyelidPos'],
                                         attributeType="float", min=0, max=1, dv=0.5, k=True)

        self.eyelidFollow = au.addAttribute(objects=[self.eyeballCtrl.control], longName=['eyelidFollow'],
                                         attributeType="float", min=0, max=2, dv=1, k=True)

        # ==============================================================================================================
        #                                             EYEBALL AIM
        # ==============================================================================================================
        if mc.xform(eyeballJnt, q=1, ws=1, t=1)[0] > 0:
            ctrlColor ='red'
        else:
            ctrlColor='yellow'

        self.eyeballAimCtrl = ct.Control(matchPos=eyeballJnt,
                                      prefix=prefixEyeballAim,
                                      shape=ct.LOCATOR, groupsCtrl=['Zro', 'Offset'],
                                      ctrlSize=scale * 0.2,
                                      ctrlColor=ctrlColor, lockChannels=['v','r','s'], side=side)

        eyeballAimCtrl = self.eyeballAimCtrl.control

        getAttribute = mc.getAttr(self.eyeballAimCtrl.parentControl[0]+'.translateZ')
        mc.setAttr(self.eyeballAimCtrl.parentControl[0]+'.translateZ', getAttribute+(positionEyeAimCtrl*scale))

        mc.aimConstraint(self.eyeballAimCtrl.control, eyballGrp[1], mo=1, weight=1, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                         worldUpType="object", worldUpObject=worldUpObject)

        # PARENT EYE AIM TO EYEBALL AIM MAIN CTRL
        mc.parent(self.eyeballAimCtrl.parentControl[0], eyeballAimMainCtrl)

        # EXPRESSION UP AND DOWN FOLLOW EYELID CTRL
        expressionEyelidCtrl= "$range = {5}.{1}; " \
                            "$a = 20 /$range; " \
                            "$b = 30 /$range; " \
                            "$c = 80 /$range;" \
                            "{2}.translateX = {3}.translateX /$c + {0}.translateX /$c;" \
                           "{2}.translateY = {3}.translateY /$a + {0}.translateY /$a;" \
                           "{4}.translateX = {3}.translateX /$c + {0}.translateX /$c;" \
                           "{4}.translateY = -{3}.translateY /$b - {0}.translateY /$b;"\
            \
            .format(eyeballAimCtrl,  # 0
                    self.eyelidFollow,  # 1
                    controllerBind03OffsetCtrlUp,  # 2
                    eyeballAimMainCtrl,# 3
                    controllerBind03OffsetCtrlDown,
                    self.eyeballCtrl.control
                    )

        mc.expression(s=expressionEyelidCtrl, n="%s%s%s" % ('eyelidCtrl', side, '_expr'), ae=0)

        # EXPRESSION UP AND DOWN FOLLOW EYELID BIND
        expressionEyelidBind = "$range = {7}.{1}; " \
                               "$a = 30 /$range; " \
                               "$b = 8 /$range; " \
                               "$d = 12 /$range; " \
                               "$c = 60 /$range;" \
                               "if ({0}.translateY >= 0) " \
                               "{8} " \
                               "{2}.translateY = {0}.translateY /$b; " \
                               "{3}.translateY = {0}.translateY /$b;" \
                               "{9} " \
                               "else if ({0}.translateY < 0)" \
                               "{8}" \
                               "{2}.translateY = {0}.translateY /$d; " \
                               "{3}.translateY = {0}.translateY /$a;" \
                               "{9} " \
                               "{2}.translateX = {0}.translateX /$c; " \
                               "{3}.translateX = {0}.translateX /$c; " \
                               "if ({6}.translateY >= 0) " \
                               "{8}" \
                               "{4}.translateY = {6}.translateY /$b; " \
                               "{5}.translateY = {6}.translateY /$b;" \
                               "{9} " \
                               "else if ({6}.translateY < 0) " \
                               "{8}" \
                               "{4}.translateY = {6}.translateY /$d; " \
                               "{5}.translateY = {6}.translateY /$a;" \
                               "{9} " \
                               "{4}.translateX = {6}.translateX /$c; " \
                               "{5}.translateX = {6}.translateX /$c;" \
            \
            .format(eyeballAimCtrl,
                    self.eyelidFollow,
                    jointBind03GrpAllUp,
                    jointBind03GrpAllDown,
                    jointBind03GrpOffsetUp,
                    jointBind03GrpOffsetDown,
                    eyeballAimMainCtrl,
                    self.eyeballCtrl.control,
                    "{",
                    "}")

        mc.expression(s=expressionEyelidBind, n="%s%s%s" % ('eyelidBind', side, '_expr'), ae=0)

        # ==============================================================================================================
        #                                                   BLINK
        # ==============================================================================================================
        # CREATE CURVE MID BLINK
        curveBlinkBindMidOld = mc.curve(d=3, ep=[(self.eyelidUp.xformJnt01), (self.eyelidUp.xformJnt05)])
        curveBlinkBindMidReb = mc.rebuildCurve(curveBlinkBindMidOld, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                                               kep=1, kt=0, s=8, d=3, tol=0.01)

        curveBlinkBindMid = mc.rename(curveBlinkBindMidReb, ('eyelidBlink' + side + '_crv'))

        curveBlinkUp = mc.duplicate(crvUp, n='eyelidBlinkUp'+side+'_crv')[0]
        curveBlinkDown = mc.duplicate(crvDown, n='eyelidBlinkDown'+side+'_crv')[0]

        blinkBsn = mc.blendShape(eyelidUp.deformCrv, eyelidDown.deformCrv, curveBlinkBindMid, n=('eyelidBlink' +side+ '_bsn'),
                      weight=[(0, 1), (1, 0)])[0]

        mc.select(cl=1)
        # wire deform up on mid curves
        stickyMidwireDefUp = mc.wire(curveBlinkUp, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefUp[0] = mc.rename(stickyMidwireDefUp[0], (au.prefixName(crvUp) + 'Blink' +side+ '_wireNode'))

        # SET TO DOWN CURVE
        mc.setAttr(blinkBsn+'.%s' % eyelidUp.deformCrv, 0)
        mc.setAttr(blinkBsn+'.%s'% eyelidDown.deformCrv, 1)

        mc.select(cl=1)
        # wire deform down on mid curves
        stickyMidwireDefDown = mc.wire(curveBlinkDown, dds=(0, 100 * scale), wire=curveBlinkBindMid)
        stickyMidwireDefDown[0] = mc.rename(stickyMidwireDefDown[0], (au.prefixName(crvDown) + 'Blink' + side+ '_wireNode'))

        # SET KEYFRAME
        mc.setDrivenKeyframe(blinkBsn +'.%s' % eyelidUp.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.eyelidPos),
                             dv=0, v=1, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn +'.%s' % eyelidUp.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.eyelidPos),
                             dv=1, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % eyelidDown.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.eyelidPos),
                             dv=0, v=0, itt='linear', ott='linear')

        mc.setDrivenKeyframe(blinkBsn + '.%s' % eyelidDown.deformCrv,
                             cd='%s.%s' % (self.eyeballCtrl.control, self.eyelidPos),
                             dv=1, v=1, itt='linear', ott='linear')

        # CONNECT TO BLENDSHAPE BIND CURVE
        eyelidUpBsn = mc.blendShape(curveBlinkUp, crvUp, n=('eyelidBlinkUp' +side+ '_bsn'),
                      weight=[(0, 1)])[0]

        mc.connectAttr(eyelidUp.controllerBind03Ctrl+'.%s' % eyelidUp.closeEyelid, eyelidUpBsn+'.%s'% curveBlinkUp)

        eyelidDownBsn = mc.blendShape(curveBlinkDown, crvDown, n=('eyelidBlinkDown' +side+ '_bsn'),
                      weight=[(0, 1)])[0]

        mc.connectAttr(eyelidDown.controllerBind03Ctrl+'.%s' % eyelidDown.closeEyelid, eyelidDownBsn+'.%s'% curveBlinkDown)

        # CREATE GROUP FOR EYELID STUFF
        eyelidGrp = mc.group(em=1, n='eyelid' + side + '_grp')

        return eyelidGrp