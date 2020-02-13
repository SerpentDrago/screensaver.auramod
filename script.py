# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

import os
import sys

_addon = xbmcaddon.Addon()
_id = _addon.getAddonInfo('id').decode('utf-8')
_path = _addon.getAddonInfo('path').decode('utf-8')
_skin = os.path.basename(
            os.path.normpath(xbmc.translatePath('special://skin/')))
_xml = 'Custom_Screensaver_1166.xml'
    

def get_params():
    for arg in sys.argv:
        if arg == 'script.py':
            pass
        elif '=' in arg:
            arg_split = arg.split('=', 1)
            if arg_split[0] and arg_split[1]:
                return arg_split


if __name__ == '__main__':
    if get_params() == ['mode', 'choose']:
        call = ('RunScript(script.skinshortcuts,'
                'type=widgets'
                '&showNone=False'
                '&skinWidgetName=screensaver.auramod.name'
                '&skinWidgetPath=screensaver.auramod.path)')
        xbmc.executebuiltin(call, wait=True)
        
    if get_params() == ['mode', 'tvchoose']:
        call = ('RunScript(script.skinshortcuts,'
                'type=widgets'
                '&showNone=False'
                '&skinWidgetName=screensaver.auramod.tvname'
                '&skinWidgetPath=screensaver.auramod.tvpath)')
        xbmc.executebuiltin(call, wait=True)

        name = xbmc.getInfoLabel('Skin.String(screensaver.auramod.name')
        _addon.setSettingString('screensaver.auramod.name', name)

        tvname = xbmc.getInfoLabel('Skin.String(screensaver.auramod.tvname')
        _addon.setSettingString('screensaver.auramod.tvname', tvname)

