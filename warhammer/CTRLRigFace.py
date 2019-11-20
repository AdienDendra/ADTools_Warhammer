from rigModule import mainSecondaryModule as ms, eyelidModule as em
import skeletonDriverModule as sd

reload(ms)
reload(sd)
reload(em)



def buildRig(scale=1.0):
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
                 sideRGT='RGT')

    eyelidLFT = em.Eyelids(crv,
                 scale,
                 sideLFT,
                 sideRGT,
                 offsetJnt02BindPos,
                 directionCtrl01,
                 directionCtrl02,
                 ctrlColor, shape)