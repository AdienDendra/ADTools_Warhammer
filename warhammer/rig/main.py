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

        headCtrl = ac.Control(matchPos=headJnt,
                                   prefix=headJnt,
                                   shape=ac.CUBE, groupsCtrl=[''],
                                   ctrlSize=scale * 10.0,
                                   ctrlColor='blue', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])

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
                                   ctrlColor='yellow', lockChannels=['v'],
                                   connect=['parentCons', 'scaleCons'])




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



    # ==================================================================================================================
    #                                            ASSIGNING THE INSTANCE NAME
    # ==================================================================================================================
        self.neckCtrl = neckCtrl.control
        self.neckCtrlGrp = neckCtrl.parentControl[0]

        self.headCtrl = headCtrl.control
        self.headCtrlGrp = headCtrl.parentControl[0]

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

    # CREATE GROUP CORESPONDENT THE JOINTS
        au.createParentTransform(listparent=[''], object=noseTipJnt, matchPos=noseTipJnt, prefix='noseTip', suffix='_jnt')
        au.connectAttrObject(self.noseTipCtrl, noseTipJnt)

    # ==================================================================================================================
    #                                CONTROLLER CORRESPONDING TO FOLLICLE
    # ==================================================================================================================

        # group to follicle
        object = [self.noseTipCtrlGrp, self.chinCtrlGrp]

        self.follicleTransformAll=[]
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            self.follicleTransformAll.append(follicleTransform)


    # ==================================================================================================================
    #                                       CREATE AIM FOR EYEBALL
    # ==================================================================================================================

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
        mc.parent(self.jawCtrlGrp, self.headLowCtrl)
        mc.parent(self.headLowCtrlGrp, self.headUpCtrlGrp, self.headCtrl)
        mc.parent(self.headCtrlGrp, self.neckCtrl)
