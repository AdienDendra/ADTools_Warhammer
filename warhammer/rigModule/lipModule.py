import maya.cmds as mc
from warhammer.rig import lip as lp
import ADUtils as au, ADCtrl as ct

reload(au)
reload(ct)
reload(lp)

class Lip:
    def __init__(self,
                 objectFolMesh,
                 lipMidUpJnt,
                 lipUpLFTJnt01,
                 lipMidDownJnt,
                 lipDownLFTJnt02,
                 lipDownLFTJnt01,
                 lipUpLFTJnt02,
                 lipCornerLFTJnt,
                 lipUpRGTJnt01,
                 lipUpRGTJnt02,
                 lipDownRGTJnt01,
                 lipDownRGTJnt02,
                 lipCornerRGTJnt,
                 scale,
                 directionLipCorner,
                 directionLip01,
                 directionLip02,
                 sideLFT,
                 sideRGT):

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

