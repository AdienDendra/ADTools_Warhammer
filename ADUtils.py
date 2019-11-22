import re
from string import digits

# CONTROL FUNCTION
SUFFIXES = {
    'mesh' : 'geo',
    'joint' : 'jnt',
    'follicle' : 'fol',
    'nurbsCurve' : 'crv',
    'camera' : None

}
GROUP = 'grp'
GIMBAL = 'Gmbl'

import maya.cmds as mc
import pymel.core as pm


def scaleCrv(sizeObj, shape):
    scaleShp = [[sizeObj * i for i in j] for j in shape]
    return scaleShp

def controller(shape):
    createCrv = mc.curve(d=1, p=shape)
    return createCrv

def prefixName(obj):
    if '_' in obj:
        getPrefN = obj.split('_')[0]
        return getPrefN
    else:
        return obj

def groupParent(groups, prefix, suffix, number='', side=''):
    # create group hierarchy
    grps = []
    for i in range(len(groups)):
        grps.append(mc.createNode('transform', n="%s%s%s%s%s_%s" % (prefix, suffix, groups[i], number, side, GROUP)))

        if i > 0:
            parentObj(grps[i-1], grps[i])

    return grps

def suffixName(obj):
    objs = obj.split('|')[-1:]
    for l in objs:
        getLen = l.split('_')
        if len(getLen) > 1:
            getSufN = getLen[1]
            return getSufN
        else:
            getSufNo = l.replace(l,'')

            return getSufNo
def parentCons(objBase, objTgt, mOffset = 1):
    parCons = mc.parentConstraint(objBase, objTgt, mo=mOffset)
    return parCons

def orientCons(objBase, objTgt, mOffset = 1):
    oriCons = mc.orientConstraint(objBase, objTgt, mo=mOffset)
    return oriCons

def pointCons(objBase, objTgt, mOffset = 1):
    pntCons = mc.pointConstraint(objBase, objTgt, mo=mOffset)
    return pntCons

def scaleCons(objBase, objTgt, mOffset = 1):
    scaleCons = mc.scaleConstraint(objBase, objTgt, mo=mOffset)
    return scaleCons

def matchPosition(objBase, objTgt):
    mc.delete(parentCons(objBase, objTgt, mOffset=0))

def matchScale(objBase, objTgt):
    mc.delete(scaleCons(objBase, objTgt, mOffset=0))

def groupObject(grpOffsetNameLs, objBase, matchPos=None, side=''):
    lR = mc.listRelatives(objBase, ap=1)

    cGrp = groupParent(grpOffsetNameLs, '%s' % prefixName(objBase), suffixName(objBase).title(), side)

    if matchPos:
        matchPosition(matchPos, cGrp[0])
        matchScale(matchPos, cGrp[0])

    if lR == None:
        parentObj(cGrp[-1], objBase)
    else:
        # parent group offset to list relatives
        parentObj(lR, cGrp[0])
        # parent obj to grp offset
        parentObj(cGrp[-1], objBase)

    return cGrp

def parentObj (objBase, objTgt):
    parObj = mc.parent(objTgt,objBase)
    return parObj

def setColor(ctrl, color):
    colorDic = {
    # 'gray': 0,
    # 'black': 1,
    # 'darkGray': 2,
    # 'lightGray': 3,
    'darkRed' : 4,
    # 'darkBlue' : 5,
    'blue' : 6,
    # 'darkGreen' : 7,
    # 'darkPurple' : 8,
    # 'purple' : 9,
    'brown' : 10,
    # 'darkBrown' : 11,
    # 'dullRed' : 12,
    'red' : 13,
    # 'green' : 14,
    'navy' : 15,
    'white': 16,
    'yellow' : 17,
    'turquoiseBlue' : 18,
    'turquoiseGreen' : 19,
    'lightPink' : 20,
    # 'lightBrown' :21,
    # 'lightYellow' :22,
    # 'dullGreen' : 23,
    # 'chocholate' : 24,
    # 'dullYellow' : 25,
    # 'greenYellow' : 26,
    # 'greenBlue' : 27,
    # 'blueGreen' : 28,
    'lightNavy' : 29,
    # 'violet' : 30,
    'ruby' :31
    }
    if color in colorDic.keys():
        ctrlSColor = mc.listRelatives(ctrl, s=1)[0]
        mc.setAttr(ctrlSColor + '.ove', 1)
        mc.setAttr(ctrlSColor + '.ovc', colorDic[color])
        return ctrlSColor
    else:
        return mc.warning("Could not find %s name color. Please check color name!" % color)

