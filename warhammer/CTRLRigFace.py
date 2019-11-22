from rigModule import mainSecondaryModule as ms, eyelidModule as em
import skeletonDriverModule as sd

reload(ms)
reload(sd)
reload(em)



def buildRig(scale=1.0,
             positionEyeAimCtrl=15):
# ======================================================================================================================
#                                              DUPLICATE JOINTS AS DRIVER
# ======================================================================================================================
    sj = sd.listFaceSkeletonDuplicate(objDuplicate='neck01Tmp_jnt',
                                      valuePrefix='',
                                      keyPrefix='Ori',
                                      suffix='jnt'
                                      )

    # ss = sd.listFaceSkeletonDuplicate(objDuplicate='neck01Tmp_jnt',
    #                                   valuePrefix=ScaleDriver,
    #                                   keyPrefix='Scl',
    #                                   suffix='jnt'
    #                                   )

    mainFace = ms.MainFace(neckJnt=sj.neck,
                 headJnt=sj.head01,
                 headUpJnt=sj.headUp01,
                 headLowJnt=sj.headLow01,
                 jawJnt=sj.jaw01,
                 noseJnt=sj.nose,
                 noseTipJnt=sj.noseTip,
                 chinJnt=sj.chin,
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
                 sideLFT='LFT',
                 sideRGT='RGT',
                 eyeballJntLFT=sj.eyeballLFT,
                 eyeballJntRGT=sj.eyeballRGT,
                 prefixEyeballAim='eyeballAim',
                 positionEyeAimCtrl=positionEyeAimCtrl,
               )

    eyelidLFT = em.Eyelid(crvUp='eyelidUpLFT_crv',
                 crvDown='eyelidDownLFT_crv',
                 headUpJoint=sj.headUp01,
                 eyeballJnt=sj.eyeballLFT,
                 prefixEyeball='eyeball',
                 prefixEyeballAim='eyeballAim',
                 scale=scale,
                 side='LFT',
                 directionLip01=15,
                 directionLip02=10,
                 positionEyeAimCtrl=positionEyeAimCtrl,
                 eyeballAimMainCtrl=mainFace.eyeballAimMainCtrl
                 )


    eyelidRGT = em.Eyelid(crvUp='eyelidUpRGT_crv',
                          crvDown='eyelidDownRGT_crv',
                          headUpJoint=sj.headUp01,
                          eyeballJnt=sj.eyeballRGT,
                          prefixEyeball='eyeball',
                          prefixEyeballAim='eyeballAim',
                          scale=scale,
                          side='RGT',
                          directionLip01=15,
                          directionLip02=10,
                          positionEyeAimCtrl=positionEyeAimCtrl,
                          eyeballAimMainCtrl=mainFace.eyeballAimMainCtrl
                          )