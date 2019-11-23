import maya.cmds as mc
from warhammer.rig import lip as lp
import ADUtils as au, ADCtrl as ct

reload(au)
reload(ct)
reload(lp)

class Lip:
    def __init__(self,
                 objectFolMesh='captainMouthFol_ply',
                 lipMidUpJnt='lipMidUp_jnt',
                 lipUpLFTJnt01='lipUp01LFT_jnt',
                 lipMidDownJnt='lipMidDown_jnt',
                 lipDownLFTJnt02='lipDown02LFT_jnt',
                 lipDownLFTJnt01='lipDown01LFT_jnt',
                 lipUpLFTJnt02='lipUp02LFT_jnt',
                 lipCornerLFTJnt='lipCornerLFT_jnt',
                 lipUpRGTJnt01='lipUp01RGT_jnt',
                 lipUpRGTJnt02='lipUp02RGT_jnt',
                 lipDownRGTJnt01='lipDown01RGT_jnt',
                 lipDownRGTJnt02='lipDown02RGT_jnt',
                 lipCornerRGTJnt='lipCornerRGT_jnt',
                 scale=1,
                 directionLipCorner=40,
                 directionLip01=35,
                 directionLip02=25,
                 sideLFT='LFT',
                 sideRGT='RGT'):

        lipGroup = mc.group(em=1, n='lipCtrl_grp')

        lipLFT = lp.Build(objectFolMesh=objectFolMesh,
                          lipUpJnt01=lipUpLFTJnt01,
                          lipUpJnt02=lipUpLFTJnt02,
                          lipDownJnt01=lipDownLFTJnt01,
                          lipDownJnt02=lipDownLFTJnt02,
                          lipCornerJnt=lipCornerLFTJnt,
                          scale=scale,
                          directionLipCorner=directionLipCorner,
                          directionLip01=directionLip01,
                          directionLip02=directionLip02,
                          side=sideLFT)

        lipRGT = lp.Build(objectFolMesh=objectFolMesh,
                          lipUpJnt01=lipUpRGTJnt01,
                          lipUpJnt02=lipUpRGTJnt02,
                          lipDownJnt01=lipDownRGTJnt01,
                          lipDownJnt02=lipDownRGTJnt02,
                          lipCornerJnt=lipCornerRGTJnt,
                          scale=scale,
                          directionLipCorner=directionLipCorner,
                          directionLip01=directionLip01,
                          directionLip02=directionLip02,
                          side=sideRGT)

        self.lipMidUp= ct.Control(matchPos=lipMidUpJnt, prefix=au.prefixName(lipMidUpJnt),
                                           shape=ct.JOINT, groupsCtrl=['','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v',])
        self.lipMidUpParentCtrl = self.lipMidUp.parentControl[0]

        self.lipMidDown= ct.Control(matchPos=lipMidDownJnt, prefix=au.prefixName(lipMidDownJnt),
                                           shape=ct.JOINT, groupsCtrl=['','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'])
        self.lipMidDownParentCtrl = self.lipMidDown.parentControl[0]

        mc.setAttr(self.lipMidDown.parentControl[0] + '.scaleY', -1)

        # constraint lip mid
        mc.parentConstraint(self.lipMidUp.control, lipMidUpJnt, mo=1)
        mc.parentConstraint(self.lipMidDown.control, lipMidDownJnt, mo=1)

        mc.scaleConstraint(self.lipMidUp.control, lipMidUpJnt, mo=1)
        mc.scaleConstraint(self.lipMidDown.control, lipMidDownJnt, mo=1)

        object = [self.lipMidUpParentCtrl, self.lipMidDownParentCtrl]
        follTransMid = []
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            follTransMid.append(follicleTransform)

        mc.parent(follTransMid, lipLFT.follicleTransformAll, lipRGT.follicleTransformAll, lipGroup)