def connectAttrTrans(objBase, objTgt):
    lR = mc.listRelatives(objTgt, ap=1)
    if lR == True:
        tAttr = mc.connectAttr(objBase + '.translate', lR + '.translate')
    else:
        tAttr = mc.connectAttr(objBase + '.translate', objTgt + '.translate')
    return tAttr

def connectAttrRot(objBase, objTgt):
    lR = mc.listRelatives(objTgt, ap=1)
    if lR == True:
        rAttr = mc.connectAttr(objBase + '.rotate', lR + '.rotate')
    else:
        rAttr = mc.connectAttr(objBase + '.rotate', objTgt + '.rotate')
    return rAttr

def connectAttrScale(objBase, objTgt):
    lR = mc.listRelatives(objTgt, ap=1)
    if lR == True:
        sAttr = mc.connectAttr(objBase + '.scaleX', lR + '.scaleX')
        sAttr = mc.connectAttr(objBase + '.scaleY', lR + '.scaleY')
        sAttr = mc.connectAttr(objBase + '.scaleZ', lR + '.scaleZ')

    else:
        sAttr = mc.connectAttr(objBase + '.scaleX', objTgt + '.scaleX')
        sAttr = mc.connectAttr(objBase + '.scaleY', objTgt + '.scaleY')
        sAttr = mc.connectAttr(objBase + '.scaleZ', objTgt + '.scaleZ')
    return sAttr

def connectAttrObject(objBase, objTgt):
    connectAttrTrans(objBase, objTgt)
    connectAttrRot(objBase, objTgt)
    connectAttrScale(objBase, objTgt)

def addAttrConfShp(obj, attrName, at, k=False, e=False, cb=False, **kwargs):
    if mc.nodeType(obj) == "transform":
        try:
            namelR    = mc.listRelatives(obj, shapes=True)[0]
            mc.addAttr(namelR, ln=attrName, at=at, **kwargs)
            mc.setAttr('%s.%s' %(namelR, attrName), e=e, k=k, cb=cb)
            return namelR
        except IndexError:
            return mc.warning("Could not find shape in %s" % obj)
    else:
        return
# GENERAL FUNCTION: ADD ATTRIBUTE(S) ON MULTIPLE OBJECTS
def addAttribute(objects=[], longName='', niceName='', separator=False, k=False, cb=False, **kwargs):
    # For each object
    for obj in objects:
        # For each attribute
        for x in range(0, len(longName)):
            # See if a niceName was defined
            attrNice = '' if not niceName else niceName[x]
            # If the attribute does not exists
            if not mc.attributeQuery(longName[x], node=obj, exists=True):
                # Add the attribute
                mc.addAttr(obj, longName=longName[x], niceName=attrNice, **kwargs)
                # If lock was set to True
                mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb) if separator else mc.setAttr((obj + '.' + longName[x]), k=k, e=1, cb=cb)
    return longName[0]

def connectAttrTransRot(objBase, objTgt):
    connectAttrTrans(objBase, objTgt)
    connectAttrRot(objBase, objTgt)

def lockHideAttr(lockChnl, ctrl):
    attrLockList = []
    for lockChannel in lockChnl:
        if lockChannel in ['t', 'r', 's']:
            for axis in ['x', 'y', 'z']:
                at = lockChannel + axis
                attrLockList.append(at)
        else:
            attrLockList.append(lockChannel)
    for at in attrLockList:
        mc.setAttr(ctrl + '.' + at, l=1, k=0)
    return attrLockList

def lockHideAttrObj(obj, attrName):
    mc.setAttr('%s.%s' % (obj, attrName), l=True, k=False )

def connectMatrixAll(objBase, objTgt):
    dMtx = connectMatrix(objBase, objTgt)
    mc.connectAttr(dMtx + '.outputTranslate', objTgt+'.translate')
    mc.connectAttr(dMtx + '.outputRotate', objTgt + '.rotate')
    mc.connectAttr(dMtx + '.outputScale', objTgt + '.scale')

