import maya.cmds as mc
import ADUtils as au
from warhammer.rig import main as mn, secondary as sc

reload(mn)
reload(sc)
reload(au)


class MainFace:
    def __init__(self,
                 neckJnt,
                 headJnt,
                 headUpJnt,
                 headLowJnt,
                 jawJnt,
                 noseJnt,
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

        main = mn.Build(objectFolMesh=objectFolMesh,
                        neckJnt=neckJnt,
                         headJnt=headJnt,
                         headUpJnt=headUpJnt,
                         headLowJnt=headLowJnt,
                         jawJnt=jawJnt,
                         noseJnt=noseJnt,
                         noseTipJnt=noseTipJnt,
                         chinJnt=chinJnt,
                         scale=scale,
                         eyeballJntLFT=eyeballJntLFT,
                         eyeballJntRGT=eyeballJntRGT,
                         prefixEyeballAim=prefixEyeballAim,
                         positionEyeAimCtrl=positionEyeAimCtrl,
                        )

        self.eyeballAimMainCtrl = main.eyeballAimMainCtrl

        secLFT = sc.Build(objectFolMesh=objectFolMesh,
                          nostrilJnt=nostrilLFTJnt,
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

        # constraint
        mc.parentConstraint(headLowJnt, jawJnt, secLFT.cheekDownJntGrp, mo=1)
        mc.parentConstraint(headLowJnt, jawJnt, secRGT.cheekDownJntGrp, mo=1)

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

        mc.parent(secLFT.follicleTransformAll, secRGT.follicleTransformAll, main.follicleTransformAll, ctrlFaceGroup)