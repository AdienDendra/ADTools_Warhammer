import maya.cmds as mc
from warhammer.rig import eyelid as el


class Eyelids:
    def __init__(self, crv,
                 scale,
                 sideLFT,
                 sideRGT,
                 offsetJnt02BindPos,
                 directionCtrl01,
                 directionCtrl02,
                 ctrlColor, shape):

        eyelid = el.controller(crv, scale, sideLFT, sideRGT, offsetJnt02BindPos, directionCtrl01, directionCtrl02,
                               ctrlColor, shape, controllerWireDown=False)