def connectMatrix(objBase, objTgt):
    listR = mc.listRelatives(objBase, f=1, ap=1)[0]
    split = listR.split('|')
    firstParent = filter(None, split)[0]

    pref = prefixName(objTgt)
    multMtx = mc.createNode('multMatrix', n=pref + '_mmtx')

    dMtx = mc.createNode('decomposeMatrix', n=pref + '_dmtx')

    mc.connectAttr(objBase + '.worldMatrix[0]', multMtx + '.matrixIn[0]')
    mc.connectAttr(firstParent + '.worldInverseMatrix[0]', multMtx + '.matrixIn[1]')

    mc.connectAttr(multMtx + '.matrixSum', dMtx + '.inputMatrix')

    return dMtx

def connection (connect, ctrl, obj):
    dic = {'parentCons': parentCons,
           'pointCons': pointCons,
           'orientCons': orientCons,
           'scaleCons': scaleCons,
           'parent': parentObj,
           'connectAttr' : connectAttrObject,
           'connectTrans' : connectAttrTrans,
           'connectOrient' : connectAttrRot,
           'connectScale' : connectAttrScale,
           'connectMatrixAll': connectMatrixAll,
           }
    rs={}
    for con in connect:
        if con in dic.keys():
            rs[con] = dic[con](ctrl, obj)
        else:
           return mc.error("Your %s key name is wrong. Please check on the key list connection!" % con)
    return rs

def duplicateAndRename(objDuplicate='', valuePrefix='', keyPrefix='',
                       suffix='', selection=False, **kwargs):
    listRename=[]
    listRenameOri =[]
    if selection:
        selectObj = mc.ls(sl=1)
        duplicate = mc.duplicate(selectObj, rc=True)
        for i in duplicate:
            renameOri = mc.rename(i, '%s%s_%s' % (prefixName(i), keyPrefix, suffix))
            rename = mc.rename(renameOri, '%s%s_%s' % (prefixName(i), valuePrefix, suffix))
            listRename.append(rename)
            listRenameOri.append(renameOri)
    else:
        duplicate = mc.duplicate(objDuplicate, rc=True)
        for i in duplicate:
            replaceTmp = i.replace('Tmp', keyPrefix)
            renameOri = mc.rename(i, '%s_%s' % (prefixName(replaceTmp), suffix))

            replaceKeyPrefix = renameOri.replace(keyPrefix, valuePrefix)
            rename = mc.rename(renameOri, replaceKeyPrefix)

            listRename.append(rename)
            listRenameOri.append(renameOri)

    return listRenameOri, listRename

def listSkeletonDic(objDuplicate='', valuePrefix='', keyPrefix='',  suffix='', selection=False, **kwargs):
    dic = {}
    listName = duplicateAndRename(objDuplicate=objDuplicate, valuePrefix=valuePrefix, keyPrefix=keyPrefix,
                                    suffix=suffix, selection=selection, kwargs=kwargs)
    listKeys = listName[0]
    listValue = listName[1]

    appendList = []
    for listKeys, listValue in zip(listKeys, listValue):
        allList = [listKeys, listValue]
        appendList.append(allList)

    for i in appendList:
        listKeys  = i[0]
        listValue = i[1]
        dic[listKeys] = listValue

    return dic



def createParentTransform(listparent, object, matchPos, prefix, suffix, side=''):
    lR = mc.listRelatives(object, ap=1)
    try:
        patterns = [r'\d+']
        prefixNumber = prefixName(prefix)
        for p in patterns:
            prefixNumber = re.findall(p, prefixNumber)[0]
    except:
        prefixNumber = ''
    # get the prefix without number
    prefixNoNumber = str(prefix).translate(None, digits)

    if side in prefixNoNumber:
        prefixNewName = prefixNoNumber.replace(side, '')
    else:
        prefixNewName = prefixNoNumber

    cGrp = groupParent(groups=listparent, prefix= prefixName(prefixNewName), number=prefixNumber,
                          suffix=suffixName(suffix).title(),
                              side=side)

    if matchPos:
        matchPosition(matchPos, cGrp[0])
        matchScale(matchPos, cGrp[0])

    if lR == None:
        parentObj(cGrp[-1], object)
    else:
        # parent group offset to list relatives
        parentObj(lR, cGrp[0])
        # parent obj to grp offset
        parentObj(cGrp[-1], object)

    return cGrp