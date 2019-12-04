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
                 jawCtrl,
                 scale,
                 headLowCtrl,
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
                          headLowCtrl=headLowCtrl,
                          jawCtrl=jawCtrl,
                          directionLipCorner=directionLipCorner,
                          directionLip01=directionLip01,
                          directionLip02=directionLip02,
                          sideRGT=sideRGT,
                          sideLFT=sideLFT,
                          side=sideLFT)

        lipRGT = lp.Build(objectFolMesh=objectFolMesh,
                          lipUpJnt01=lipUpRGTJnt01,
                          lipUpJnt02=lipUpRGTJnt02,
                          lipDownJnt01=lipDownRGTJnt01,
                          lipDownJnt02=lipDownRGTJnt02,
                          lipCornerJnt=lipCornerRGTJnt,
                          scale=scale,
                          headLowCtrl=headLowCtrl,
                          jawCtrl=jawCtrl,
                          directionLipCorner=directionLipCorner,
                          directionLip01=directionLip01,
                          directionLip02=directionLip02,
                          sideRGT=sideRGT,
                          sideLFT=sideLFT,
                          side=sideRGT)

        self.lipMidUp= ct.Control(matchPos=lipMidUpJnt, prefix=au.prefixName(lipMidUpJnt),
                                           shape=ct.JOINT, groupsCtrl=['','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v',])

        self.lipMidDown= ct.Control(matchPos=lipMidDownJnt, prefix=au.prefixName(lipMidDownJnt),
                                           shape=ct.JOINT, groupsCtrl=['','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'])

        self.lipMidUpParentCtrl = self.lipMidUp.parentControl[0]
        self.lipMidDownParentCtrl = self.lipMidDown.parentControl[0]

        au.createParentTransform(listparent=[''], object=lipMidUpJnt, matchPos=lipMidUpJnt, prefix='lipMidUp', suffix='_jnt')
        au.createParentTransform(listparent=[''], object=lipMidDownJnt, matchPos=lipMidDownJnt, prefix='lipMidDown', suffix='_jnt')

        # lip mid up setup
        au.connectAttrObject(self.lipMidUp.control, lipMidUpJnt)

        # lip mid down setup
        mc.setAttr(self.lipMidDown.parentControl[0] + '.scaleY', -1)
        transMult = mc.createNode('multiplyDivide', n=au.prefixName(self.lipMidDown.control) + 'Trans'  + '_mdn')
        rotMult = mc.createNode('multiplyDivide', n=au.prefixName(self.lipMidDown.control) + 'Rot' + '_mdn')
        mc.setAttr(transMult + '.input2Y', -1)
        mc.setAttr(rotMult + '.input2Z', -1)
        mc.setAttr(rotMult + '.input2X', -1)

        mc.connectAttr(self.lipMidDown.control + '.translate', transMult + '.input1')
        mc.connectAttr(self.lipMidDown.control + '.rotate', rotMult + '.input1')

        mc.connectAttr(transMult + '.output', lipMidDownJnt + '.translate')
        mc.connectAttr(rotMult + '.output', lipMidDownJnt + '.rotate')

        # au.connectAttrObject(self.lipMidDown.control, lipMidDownJnt)

        # constraint lip mid

        # mc.parentConstraint(self.lipMidUp.control, lipMidUpJnt, mo=1)
        # mc.parentConstraint(self.lipMidDown.control, lipMidDownJnt, mo=1)
        #
        # mc.scaleConstraint(self.lipMidUp.control, lipMidUpJnt, mo=1)
        # mc.scaleConstraint(self.lipMidDown.control, lipMidDownJnt, mo=1)

        object = [self.lipMidUpParentCtrl, self.lipMidDownParentCtrl]
        follTransMid = []
        for i in object:
            follicle = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn'])[0]
            mc.parent(i, follicle)
            mc.scaleConstraint(headLowCtrl, follicle)
            follTransMid.append(follicle)

        mc.orientConstraint(jawCtrl, follTransMid[1])
        mc.orientConstraint(headLowCtrl, follTransMid[0])

        mc.parent(follTransMid, lipLFT.follicleTransformAll, lipRGT.follicleTransformAll, lipGroup)

        self.lipGroup = lipGroup

