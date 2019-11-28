from rigModule import mainSecondaryModule as ms, eyelidModule as em, lipModule as lm
import skeletonDriverModule as sd
import maya.cmds as mc

reload(ms)
reload(sd)
reload(em)
reload(lm)



def buildRig(scale=1.0,
             positionEyeAimCtrl=15,
             directionLipCorner=40,
             directionLip01=35,
             directionLip02=25,
             directionLid01=15,
             directionLid02=10,
             offsetEyelidPos=4,
             sideLFT='LFT',
             sideRGT='RGT',
             eyeballAim='eyeballAim',
             eyeball='eyeball',
             objectFolMesh='captainCtrlFol_ply'
             ):
# ======================================================================================================================
#                                              DUPLICATE JOINTS AS DRIVER
# ======================================================================================================================
    if mc.objExists('neck01_jnt'):
        mc.error('%s%s%s' % ('Please remove the',' neck01_jnt ', 'joint first!'))

    sj = sd.listFaceSkeletonDuplicate(objDuplicate='neck01Tmp_jnt',
                                      valuePrefix='',
                                      keyPrefix='Ori',
                                      suffix='jnt'
                                      )

    ctrlGrp = mc.group(em=1, n='worldSpace_grp')
    utilsGrp = mc.group(em=1, n='utils_grp')

    mainFace = ms.MainFace(ctrlGrp=ctrlGrp,
                           neckJnt=sj.neck,
                         headJnt=sj.head01,
                         headUpJnt=sj.headUp01,
                         earLFTJnt=sj.earLFT,
                         earRGTJnt=sj.earRGT,
                         headLowJnt=sj.headLow01,
                         jawJnt=sj.jaw01,
                         noseJnt=sj.nose,
                         upperTeethJnt=sj.upperTeeth,
                         lowerTeethJnt=sj.lowerTeeth,
                         tongue01Jnt=sj.tongue01,
                         tongue02Jnt=sj.tongue02,
                         tongue03Jnt=sj.tongue03,
                         tongue04Jnt=sj.tongue04,
                         noseTipJnt=sj.noseTip,
                         chinJnt=sj.chin,
                         throatJnt= sj.throat,
                         scale=scale,
                         nostrilLFTJnt=sj.nostrilLFT,
                         cheekUpLFTJnt=sj.cheekUpLFT,
                         cheekDownLFTJnt=sj.cheekDownLFT,
                         eyebrowInLFTJnt=sj.eyebrowInLFT,
                         eyebrowMidLFTJnt=sj.eyebrowMidLFT,
                         eyebrowOutLFTJnt=sj.eyebrowOutLFT,
                         browInLFTJnt=sj.browInLFT,
                         browMidLFTJnt=sj.browMidLFT,
                         browOutLFTJnt=sj.browOutLFT,
                         eyelidPinchLFTJnt=sj.eyelidPinchLFT,
                         nostrilRGTJnt=sj.nostrilRGT,
                         cheekUpRGTJnt=sj.cheekUpRGT,
                         cheekDownRGTJnt=sj.cheekDownRGT,
                         eyebrowInRGTJnt=sj.eyebrowInRGT,
                         eyebrowMidRGTJnt=sj.eyebrowMidRGT,
                         eyebrowOutRGTJnt=sj.eyebrowOutRGT,
                         browInRGTJnt=sj.browInRGT,
                         browMidRGTJnt=sj.browMidRGT,
                         browOutRGTJnt=sj.browOutRGT,
                         eyelidPinchRGTJnt=sj.eyelidPinchRGT,
                         sideLFT=sideLFT,
                         sideRGT=sideRGT,
                         eyeballJntLFT=sj.eyeballLFT,
                         eyeballJntRGT=sj.eyeballRGT,
                         prefixEyeballAim=eyeballAim,
                         positionEyeAimCtrl=positionEyeAimCtrl,
                         objectFolMesh=objectFolMesh,
                       )

    eyelidLFT = em.Eyelid(crvUp='eyelidUpLFT_crv',
                          crvDown='eyelidDownLFT_crv',
                          offsetEyelidPos=offsetEyelidPos,
                          eyeballJnt=sj.eyeballLFT,
                          prefixEyeball=eyeball,
                          prefixEyeballAim=eyeballAim,
                          scale=scale,
                          side=sideLFT,
                          directionLid01=directionLid01,
                          directionLid02=directionLid02,
                          positionEyeAimCtrl=positionEyeAimCtrl,
                          eyeballAimMainCtrl=mainFace.eyeballAimMainCtrl,
                          headUpCtrl= mainFace.headUpCtrl
                          )


    eyelidRGT = em.Eyelid(crvUp='eyelidUpRGT_crv',
                          crvDown='eyelidDownRGT_crv',
                          offsetEyelidPos=offsetEyelidPos,
                          eyeballJnt=sj.eyeballRGT,
                          prefixEyeball=eyeball,
                          prefixEyeballAim=eyeballAim,
                          scale=scale,
                          side=sideRGT,
                          directionLid01=directionLid01,
                          directionLid02=directionLid02,
                          positionEyeAimCtrl=positionEyeAimCtrl,
                          eyeballAimMainCtrl=mainFace.eyeballAimMainCtrl,
                          headUpCtrl = mainFace.headUpCtrl
                          )

    lip = lm.Lip(objectFolMesh=objectFolMesh,
                 lipMidUpJnt=sj.lipMidUp,
                 lipUpLFTJnt01=sj.lipUp01LFT,
                 lipMidDownJnt=sj.lipMidDown,
                 lipDownLFTJnt02=sj.lipDown02LFT,
                 lipDownLFTJnt01=sj.lipDown01LFT,
                 lipUpLFTJnt02=sj.lipUp02LFT,
                 lipCornerLFTJnt=sj.lipCornerLFT,
                 lipUpRGTJnt01=sj.lipUp01RGT,
                 lipUpRGTJnt02=sj.lipUp02RGT,
                 lipDownRGTJnt01=sj.lipDown01RGT,
                 lipDownRGTJnt02=sj.lipDown02RGT,
                 lipCornerRGTJnt=sj.lipCornerRGT,
                 scale=scale,
                 headLowCtrl=mainFace.headLowCtrl,
                 directionLipCorner=directionLipCorner,
                 directionLip01=directionLip01,
                 directionLip02=directionLip02,
                 sideLFT=sideLFT,
                 sideRGT=sideRGT
                 )

    # PARENT TO THE GROUP
    # mc.parent(mainFace.neckCtrlGrp, mainFace.ctrlFaceGroup, lip.lipGroup, ctrlGrp)

    mc.parent('mainJnt_grp', 'faceCrv_grp', eyelidLFT.blink, eyelidRGT.blink,
              eyelidLFT.eyeballMoveGrp, eyelidRGT.eyeballMoveGrp, ctrlGrp, utilsGrp)