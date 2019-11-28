import maya.cmds as mc, maya.OpenMaya as om
import ADCtrl as ct, ADUtils as au

reload (ct)
reload (au)

# load Plug-ins
matrixNode = mc.pluginInfo('matrixNodes.mll', query=True, loaded=True)
quatNode = mc.pluginInfo('quatNodes.mll', query=True, loaded=True)

if not matrixNode:
    mc.loadPlugin( 'matrixNodes.mll' )

if not quatNode:
    mc.loadPlugin( 'quatNodes.mll' )

class Build:
    def __init__(self, crv, eyeballJnt, worldUpObject,
                 scale, side,
                 directionLip01, directionLip02,
                 ctrlColor, controllerLidDown):

        self.pos = mc.xform(eyeballJnt, q=1, ws=1, t=1)[0]

        self.prefixNameCrv = au.prefixName(crv)
        self.vtxCrv = mc.ls('%s.cv[0:*]' % crv, fl=True)

        self.createJointLid(crv=crv, worldUpObject=worldUpObject, scale=scale, eyeballJnt=eyeballJnt)

        self.wireBindCurve(crv=crv, scale=scale, side=side, directionLip01=directionLip01, eyeballJnt=eyeballJnt,
                           directionLip02=directionLip02)


        self.controllerLid(scale=scale, side=side,
                           controllerLidDown=controllerLidDown, ctrlColor=ctrlColor)


    def controllerLid(self, scale, side, controllerLidDown, ctrlColor):
        # controller 03
        self.controllerBind03 = ct.Control(matchPos=self.jnt03, prefix=self.prefixNameCrv+ '03',
                                           shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset'], ctrlSize=scale*0.4,
                                           ctrlColor='red', lockChannels=['v', 's'], side=side
                                           )
        # ADD ATTRIBUTE
        au.addAttribute(objects=[self.controllerBind03.control], longName=['eyelid'], niceName=[' '], at="enum",
                        en='Eyelid', cb=True)

        self.closeEyelid = au.addAttribute(objects=[self.controllerBind03.control], longName=['closeEyelid'],
                                           attributeType="float", min=0, max=1, dv=0, k=True)

        self.controllerBind03Ctrl = self.controllerBind03.control
        self.controllerBind03OffsetCtrl = self.controllerBind03.parentControl[1]

        # controller 01
        self.controllerBind01 = ct.Control(matchPos=self.jnt01, prefix=self.prefixNameCrv + '01',
                                           shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset', 'All'], ctrlSize=scale*0.15,
                                           ctrlColor=ctrlColor, lockChannels=['v', 's'], side=side
                                           )
        self.controllerBindGrpZro01 = self.controllerBind01.parentControl[0]

        # controller 02
        self.controllerBind02 = ct.Control(matchPos=self.jnt02, prefix=self.prefixNameCrv + '02',
                                           shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset'], ctrlSize=scale*0.2,
                                           ctrlColor=ctrlColor, lockChannels=['v', 's'], side=side
                                           )
        # controller 05
        self.controllerBind05 = ct.Control(matchPos=self.jnt05, prefix=self.prefixNameCrv + '05',
                                           shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset', 'All'], ctrlSize=scale*0.15,
                                           ctrlColor=ctrlColor, lockChannels=['v', 's'], side=side
                                           )
        self.controllerBindGrpZro05 = self.controllerBind05.parentControl[0]

        # controller 04
        self.controllerBind04 = ct.Control(matchPos=self.jnt04, prefix=self.prefixNameCrv + '04',
                                           shape=ct.CIRCLEPLUS, groupsCtrl=['Zro', 'Offset'], ctrlSize=scale*0.2,
                                           ctrlColor=ctrlColor, lockChannels=['v', 's'], side=side
                                           )

        # create grp controller and parent into it
        self.grpDrvCtrl = mc.createNode('transform', n=self.prefixNameCrv + 'Ctrl' + '_grp')
        mc.parent(self.controllerBind03.parentControl[0], self.controllerBind01.parentControl[0], self.controllerBind02.parentControl[0],
                  self.controllerBind05.parentControl[0], self.controllerBind04.parentControl[0], self.grpDrvCtrl)

        # # connect group parent bind joint 01 and 02 to the controller grp parent 01 and 02
        # au.connectAttrTransRot(self.jointBind02Grp[0], self.controllerBind02.parentControl[0])
        # au.connectAttrTransRot(self.jointBind04Grp[0], self.controllerBind04.parentControl[0])

        # flipping controller
        if controllerLidDown:
            if self.pos > 0:
                mc.setAttr(self.controllerBind01.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind02.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind04.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind05.parentControl[0] + '.scaleX', 1)

                # connect translate controller to joint
                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt05)
            else:
                mc.setAttr(self.controllerBind01.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind02.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind04.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind05.parentControl[0] + '.scaleX', -1)
                # connect translate controller to joint
                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=-1, input2Y=-1, input2Z=1,
                                          jointBindTarget=self.jnt05)

            mc.setAttr(self.controllerBind01.parentControl[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind02.parentControl[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind05.parentControl[0] + '.scaleY', -1)
            mc.setAttr(self.controllerBind04.parentControl[0] + '.scaleY', -1)

            mc.setAttr(self.controllerBind03.parentControl[0] + '.scaleY', -1)

            au.connectAttrRot(self.controllerBind01.control, self.jnt01)

            au.connectAttrRot(self.controllerBind02.control, self.jnt02)

            # mid translate and rotate
            self.bindTranslateReverse(control=self.controllerBind03.control,
                                      input2X=1, input2Y=-1, input2Z=1,
                                      jointBindTarget=self.jnt03)

            au.connectAttrRot(self.controllerBind03.control, self.jnt03)

            au.connectAttrRot(self.controllerBind04.control, self.jnt04)

            au.connectAttrRot(self.controllerBind05.control, self.jnt05)

        else:
            if self.pos > 0:
                mc.setAttr(self.controllerBind01.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind02.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind04.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind05.parentControl[0] + '.scaleX', 1)

                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt01)
                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt02)
                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt05)

            else:
                mc.setAttr(self.controllerBind01.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind02.parentControl[0] + '.scaleX', 1)
                mc.setAttr(self.controllerBind04.parentControl[0] + '.scaleX', -1)
                mc.setAttr(self.controllerBind05.parentControl[0] + '.scaleX', -1)

                # right side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind01.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt01)

                # right side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind02.control,
                                          input2X=1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt02)

                # left side 02 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind04.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt04)

                # left side 01 translate and rotate
                self.bindTranslateReverse(control=self.controllerBind05.control,
                                          input2X=-1, input2Y=1, input2Z=1,
                                          jointBindTarget=self.jnt05)


            au.connectAttrRot(self.controllerBind02.control, self.jnt02)

            au.connectAttrRot(self.controllerBind01.control, self.jnt01)

            # left side 02 translate and rotate
            au.connectAttrRot(self.controllerBind04.control, self.jnt04)

            # left side 01 translate and rotate
            au.connectAttrRot(self.controllerBind05.control, self.jnt05)

            # mid translate and rotate
            au.connectAttrTransRot(self.controllerBind03.control, self.jnt03)

    def bindTranslateReverse(self, control, input2X, input2Y, input2Z, jointBindTarget):
        mdnReverse = mc.createNode('multiplyDivide', n=au.prefixName(control) + '_mdn')
        mc.connectAttr(control + '.translate', mdnReverse + '.input1')

        mc.setAttr(mdnReverse + '.input2X', input2X)
        mc.setAttr(mdnReverse + '.input2Y', input2Y)
        mc.setAttr(mdnReverse + '.input2Z', input2Z)

        # connect to object
        mc.connectAttr(mdnReverse+'.output', jointBindTarget+'.translate')

    def wireBindCurve(self, crv, directionLip01, directionLip02,
                      scale, eyeballJnt, side):

        jointPosBind = len(self.allJoint)

        # query position of bind joint
        joint01 =  self.allJoint[(jointPosBind * 0)]

        joint02 =  self.allJoint[(jointPosBind / 4)]

        transform = None
        if not len(self.allJoint) % 2 == 0:
            joint03 = self.allJoint[(jointPosBind / 2)]

        else:
            tempJnt03 = self.allJoint[(jointPosBind / 2)]
            tempsjoint03 = self.allJoint[(jointPosBind / 2)-1]
            transform = mc.createNode('transform', n='guide')
            joint03 = mc.delete(mc.parentConstraint(tempJnt03, tempsjoint03, transform))

        joint04 =  self.allJoint[(jointPosBind / 2) + (jointPosBind / 4)]
        joint05 =  self.allJoint[-1]

        # query the position right side
        self.xformJnt01 = mc.xform(joint01, ws=1, q=1, t=1)
        self.xformJnt02 = mc.xform(joint02, ws=1, q=1, t=1)
        self.xformJnt03 = mc.xform(joint03, ws=1, q=1, t=1)
        self.xformJnt04 = mc.xform(joint04, ws=1, q=1, t=1)
        self.xformJnt05 = mc.xform(joint05, ws=1, q=1, t=1)
        mc.delete(transform)

        mc.select(cl=1)
        jnt01  = mc.joint(n=self.prefixNameCrv + '01' + '_bind', p=self.xformJnt01, rad=0.5 * scale)
        jnt02  = mc.duplicate(jnt01, n=self.prefixNameCrv + '02' + '_bind')[0]
        jnt03  = mc.duplicate(jnt01, n=self.prefixNameCrv + '03' +  '_bind')[0]
        jnt04  = mc.duplicate(jnt01, n=self.prefixNameCrv + '04' +  '_bind')[0]
        jnt05  = mc.duplicate(jnt01, n=self.prefixNameCrv + '05' +  '_bind')[0]

        # set the position RGT joint
        mc.xform(jnt02, ws=1, t=self.xformJnt02)
        mc.xform(jnt03, ws=1, t=self.xformJnt03)
        mc.xform(jnt04, ws=1, t=self.xformJnt04)
        mc.xform(jnt05, ws=1, t=self.xformJnt05)


        # create bind curve
        deformCrv = mc.duplicate(crv)[0]
            # mc.curve(ep=[(self.xformJnt01), (self.xformJnt02), (self.xformJnt03),
            #                      (self.xformJnt04), (self.xformJnt05)], degree=3)

        deformCrv = mc.rename(deformCrv, (self.prefixNameCrv + 'Bind' + '_crv'))

        # parent the bind joint
        self.jointBind03Grp = au.createParentTransform(listparent=['Zro', 'Offset', 'All'], object=jnt03,
                                                       matchPos=jnt03, prefix=self.prefixNameCrv+ '03',
                                                       suffix='_bind', side=side)

        self.jointBind01Grp = au.createParentTransform(listparent=['Zro', 'Offset'], object=jnt01,
                                                       matchPos=jnt01, prefix=self.prefixNameCrv + '01',
                                                       suffix='_bind', side=side)

        self.jointBind02Grp = au.createParentTransform(listparent=['Zro', 'Offset'], object=jnt02,
                                                       matchPos=jnt02, prefix=self.prefixNameCrv + '02',
                                                       suffix='_bind', side=side)

        self.jointBind05Grp = au.createParentTransform(listparent=['Zro', 'Offset'], object=jnt05,
                                                       matchPos=jnt05, prefix=self.prefixNameCrv + '05',
                                                       suffix='_bind', side=side)

        self.jointBind04Grp = au.createParentTransform(listparent=['Zro', 'Offset'], object=jnt04,
                                                       matchPos=jnt04, prefix=self.prefixNameCrv + '04',
                                                       suffix='_bind', side=side)

        # assign bind grp jnt
        self.jointBind03GrpAll = self.jointBind03Grp[2]
        self.jointBind03GrpOffset = self.jointBind03Grp[1]

        # eyeball grp connect
        self.eyeballOffsetBind01 = self.eyeballGrpBind(crv=crv, bindZroGrp=self.jointBind01Grp[0],
                                                       number='01', side=side, eyeballJnt=eyeballJnt)

        self.eyeballOffsetBind03 = self.eyeballGrpBind(crv=crv, bindZroGrp=self.jointBind03Grp[0],
                                                       number='03', side=side, eyeballJnt=eyeballJnt)

        self.eyeballOffsetBind05 = self.eyeballGrpBind(crv=crv, bindZroGrp=self.jointBind05Grp[0],
                                                       number='05', side=side, eyeballJnt=eyeballJnt)

        if self.pos > 0:
            mc.setAttr(self.jointBind01Grp[0] + '.rotateY', directionLip01 * -1)
            mc.setAttr(self.jointBind02Grp[0] + '.rotateY', directionLip02 * -1)
            mc.setAttr(self.jointBind05Grp[0] + '.rotateY', directionLip01)
            mc.setAttr(self.jointBind04Grp[0] + '.rotateY', directionLip02)

        else:
            mc.setAttr(self.jointBind01Grp[0] + '.rotateY', directionLip01)
            mc.setAttr(self.jointBind02Grp[0] + '.rotateY', directionLip02)
            mc.setAttr(self.jointBind05Grp[0] + '.rotateY', directionLip01*-1)
            mc.setAttr(self.jointBind04Grp[0] + '.rotateY', directionLip02*-1)

        # rebuild the curve
        mc.rebuildCurve(deformCrv, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0,
                        kep=1, kt=0, s=8, d=3, tol=0.01)

        # skinning the joint to the bind curve
        skinCls = mc.skinCluster([jnt05, jnt04, jnt01, jnt02, jnt03], deformCrv,
                                 n='%s%s%s'% ('wire', self.prefixNameCrv.capitalize(), 'SkinCluster'), tsb=True, bm=0, sm=0, nw=1, mi=3)

        # Distribute the skin
        skinPercent0 = '%s.cv[0]' % deformCrv
        skinPercent1 = '%s.cv[1]' % deformCrv
        skinPercent2 = '%s.cv[2]' % deformCrv
        skinPercent3 = '%s.cv[3]' % deformCrv
        skinPercent4 = '%s.cv[4]' % deformCrv
        skinPercent5 = '%s.cv[5]' % deformCrv
        skinPercent6 = '%s.cv[6]' % deformCrv
        skinPercent7 = '%s.cv[7]' % deformCrv
        skinPercent8 = '%s.cv[8]' % deformCrv
        skinPercent9 = '%s.cv[9]' % deformCrv
        skinPercent10 = '%s.cv[10]' % deformCrv

        mc.skinPercent(skinCls[0], skinPercent0, tv=[(jnt01, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent1, tv=[(jnt01, 0.9), (jnt02, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent2, tv=[(jnt01, 0.7), (jnt02, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent3, tv=[(jnt02, 0.5), (jnt01, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent4, tv=[(jnt02, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent5, tv=[(jnt03, 1.0)])
        mc.skinPercent(skinCls[0], skinPercent6, tv=[(jnt04, 0.3), (jnt03, 0.7)])
        mc.skinPercent(skinCls[0], skinPercent7, tv=[(jnt04, 0.5), (jnt05, 0.25), (jnt03, 0.25)])
        mc.skinPercent(skinCls[0], skinPercent8, tv=[(jnt05, 0.7), (jnt04, 0.3)])
        mc.skinPercent(skinCls[0], skinPercent9, tv=[(jnt05, 0.9), (jnt04, 0.1)])
        mc.skinPercent(skinCls[0], skinPercent10, tv=[(jnt05, 1.0)])

        # wire the curve
        wireDef = mc.wire(crv, dds=(0, 100 * scale), wire=deformCrv)
        wireDef[0] = mc.rename(wireDef[0], (self.prefixNameCrv + '_wireNode'))

        # constraint mid to 02 left and right
        mc.parentConstraint(jnt03, jnt05, self.jointBind04Grp[0], mo=1)
        mc.parentConstraint(jnt03, jnt01, self.jointBind02Grp[0], mo=1)

        self.jnt03 = jnt03
        self.jnt01 = jnt01
        self.jnt02 = jnt02
        self.jnt05 = jnt05
        self.jnt04 = jnt04

        # create grp curves
        self.curvesGrp = mc.createNode('transform', n=self.prefixNameCrv + 'Crv' + '_grp')
        mc.setAttr (self.curvesGrp + '.it', 0, l=1)
        mc.parent(deformCrv, mc.listConnections(wireDef[0] + '.baseWire[0]')[0], self.curvesGrp)
        mc.hide(self.curvesGrp)

        # create grp bind
        self.bindJntGrp = mc.createNode('transform', n=self.prefixNameCrv + 'JntBind' + '_grp')
        mc.parent(self.eyeballOffsetBind03[0], self.eyeballOffsetBind01[0], self.jointBind02Grp[0],
                  self.eyeballOffsetBind05[0], self.jointBind04Grp[0], self.bindJntGrp)
        mc.hide(self.bindJntGrp)

        self.deformCrv = deformCrv

    def eyeballGrpBind(self, crv, number, side, bindZroGrp, eyeballJnt):
        # bind grp for eyeball
        eyeballZro = mc.group(em=1, n=au.prefixName(crv)+'EyeballZro' + number + side+'_grp')
        eyeballOffset = mc.group(em=1, n=au.prefixName(crv)+'EyeballOffset' + number + side +'_grp', p=eyeballZro)
        mc.delete(mc.parentConstraint(eyeballJnt, eyeballZro))

        mc.parent(bindZroGrp, eyeballOffset)

        return eyeballZro, eyeballOffset

    def createJointLid(self, crv, worldUpObject, eyeballJnt, scale):
        self.allJointCenter =[]
        self.allJoint =[]
        self.allLocator=[]

        for i, v in enumerate(self.vtxCrv):
            # create joint
            mc.select(cl=1)
            self.joint = mc.joint(n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_jnt'), rad=0.1 * scale)
            pos = mc.xform(v, q=1, ws=1, t=1)
            mc.xform(self.joint, ws=1, t=pos)
            self.allJoint.append(self.joint)

            mc.select(cl=1)
            self.jointCenter = mc.joint(n='%s%02d%s%s' % (self.prefixNameCrv, (i + 1),'Ctr', '_jnt'), rad=0.1 * scale)
            posC = mc.xform(eyeballJnt, q=1, ws=1, t=1)
            mc.xform(self.jointCenter, ws=1, t=posC)
            mc.parent(self.joint, self.jointCenter)

            # change direction of joint center
            mc.joint(self.jointCenter, e=1, oj="xyz", secondaryAxisOrient="yup", ch=1, zso=1)
            self.allJointCenter.append(self.jointCenter)

            # create locator
            self.locator = mc.spaceLocator(n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_loc'))[0]

            mc.xform(self.locator, ws=1, t=pos)

            # aim constraint of joint
            mc.aimConstraint(self.locator, self.jointCenter, mo=1, weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0),
                               worldUpType="object", worldUpObject=worldUpObject)

            self.allLocator.append(self.locator)

            # connect curve to locator grp
            curveRelatives = mc.listRelatives(crv, s=True)[0]
            u = self.getUParam(pos, curveRelatives)
            pci = mc.createNode("pointOnCurveInfo", n='%s%02d%s' % (self.prefixNameCrv, (i + 1), '_pci'))
            mc.connectAttr(curveRelatives + '.worldSpace', pci + '.inputCurve')
            mc.setAttr(pci + '.parameter', u)
            mc.connectAttr(pci + '.position', self.locator + '.t')


        # grouping joint
        self.jointGrp = mc.group(em=1, n=self.prefixNameCrv + 'Jnt' + '_grp')
        mc.parent(self.allJointCenter, worldUpObject, self.jointGrp)
        mc.hide(self.jointGrp)

        # grouping locator
        self.locatorGrp = mc.group(em=1, n=self.prefixNameCrv+'Loc'+'_grp')
        mc.setAttr (self.locatorGrp + '.it', 0, l=1)
        mc.parent(self.allLocator, self.locatorGrp)
        mc.hide(self.locatorGrp)

    def getUParam(self, pnt=[], crv=None):
        point = om.MPoint(pnt[0], pnt[1], pnt[2])
        curveFn = om.MFnNurbsCurve(self.getDagPath(crv))
        paramUtill = om.MScriptUtil()
        paramPtr = paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve == True:

            curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)
        else:
            point = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kObject)
            curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)

        param = paramUtill.getDouble(paramPtr)
        return param

    def getDagPath(self, objectName):
        if isinstance(objectName, list) == True:
            oNodeList = []
            for o in objectName:
                selectionList = om.MSelectionList()
                selectionList.add(o)
                oNode = om.MDagPath()
                selectionList.getDagPath(0, oNode)
                oNodeList.append(oNode)
            return oNodeList
        else:
            selectionList = om.MSelectionList()
            selectionList.add(objectName)
            oNode = om.MDagPath()
            selectionList.getDagPath(0, oNode)
            return oNode