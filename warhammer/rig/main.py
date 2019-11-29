import maya.cmds as mc
import ADCtrl as ac, ADUtils as au

reload(ac)

class Build:
    def __init__(self,
                 ctrlGrp,
                 neckJnt,
                 headJnt,
                 headUpJnt,
                 headLowJnt,
                 jawJnt,
                 noseJnt,
                 upperTeethJnt,
                 lowerTeethJnt,
                 tongue01Jnt,
                 tongue02Jnt,
                 tongue03Jnt,
                 tongue04Jnt,
                 objectFolMesh,
                 noseTipJnt,
                 chinJnt,
                 throatJnt,
                 scale,
                 eyeballJntLFT,
                 eyeballJntRGT,
                 prefixEyeballAim,
                 positionEyeAimCtrl,
                 ):


        # CREATE CONTROLLER
        neckCtrl = ac.Control(matchPos=neckJnt,
                                   prefix=neckJnt,
                                   shape=ac.CIRCLEPLUS, groupsCtrl=[''],
                                   ctrlSize=scale * 15.0,
                                   gimbal=True,
                                   ctrlColor='yellow', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        headCtrl = ac.Control(matchPos=headJnt,
                                   prefix=headJnt,
                                   shape=ac.CUBE, groupsCtrl=['','Global', "Local"],
                                   ctrlSize=scale * 10.0,
                                   gimbal=True,
                                   ctrlColor='blue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])
        # ADD ATTRIBUTE


        headUpCtrl = ac.Control(matchPos=headUpJnt,
                                     prefix=headUpJnt,
                                     shape=ac.CIRCLEHALF, groupsCtrl=[''],
                                     ctrlSize=scale * 10.0,
                                     ctrlColor='red', lockChannels=['v'],
                                     connect=['parentCons', 'scaleCons'])

        headLowCtrl = ac.Control(matchPos=headLowJnt,
                                      prefix=headLowJnt,
                                      shape=ac.CIRCLEHALF, groupsCtrl=[''],
                                      ctrlSize=scale * 10.0,
                                      ctrlColor='red', lockChannels=['v'],
                                      connect=['parentCons', 'scaleCons'])

        jawCtrl = ac.Control(matchPos=jawJnt,
                                  prefix=jawJnt,
                                  shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                  ctrlSize=scale * 10.0,
                                  ctrlColor='yellow', lockChannels=['v','s'],
                                  connect=['parentCons', 'scaleCons'])

        noseTipCtrl = ac.Control(matchPos=noseTipJnt,
                                      prefix=noseTipJnt,
                                      shape=ac.JOINT, groupsCtrl=['','Offset'],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='yellow', lockChannels=['v'])

        chinCtrl = ac.Control(matchPos=chinJnt,
                                   prefix=chinJnt,
                                   shape=ac.JOINT, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='yellow', lockChannels=['v'])

        throatCtrl = ac.Control(matchPos=throatJnt,
                                   prefix=throatJnt,
                                   shape=ac.JOINT, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='yellow', lockChannels=['v'])

        upperTeeth = ac.Control(matchPos=upperTeethJnt,
                                   prefix=upperTeethJnt,
                                   shape=ac.CUBE, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='blue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        lowerTeeth = ac.Control(matchPos=lowerTeethJnt,
                                   prefix=lowerTeethJnt,
                                   shape=ac.CUBE, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='blue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        tongue01 = ac.Control(matchPos=tongue01Jnt,
                                   prefix=tongue01Jnt,
                                   shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='turquoiseBlue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        tongue02 = ac.Control(matchPos=tongue02Jnt,
                                   prefix=tongue02Jnt,
                                   shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='turquoiseBlue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        tongue03 = ac.Control(matchPos=tongue03Jnt,
                                   prefix=tongue03Jnt,
                                   shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='turquoiseBlue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        tongue04 = ac.Control(matchPos=tongue04Jnt,
                                   prefix=tongue04Jnt,
                                   shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='turquoiseBlue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])


    # ==================================================================================================================
    #                                            ASSIGNING THE INSTANCE NAME
    # ==================================================================================================================
        self.neckCtrl = neckCtrl.control
        self.neckCtrlGimbal = neckCtrl.controlGimbal
        self.neckCtrlGrp = neckCtrl.parentControl[0]

        self.headCtrl = headCtrl.control
        self.headCtrlGimbal = headCtrl.controlGimbal
        self.headCtrlGrp = headCtrl.parentControl[0]
        self.headCtrlGlobal = headCtrl.parentControl[1]
        self.headCtrlLocal = headCtrl.parentControl[2]

        self.headUpCtrl = headUpCtrl.control
        self.headUpCtrlGrp = headUpCtrl.parentControl[0]

        self.headLowCtrl = headLowCtrl.control
        self.headLowCtrlGrp = headLowCtrl.parentControl[0]

        self.jawCtrl = jawCtrl.control
        self.jawCtrlGrp = jawCtrl.parentControl[0]

        self.noseTipCtrl = noseTipCtrl.control
        self.noseTipCtrlGrp = noseTipCtrl.parentControl[0]
        self.noseTipCtrlOffset = noseTipCtrl.parentControl[1]

        self.chinCtrl = chinCtrl.control
        self.chinCtrlGrp = chinCtrl.parentControl[0]

        self.throatCtrl = throatCtrl.control
        self.throatCtrlGrp = throatCtrl.parentControl[0]

        self.upperTeethCtrl = upperTeeth.control
        self.upperTeethCtrlGrp = upperTeeth.parentControl[0]

        self.lowerTeethCtrl = lowerTeeth.control
        self.lowerTeethCtrlGrp = lowerTeeth.parentControl[0]

        self.tongue01Ctrl = tongue01.control
        self.tongue01CtrlGrp = tongue01.parentControl[0]

        self.tongue02Ctrl = tongue02.control
        self.tongue02CtrlGrp = tongue02.parentControl[0]

        self.tongue03Ctrl = tongue03.control
        self.tongue03CtrlGrp = tongue03.parentControl[0]

        self.tongue04Ctrl = tongue04.control
        self.tongue04CtrlGrp = tongue04.parentControl[0]


    # LOCAL WORLD HEAD
        self.localWorld(objectName='head', objectCtrl=self.headCtrl,
                        objectParentGrp=self.headCtrlGrp, objectParentGlobal=self.headCtrlGlobal,
                        objectParentLocal=self.headCtrlLocal,
                        localBase=self.neckCtrlGimbal, worldBase=ctrlGrp, eyeAim=False)

    # CREATE GROUP CORESPONDENT THE JOINTS
        au.createParentTransform(listparent=[''], object=noseTipJnt, matchPos=noseTipJnt, prefix='noseTip', suffix='_jnt')
        au.createParentTransform(listparent=[''], object=chinJnt, matchPos=chinJnt, prefix='chin', suffix='_jnt')
        au.createParentTransform(listparent=[''], object=throatJnt, matchPos=throatJnt, prefix='throat', suffix='_jnt')

        au.connectAttrObject(self.noseTipCtrl, noseTipJnt)
        au.connectAttrObject(self.chinCtrl, chinJnt)
        au.connectAttrObject(self.throatCtrl, throatJnt)


    # SCALE CONSTRAINT
        mc.scaleConstraint(self.headCtrl, noseJnt)


    # ==================================================================================================================
    #                                CONTROLLER CORRESPONDING TO FOLLICLE
    # ==================================================================================================================

        # group to follicle
        object = [self.noseTipCtrlGrp, self.chinCtrlGrp, self.throatCtrlGrp]

        self.follicleTransformAll=[]
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            self.follicleTransformAll.append(follicleTransform)

        mc.scaleConstraint(self.headCtrl, self.follicleTransformAll[0])
        mc.scaleConstraint(self.jawCtrl, self.follicleTransformAll[1])
        mc.scaleConstraint(self.jawCtrl, self.follicleTransformAll[2])


    # ==================================================================================================================
    #                                       CREATE AIM FOR EYEBALL
    # ==================================================================================================================

        eyeballAimMainCtrl = ac.Control(matchPos=eyeballJntLFT,
                                        matchPosTwo=eyeballJntRGT,
                                             prefix=prefixEyeballAim,
                                             shape=ac.LOCATOR, groupsCtrl=['', 'Global', 'Local'],
                                             ctrlSize=scale * 0.4,
                                             ctrlColor='blue', lockChannels=['v', 'r', 's'])

        self.eyeballAimMainCtrl = eyeballAimMainCtrl.control
        self.eyeballAimMainCtrlGrp = eyeballAimMainCtrl.parentControl[0]
        self.eyeballAimMainCtrlGlobal = eyeballAimMainCtrl.parentControl[1]
        self.eyeballAimMainCtrlLocal= eyeballAimMainCtrl.parentControl[2]

        getAttribute = mc.getAttr(eyeballAimMainCtrl.parentControl[0]+'.translateZ')
        mc.setAttr(eyeballAimMainCtrl.parentControl[0]+'.translateZ', getAttribute+(positionEyeAimCtrl*scale))

        # LOCAL WORLD AIM EYEBALL
        self.localWorld(objectName='eyeballAim', objectCtrl=self.eyeballAimMainCtrl,
                        objectParentGrp=self.eyeballAimMainCtrlGrp,
                        objectParentGlobal=self.eyeballAimMainCtrlGlobal,
                        objectParentLocal=self.eyeballAimMainCtrlLocal,
                        localBase=self.headUpCtrl, worldBase=ctrlGrp, eyeAim=True)

    # PARENT TONGUE HIERARCHY
        mc.parent(self.tongue04CtrlGrp, self.tongue03Ctrl )
        mc.parent(self.tongue03CtrlGrp, self.tongue02Ctrl )
        mc.parent(self.tongue02CtrlGrp, self.tongue01Ctrl )
        mc.parent(self.tongue01CtrlGrp, self.lowerTeethCtrlGrp, self.jawCtrl )
        mc.parent(self.upperTeethCtrlGrp, self.headLowCtrl)

    # PARENTING GRP
        mc.parent(self.jawCtrlGrp, self.headLowCtrl)
        mc.parent(self.eyeballAimMainCtrlGrp, self.headUpCtrl)
        mc.parent(self.headLowCtrlGrp, self.headUpCtrlGrp, self.headCtrlGimbal)
        mc.parent(self.headCtrlGrp, self.neckCtrlGimbal)



    def localWorld(self,objectName, objectCtrl, objectParentGrp,
                   objectParentGlobal, objectParentLocal, localBase, worldBase, eyeAim=False):
        # LOCAL WORLD HEAD
        local = mc.createNode('transform', n=objectName + 'Local_grp')
        mc.parent(local, objectParentGrp)
        mc.setAttr(local + '.translate', 0, 0, 0, type="double3")
        mc.setAttr(local + '.rotate', 0, 0, 0, type="double3")

        world = mc.duplicate(local, n=objectName + 'World_grp')[0]

        mc.parentConstraint(localBase, local, mo=1)
        mc.parentConstraint(worldBase, world, mo=1)

        if not eyeAim:
            mc.parentConstraint(local, objectParentGlobal, mo=1)
            localWorldCons = mc.orientConstraint(local, world, objectParentLocal, mo=1)[0]
        else:
            localWorldCons = mc.parentConstraint(local, world, objectParentLocal, mo=1)[0]

        # CONNECT THE ATTRIBUTE
        headLocalWrld = au.addAttribute(objects=[objectCtrl], longName=['localWorld'],
                                             attributeType="float", min=0, max=1, dv=0, k=True)

        # CREATE REVERSE
        reverse = mc.createNode('reverse', n=objectName + 'LocalWorld_rev')
        mc.connectAttr(objectCtrl + '.%s' % headLocalWrld, reverse + '.inputX')

        mc.connectAttr(reverse + '.outputX', localWorldCons + '.%sW0' % local)
        mc.connectAttr(objectCtrl + '.%s' % headLocalWrld, localWorldCons + '.%sW1' % world)

