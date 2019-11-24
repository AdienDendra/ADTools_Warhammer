import maya.cmds as mc
import ADCtrl as ac, ADUtils as au

reload(ac)

class Build:
    def __init__(self,
                 neckJnt,
                 headJnt,
                 headUpJnt,
                 headLowJnt,
                 jawJnt,
                 noseJnt,
                 objectFolMesh,
                 noseTipJnt,
                 chinJnt,
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
                                   ctrlColor='yellow', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])
        self.neckCtrl = neckCtrl.control
        self.neckCtrlGrp = neckCtrl.parentControl[0]

        headCtrl = ac.Control(matchPos=headJnt,
                                   prefix=headJnt,
                                   shape=ac.CUBE, groupsCtrl=[''],
                                   ctrlSize=scale * 10.0,
                                   ctrlColor='blue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        self.headCtrl = headCtrl.control
        self.headCtrlGrp = headCtrl.parentControl[0]

        headUpCtrl = ac.Control(matchPos=headUpJnt,
                                     prefix=headUpJnt,
                                     shape=ac.CIRCLEHALF, groupsCtrl=[''],
                                     ctrlSize=scale * 10.0,
                                     ctrlColor='red', lockChannels=['v'],
                                     connect=['parentCons', 'scaleCons'])

        self.headUpCtrl = headUpCtrl.control
        self.headUpCtrlGrp = headUpCtrl.parentControl[0]

        headLowCtrl = ac.Control(matchPos=headLowJnt,
                                      prefix=headLowJnt,
                                      shape=ac.CIRCLEHALF, groupsCtrl=[''],
                                      ctrlSize=scale * 10.0,
                                      ctrlColor='red', lockChannels=['v'],
                                      connect=['parentCons', 'scaleCons'])

        self.headLowCtrl = headLowCtrl.control
        self.headLowCtrlGrp = headLowCtrl.parentControl[0]

        jawCtrl = ac.Control(matchPos=jawJnt,
                                  prefix=jawJnt,
                                  shape=ac.SQUAREPLUS, groupsCtrl=[''],
                                  ctrlSize=scale * 10.0,
                                  ctrlColor='yellow', lockChannels=['v','s'],
                                  connect=['parentCons', 'scaleCons'])

        self.jawCtrl = jawCtrl.control
        self.jawCtrlGrp = jawCtrl.parentControl[0]

        noseTipCtrl = ac.Control(matchPos=noseTipJnt,
                                      prefix=noseTipJnt,
                                      shape=ac.JOINT, groupsCtrl=['','Offset'],
                                      ctrlSize=scale * 1.0,
                                      ctrlColor='yellow', lockChannels=['v'])

        self.noseTipCtrl = noseTipCtrl.control
        self.noseTipCtrlGrp = noseTipCtrl.parentControl[0]
        self.noseTipCtrlOffset = noseTipCtrl.parentControl[1]

        noseTipGrp = au.createParentTransform(listparent=[''], object=noseTipJnt, matchPos=noseTipJnt, prefix='noseTip', suffix='_jnt')

        au.connectAttrObject(self.noseTipCtrl, noseTipJnt)

        # noseCtrl = ac.Control(matchPos=noseJnt,
        #                            prefix=noseJnt,
        #                            shape=ac.LOCATOR, groupsCtrl=[''],
        #                            ctrlSize=scale * 3.0,
        #                            ctrlColor='blue', lockChannels=['v'])
        #
        # self.noseCtrl = noseCtrl.control
        # self.noseCtrlGrp = noseCtrl.parentControl[0]
        # tz = mc.getAttr(self.noseCtrlGrp+'.translateZ')
        # mc.setAttr(self.noseCtrlGrp+'.translateZ', tz+8)

        # # connect nose ctrl to nostip grp ctrl
        # au.connectAttrObject(self.noseCtrl, self.noseTipCtrlOffset)

        chinCtrl = ac.Control(matchPos=chinJnt,
                                   prefix=chinJnt,
                                   shape=ac.JOINT, groupsCtrl=[''],
                                   ctrlSize=scale * 1.0,
                                   ctrlColor='yellow', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

        self.chinCtrl = chinCtrl.control
        self.chinCtrlGrp = chinCtrl.parentControl[0]

        # group to follicle
        object = [self.noseTipCtrlGrp]

        self.follicleTransformAll=[]
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            self.follicleTransformAll.append(follicleTransform)


        # ==============================================================================================================
        #                                       CREATE AIM FOR EYEBALL
        # ==============================================================================================================

        eyeballAimMainCtrl = ac.Control(matchPos=eyeballJntLFT,
                                        matchPosTwo=eyeballJntRGT,
                                             prefix=prefixEyeballAim,
                                             shape=ac.LOCATOR, groupsCtrl=['Zro', 'Offset'],
                                             ctrlSize=scale * 0.4,
                                             ctrlColor='blue', lockChannels=['v', 'r', 's'])

        self.eyeballAimMainCtrl = eyeballAimMainCtrl.control

        getAttribute = mc.getAttr(eyeballAimMainCtrl.parentControl[0]+'.translateZ')
        mc.setAttr(eyeballAimMainCtrl.parentControl[0]+'.translateZ', getAttribute+(positionEyeAimCtrl*scale))


        # PARENTING GRP
        mc.parent(self.chinCtrlGrp, self.jawCtrl)
        mc.parent(self.jawCtrlGrp, self.headLowCtrl)

        mc.parent(self.headLowCtrlGrp, self.headUpCtrlGrp, self.headCtrl)
        mc.parent(self.headCtrlGrp, self.neckCtrl)
