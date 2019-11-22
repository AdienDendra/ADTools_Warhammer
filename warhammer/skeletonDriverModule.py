import maya.cmds as mc
import ADUtils as au
reload (au)


class listFaceSkeletonDuplicate:
    # HEAD PART AND FACE
    def __init__(self, objDuplicate,
                 valuePrefix,
                 keyPrefix,
                 suffix,
                 oriPrefix='',
                 ):

        hide = mc.ls(type='joint')
        mc.hide(hide)

        # DUPLICATE SKELETON
        sj = au.listSkeletonDic(objDuplicate=objDuplicate,
                                valuePrefix=valuePrefix,
                                keyPrefix=keyPrefix,
                                oriPrefix=oriPrefix,
                                suffix=suffix)

        # NECK AND HEAD
        self.neck       = sj['%s%s%s_%s' % ('neck01', oriPrefix, keyPrefix, suffix)]
        self.head01     = sj['%s%s%s_%s' % ('head01', oriPrefix, keyPrefix, suffix)]
        self.head02     = sj['%s%s%s_%s' % ('head02', oriPrefix, keyPrefix, suffix)]


        self.headUp01      = sj['%s%s%s_%s' % ('headUp01', oriPrefix, keyPrefix, suffix)]
        self.headLow01     = sj['%s%s%s_%s' % ('headLow01', oriPrefix, keyPrefix, suffix)]
        self.jaw01     = sj['%s%s%s_%s' % ('jaw01', oriPrefix, keyPrefix, suffix)]
        self.chin     = sj['%s%s%s_%s' % ('chin', oriPrefix, keyPrefix, suffix)]


        # EYELIDS LFT
        self.eyebrowInLFT    = sj['%s%s%s%s_%s' % ('eyebrowIn', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.eyebrowMidLFT    = sj['%s%s%s%s_%s' % ('eyebrowMid', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.eyebrowOutLFT    = sj['%s%s%s%s_%s' % ('eyebrowOut', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.eyelidPinchLFT    = sj['%s%s%s%s_%s' % ('eyelidPinch', oriPrefix, keyPrefix, 'LFT', suffix)]

        # BROW LFT
        self.browInLFT    = sj['%s%s%s%s_%s' % ('browIn', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.browMidLFT    = sj['%s%s%s%s_%s' % ('browMid', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.browOutLFT    = sj['%s%s%s%s_%s' % ('browOut', oriPrefix, keyPrefix, 'LFT', suffix)]

        # CHEEK MID LFT SIDE
        self.cheekUpLFT     = sj['%s%s%s%s_%s' % ('cheekUp', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.cheekDownLFT   = sj['%s%s%s%s_%s' % ('cheekDown', oriPrefix, keyPrefix, 'LFT', suffix)]

        # NOSE LFT
        self.nose    = sj['%s%s%s_%s' % ('nose', oriPrefix, keyPrefix, suffix)]
        self.noseTip    = sj['%s%s%s_%s' % ('noseTip', oriPrefix, keyPrefix, suffix)]
        self.nostrilLFT = sj['%s%s%s%s_%s' % ('nostril', oriPrefix, keyPrefix, 'LFT', suffix)]

        # LIP
        self.lipMidUp    = sj['%s%s%s_%s' % ('lipMidUp', oriPrefix, keyPrefix, suffix)]
        self.lipMidDown  = sj['%s%s%s_%s' % ('lipMidDown', oriPrefix, keyPrefix, suffix)]

        # LIP LFT
        self.lipUp01LFT    = sj['%s%s%s%s_%s' % ('lipUp01', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.lipUp02LFT    = sj['%s%s%s%s_%s' % ('lipUp02', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.lipDown01LFT  = sj['%s%s%s%s_%s' % ('lipDown01', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.lipDown02LFT  = sj['%s%s%s%s_%s' % ('lipDown02', oriPrefix, keyPrefix, 'LFT', suffix)]

        self.lipCornerLFT    = sj['%s%s%s%s_%s' % ('lipCorner', oriPrefix, keyPrefix, 'LFT', suffix)]

        # EYELIDS RGT
        self.eyebrowInRGT    = sj['%s%s%s%s_%s' % ('eyebrowIn', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.eyebrowMidRGT    = sj['%s%s%s%s_%s' % ('eyebrowMid', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.eyebrowOutRGT    = sj['%s%s%s%s_%s' % ('eyebrowOut', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.eyelidPinchRGT    = sj['%s%s%s%s_%s' % ('eyelidPinch', oriPrefix, keyPrefix, 'RGT', suffix)]

        # BROW RGT
        self.browInRGT    = sj['%s%s%s%s_%s' % ('browIn', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.browMidRGT    = sj['%s%s%s%s_%s' % ('browMid', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.browOutRGT    = sj['%s%s%s%s_%s' % ('browOut', oriPrefix, keyPrefix, 'RGT', suffix)]

        # CHEEK MID RGT SIDE
        self.cheekUpRGT     = sj['%s%s%s%s_%s' % ('cheekUp', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.cheekDownRGT   = sj['%s%s%s%s_%s' % ('cheekDown', oriPrefix, keyPrefix, 'RGT', suffix)]

        # NOSE RGT
        self.nostrilRGT = sj['%s%s%s%s_%s' % ('nostril', oriPrefix, keyPrefix, 'RGT', suffix)]

        # LIP RGT
        self.lipUp01RGT    = sj['%s%s%s%s_%s' % ('lipUp01', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.lipUp02RGT    = sj['%s%s%s%s_%s' % ('lipUp02', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.lipDown01RGT  = sj['%s%s%s%s_%s' % ('lipDown01', oriPrefix, keyPrefix, 'RGT', suffix)]
        self.lipDown02RGT  = sj['%s%s%s%s_%s' % ('lipDown02', oriPrefix, keyPrefix, 'RGT', suffix)]

        self.lipCornerRGT    = sj['%s%s%s%s_%s' % ('lipCorner', oriPrefix, keyPrefix, 'RGT', suffix)]

        # EYEBALL
        self.eyeballLFT = sj['%s%s%s%s_%s' % ('eyeball', oriPrefix, keyPrefix, 'LFT', suffix)]
        self.eyeballRGT = sj['%s%s%s%s_%s' % ('eyeball', oriPrefix, keyPrefix, 'RGT', suffix)]


        # mc.parent(self.neck, 'tmpJnt_grp')
