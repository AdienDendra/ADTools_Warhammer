import maya.cmds as mc
import ADUtils as au, ADCtrl as ct
import re
from string import digits

reload(au)
reload(ct)

class Build:
    def __init__(self,
                 objectFolMesh,
                 lipUpJnt01,
                 lipUpJnt02,
                 lipDownJnt01,
                 lipDownJnt02,
                 lipCornerJnt,
                 directionLipCorner,
                 directionLip01,
                 directionLip02,
                 headLowCtrl,
                 jawCtrl,
                 scale,
                 sideRGT,
                 sideLFT,
                 side):

        self.pos = mc.xform(lipCornerJnt, q=1, ws=1, t=1)[0]

        # corner
        self.rotation(object=lipCornerJnt, directionLip=directionLipCorner)
        self.rotation(object=lipUpJnt01, directionLip=directionLip01)
        self.rotation(object=lipUpJnt02, directionLip=directionLip02)
        self.rotation(object=lipDownJnt01, directionLip=directionLip01)
        self.rotation(object=lipDownJnt02, directionLip=directionLip02)

        mc.makeIdentity(lipCornerJnt, apply=True, t=1, r=1, s=1, n=2)
        mc.makeIdentity(lipUpJnt01, apply=True, t=1, r=1, s=1, n=2)
        mc.makeIdentity(lipUpJnt02, apply=True, t=1, r=1, s=1, n=2)
        mc.makeIdentity(lipDownJnt01, apply=True, t=1, r=1, s=1, n=2)
        mc.makeIdentity(lipDownJnt02, apply=True, t=1, r=1, s=1, n=2)

        # controller
        self.corner= ct.Control(matchPos=lipCornerJnt, prefix='lipCorner',
                                           shape=ct.JOINT, groupsCtrl=['Zro','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'], side=side)
        self.cornerParentCtrl = self.corner.parentControl[0]

        self.upLip01= ct.Control(matchPos=lipUpJnt01, prefix='lipUp01',
                                           shape=ct.JOINT, groupsCtrl=['Zro','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'], side=side)
        self.upLip01ParentCtrl = self.upLip01.parentControl[0]

        self.upLip02= ct.Control(matchPos=lipUpJnt02, prefix='lipUp02',
                                           shape=ct.JOINT, groupsCtrl=['Zro','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'], side=side)
        self.upLip02ParentCtrl = self.upLip02.parentControl[0]

        self.downLip01= ct.Control(matchPos=lipDownJnt01, prefix='lipDown01',
                                           shape=ct.JOINT, groupsCtrl=['Zro','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'], side=side)
        self.downLip01ParentCtrl = self.downLip01.parentControl[0]


        self.downLip02= ct.Control(matchPos=lipDownJnt02, prefix='lipDown02',
                                           shape=ct.JOINT, groupsCtrl=['Zro','Offset'], ctrlSize=scale * 0.4,
                                           ctrlColor='red', lockChannels=['v'], side=side)
        self.downLip02ParentCtrl = self.downLip02.parentControl[0]

        cornerGrpJnt = au.createParentTransform(listparent=[''], object=lipCornerJnt, matchPos=lipCornerJnt, prefix='lipCorner', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=lipUpJnt01, matchPos=lipUpJnt01, prefix='lipUp01', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=lipUpJnt02, matchPos=lipUpJnt02, prefix='lipUp02', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=lipDownJnt01, matchPos=lipDownJnt01, prefix='lipDown01', suffix='_jnt', side=side)
        au.createParentTransform(listparent=[''], object=lipDownJnt02, matchPos=lipDownJnt02, prefix='lipDown02', suffix='_jnt', side=side)


        # flipping controller
        self.flippingCtrl(sideRGT, sideLFT, self.corner,downlip=False, side=side, jointTgt=lipCornerJnt)
        self.flippingCtrl(sideRGT, sideLFT, self.upLip01,downlip=False, side=side, jointTgt=lipUpJnt01)
        self.flippingCtrl(sideRGT, sideLFT, self.upLip02,downlip=False, side=side, jointTgt=lipUpJnt02)
        self.flippingCtrl(sideRGT, sideLFT, self.downLip01,downlip=True, side=side, jointTgt=lipDownJnt01)
        self.flippingCtrl(sideRGT, sideLFT, self.downLip02,downlip=True, side=side, jointTgt=lipDownJnt02)

        au.connectAttrScale(self.corner.control, lipCornerJnt)
        au.connectAttrScale(self.upLip01.control, lipUpJnt01)
        au.connectAttrScale(self.upLip02.control, lipUpJnt02)
        au.connectAttrScale(self.downLip01.control, lipDownJnt01)
        au.connectAttrScale(self.downLip02.control, lipDownJnt02)


        object = [self.cornerParentCtrl, self.upLip01ParentCtrl, self.upLip02ParentCtrl,
                  self.downLip01ParentCtrl, self.downLip02ParentCtrl]
        self.follicleTransformAll=[]
        for i in object:
            follicle = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn'])[0]
            mc.parent(i, follicle)
            mc.scaleConstraint(headLowCtrl, follicle)

            self.follicleTransformAll.append(follicle)

        mc.orientConstraint(jawCtrl, self.follicleTransformAll[0], mo=1)
        mc.orientConstraint(jawCtrl, self.follicleTransformAll[3], mo=1)
        mc.orientConstraint(jawCtrl,self.follicleTransformAll[4], mo=1)

        mc.orientConstraint(headLowCtrl,self.follicleTransformAll[1], mo=1)
        mc.orientConstraint(headLowCtrl,self.follicleTransformAll[2], mo=1)

        # CONSTRAINT CORNER JNT GRP
        mc.parentConstraint(headLowCtrl, jawCtrl, cornerGrpJnt, mo=1)

    def flippingCtrl(self, sideRGT, sideLFT, object, downlip, side, jointTgt):
        if sideRGT in object.control:
            newName = object.control.replace(sideRGT, '')
        elif sideLFT in object.control:
            newName = object.control.replace(sideLFT, '')
        else:
            newName = object.control
            # get the number
        try:
            patterns = [r'\d+']
            prefixNumber = au.prefixName(newName)
            for p in patterns:
                prefixNumber = re.findall(p, prefixNumber)[0]
        except:
            prefixNumber = ''
        # get the prefix without number
        prefixNoNumber = str(au.prefixName(newName)).translate(None, digits)

        transMult = mc.createNode('multiplyDivide', n=prefixNoNumber + 'Trans' + prefixNumber + side + '_mdn')
        rotMult = mc.createNode('multiplyDivide', n=prefixNoNumber + 'Rot' + prefixNumber + side + '_mdn')

        if mc.xform(object.parentControl[0], q=1, ws=1, t=1)[0] < 0:
            mc.setAttr(object.parentControl[0] + '.scaleX', -1)
            mc.setAttr(transMult + '.input2X', -1)
            mc.setAttr(rotMult + '.input2Z', -1)
            mc.setAttr(rotMult + '.input2Y', -1)
            if downlip:
                mc.setAttr(object.parentControl[0] + '.scaleY', -1)
                mc.setAttr(transMult + '.input2Y', -1)
                mc.setAttr(rotMult + '.input2Z', 1)
                mc.setAttr(rotMult + '.input2X', -1)
        else:
            if downlip:
                mc.setAttr(object.parentControl[0] + '.scaleY', -1)
                mc.setAttr(transMult+'.input2Y', -1)
                mc.setAttr(rotMult+'.input2Z', -1)
                mc.setAttr(rotMult + '.input2X', -1)

        mc.connectAttr(object.control + '.translate', transMult + '.input1')
        mc.connectAttr(object.control + '.rotate', rotMult + '.input1')

        mc.connectAttr(transMult + '.output', jointTgt + '.translate')
        mc.connectAttr(rotMult + '.output', jointTgt + '.rotate')

    def rotation(self, object, directionLip):
        if mc.xform(object, q=1, ws=1, t=1)[0] <0:
            mc.setAttr(object+ '.rotateY', directionLip * -1)
        else:
            mc.setAttr(object + '.rotateY', directionLip)
