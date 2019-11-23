import maya.cmds as mc
import ADUtils as au, ADCtrl as ct

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
                 scale,
                 side):

        self.pos = mc.xform(lipCornerJnt, q=1, ws=1, t=1)[0]

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

        # flipping controller
        self.flippingCtrl(self.corner,downlip=False)
        self.flippingCtrl(self.upLip01,downlip=False)
        self.flippingCtrl(self.upLip02,downlip=False)
        self.flippingCtrl(self.downLip01,downlip=True)
        self.flippingCtrl(self.downLip02,downlip=True)

        # corner
        self.rotation(object=self.corner.parentControl[0], directionLip=directionLipCorner)
        self.rotation(object=self.upLip01.parentControl[0], directionLip=directionLip01)
        self.rotation(object=self.upLip02.parentControl[0], directionLip=directionLip02)
        self.rotation(object=self.downLip01.parentControl[0], directionLip=directionLip01)
        self.rotation(object=self.downLip02.parentControl[0], directionLip=directionLip02)


        mc.parentConstraint(self.corner.control, lipCornerJnt, mo=1)
        mc.parentConstraint(self.upLip01.control, lipUpJnt01, mo=1)
        mc.parentConstraint(self.upLip02.control, lipUpJnt02, mo=1)
        mc.parentConstraint(self.downLip01.control, lipDownJnt01,  mo=1)
        mc.parentConstraint(self.downLip02.control, lipDownJnt02, mo=1)

        mc.scaleConstraint(self.corner.control, lipCornerJnt, mo=1)
        mc.scaleConstraint(self.upLip01.control, lipUpJnt01, mo=1)
        mc.scaleConstraint(self.upLip02.control, lipUpJnt02, mo=1)
        mc.scaleConstraint(self.downLip01.control, lipDownJnt01,  mo=1)
        mc.scaleConstraint(self.downLip02.control, lipDownJnt02, mo=1)

        object = [self.cornerParentCtrl, self.upLip01ParentCtrl, self.upLip02ParentCtrl, self.downLip01ParentCtrl, self.downLip02ParentCtrl]
        self.follicleTransformAll=[]
        for i in object:
            follicleTransform = au.createFollicleSel(objSel=i, objMesh=objectFolMesh, connectFol=['transConn', 'rotateConn'])[0]
            mc.parent(i, follicleTransform)
            self.follicleTransformAll.append(follicleTransform)

    def flippingCtrl(self, object, downlip):
        if mc.xform(object.parentControl[0], q=1, ws=1, t=1)[0] < 0:
            mc.setAttr(object.parentControl[0] + '.scaleX', -1)

            if downlip:
                mc.setAttr(object.parentControl[0] + '.scaleY', -1)
        else:
            if downlip:
                mc.setAttr(object.parentControl[0] + '.scaleY', -1)

    def rotation(self, object, directionLip):
        if mc.xform(object, q=1, ws=1, t=1)[0] <0:
            mc.setAttr(object+ '.rotateY', directionLip * -1)
        else:
            mc.setAttr(object + '.rotateY', directionLip)
