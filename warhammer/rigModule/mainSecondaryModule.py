import maya.cmds as mc
from warhammer.rig import main as mn, secondary as sc

reload(mn)
reload(sc)


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
                 ):

        # BUILD CONTROLLER

        main = mn.Build(neckJnt=neckJnt,
                 headJnt=headJnt,
                 headUpJnt=headUpJnt,
                 headLowJnt=headLowJnt,
                 jawJnt=jawJnt,
                 noseJnt=noseJnt,
                 noseTipJnt=noseTipJnt,
                 chinJnt=chinJnt,
                 scale=scale)

        secLFT = sc.Build(nostrilJnt=nostrilLFTJnt,
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

        secRGT = sc.Build(nostrilJnt=nostrilRGTJnt,
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

        # PARENTING GRP
        mc.parent(secLFT.nostrilCtrlGrp, secRGT.nostrilCtrlGrp, main.noseCtrl)

        mc.parent(secLFT.cheekUpCtrlGrp, secRGT.cheekUpCtrlGrp,
                  secLFT.browInCtrlGrp, secRGT.browInCtrlGrp,
                  secLFT.browMidCtrlGrp, secRGT.browMidCtrlGrp,
                  secLFT.browOutCtrlGrp, secRGT.browOutCtrlGrp,
                  secLFT.eyelidPinchCtrlGrp, secRGT.eyelidPinchCtrlGrp,
                  secLFT.eyebrowCtrlGrp, secRGT.eyebrowCtrlGrp,
                  main.headUpCtrl)

        mc.parent(secLFT.cheekDownCtrlGrp, secRGT.cheekDownCtrlGrp,
                  main.jawCtrl)