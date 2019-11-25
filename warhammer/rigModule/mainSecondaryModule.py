import maya.cmds as mc
import ADUtils as au
from warhammer.rig import main as mn, secondary as sc

reload(mn)
reload(sc)
reload(au)


class MainFace:
    def __init__(self,
                 ctrlGrp,
                 neckJnt,
                 headJnt,
                 headUpJnt,
                 headLowJnt,
                 jawJnt,
                 upperTeethJnt,
                 lowerTeethJnt,
                 tongue01Jnt,
                 tongue02Jnt,
                 tongue03Jnt,
                 tongue04Jnt,
                 earLFTJnt,
                 earRGTJnt,
                 noseTipJnt,
                 chinJnt,
                 scale,
                 nostrilLFTJnt,
                 cheekUpLFTJnt,
                 cheekDownLFTJnt,
                 eyebrowInLFTJnt,
                 eyebrowMidLFTJnt,
                 eyebrowOutLFTJnt,
                 browInLFTJnt,
                 browMidLFTJnt,
                 browOutLFTJnt,
                 eyelidPinchLFTJnt,
                 nostrilRGTJnt,
                 cheekUpRGTJnt,
                 cheekDownRGTJnt,
                 eyebrowInRGTJnt,
                 eyebrowMidRGTJnt,
                 eyebrowOutRGTJnt,
                 browInRGTJnt,
                 browMidRGTJnt,
                 browOutRGTJnt,
                 eyelidPinchRGTJnt,
                 sideLFT,
                 sideRGT,
                 eyeballJntLFT,
                 eyeballJntRGT,
                 prefixEyeballAim,
                 positionEyeAimCtrl,
                 objectFolMesh,
                 ):

        # BUILD CONTROLLER
        ctrlFaceGroup = mc.group(em=1, n='faceCtrl_grp')


        main = mn.Build(ctrlGrp=ctrlGrp,
                        objectFolMesh=objectFolMesh,
                        neckJnt=neckJnt,
                         headJnt=headJnt,
                         headUpJnt=headUpJnt,
                         headLowJnt=headLowJnt,
                         jawJnt=jawJnt,
                        upperTeethJnt=upperTeethJnt,
                        lowerTeethJnt=lowerTeethJnt,
                        tongue01Jnt=tongue01Jnt,
                        tongue02Jnt=tongue02Jnt,
                        tongue03Jnt=tongue03Jnt,
                        tongue04Jnt=tongue04Jnt,
                         noseTipJnt=noseTipJnt,
                         chinJnt=chinJnt,
                         scale=scale,
                         eyeballJntLFT=eyeballJntLFT,
                         eyeballJntRGT=eyeballJntRGT,
                         prefixEyeballAim=prefixEyeballAim,
                         positionEyeAimCtrl=positionEyeAimCtrl,
                        )


        secLFT = sc.Build(objectFolMesh=objectFolMesh,
                          nostrilJnt=nostrilLFTJnt,
                          earJnt=earLFTJnt,
                                cheekUpJnt=cheekUpLFTJnt,
                                cheekDownJnt=cheekDownLFTJnt,
                                eyebrowInJnt=eyebrowInLFTJnt,
                                eyebrowMidJnt=eyebrowMidLFTJnt,
                                eyebrowOutJnt=eyebrowOutLFTJnt,
                                browInJnt=browInLFTJnt,
                                browMidJnt=browMidLFTJnt,
                                browOutJnt=browOutLFTJnt,
                                eyelidPinchJnt=eyelidPinchLFTJnt,
                                scale=scale,
                                side=sideLFT)

        secRGT = sc.Build(objectFolMesh=objectFolMesh,
                          nostrilJnt=nostrilRGTJnt,
                          earJnt=earRGTJnt,
                          cheekUpJnt=cheekUpRGTJnt,
                                cheekDownJnt=cheekDownRGTJnt,
                                eyebrowInJnt=eyebrowInRGTJnt,
                                eyebrowMidJnt=eyebrowMidRGTJnt,
                                eyebrowOutJnt=eyebrowOutRGTJnt,
                                browInJnt=browInRGTJnt,
                                browMidJnt=browMidRGTJnt,
                                browOutJnt=browOutRGTJnt,
                                eyelidPinchJnt=eyelidPinchRGTJnt,
                                scale=scale,
                                side=sideRGT)

        self.headUpCtrlGrpParent = main.headUpCtrlGrp

        # constraint
        mc.parentConstraint(headLowJnt, jawJnt, secLFT.cheekDownJntGrp, mo=1)
        mc.parentConstraint(headLowJnt, jawJnt, secRGT.cheekDownJntGrp, mo=1)

        mc.parent(secLFT.eyebrowCtrlGrp, secRGT.eyebrowCtrlGrp, main.headUpCtrl)
        mc.parent(secLFT.earCtrlGrp, secRGT.earCtrlGrp, main.headCtrl)
        mc.parent(secLFT.follicleTransformAll, secRGT.follicleTransformAll, main.follicleTransformAll, ctrlFaceGroup)

        self.ctrlFaceGroup = ctrlFaceGroup
        self.neckCtrlGrp = main.neckCtrlGrp
        self.eyeballAimMainCtrlGrp = main.eyeballAimMainCtrlGrp
        self.eyeballAimMainCtrl = main.eyeballAimMainCtrl
        self.headCtrlGrp = main.headCtrlGrp

        # # coonect nose ctrl to ctrl nostril offset grp LFT
        # au.connectAttrObject(main.noseCtrl, secLFT.nostrilCtrlOffset)
        #
        # # coonect nose ctrl to ctrl nostril offset grp RGT
        # transMdn = mc.createNode('multiplyDivide', n='noseTrans_mdn')
        # mc.connectAttr(main.noseCtrl+'.translate', transMdn+'.input1')
        # mc.setAttr(transMdn+'.input2Z', -1)
        #
        # rotMdn = mc.createNode('multiplyDivide', n='noseRot_mdn')
        # mc.connectAttr(main.noseCtrl+'.rotate', rotMdn+'.input1')
        # mc.setAttr(rotMdn+'.input2Z', -1)

        # mc.connectAttr(transMdn+'.output', secRGT.nostrilCtrlOffset+'.translate')
        # mc.connectAttr(rotMdn+'.output', secRGT.nostrilCtrlOffset+'.rotate')

        # PARENTING GRP
        # mc.parent(main.noseCtrlGrp, secLFT.cheekUpCtrlGrp, secRGT.cheekUpCtrlGrp, secLFT.browInCtrlGrp, secRGT.browInCtrlGrp,
        #           secLFT.browMidCtrlGrp, secRGT.browMidCtrlGrp, secLFT.browOutCtrlGrp, secRGT.browOutCtrlGrp,
        #           secLFT.eyelidPinchCtrlGrp, secRGT.eyelidPinchCtrlGrp, secLFT.eyebrowCtrlGrp, secRGT.eyebrowCtrlGrp,
        #           secLFT.nostrilCtrlGrp, secRGT.nostrilCtrlGrp, secLFT.cheekDownCtrlGrp, secRGT.cheekDownCtrlGrp,
        #           ctrlFaceGroup)
