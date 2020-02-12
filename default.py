# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcaddon

if sys.version_info >= (2, 7):
    import json
else:
    import simplejson as json

# Import the common settings
from resources.lib.settings import log

ADDON = xbmcaddon.Addon(id='screensaver.auramod')
CWD = ADDON.getAddonInfo('path').decode("utf-8")


# Monitor class to handle events like the screensaver deactivating
class ScreensaverExitMonitor(xbmc.Monitor):
    def __init__(self):
        self.stopScreensaver = False

    # Called when the screensaver should be stopped
    def onScreensaverDeactivated(self):
        log("Deactivate Screensaver")
        self.stopScreensaver = True

    def onScreensaverActivated(self):
        log("Activate Screensaver")
        self.stopScreensaver = False

    def isStopScreensaver(self):
        return self.stopScreensaver


##################################
# Main of the AuraMod Screensaver
##################################
if __name__ == '__main__':
    log("AuraModScreen Starting %s" % ADDON.getAddonInfo('version'))

    # Start the monitor so we can see when the screensaver quits
    exitMon = ScreensaverExitMonitor()

    # Do something to stop the screensaver and see if we need to navigate
    # to the Auramod screensaver xml, or if it is already showing

    # A bit of a hack, but we need Kodi to think a user is "doing things" so
    # that itstops the screensaver, so we just send the message
    # to open the Context menu - which in our case will do nothing
    # but it does make Kodi think the user has done something
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Input.ContextMenu", "id": 1}')

    # Limit the maximum amount of time to wait for the screensaver to end
    maxWait = 30
    while (not exitMon.isStopScreensaver()) and (maxWait > 0):
        log("AuraModScreen: still running initial screensaver, waiting for stop")
        xbmc.sleep(100)
        maxWait = maxWait - 1

    del exitMon
    log("AuraModScreen: Initial screensaver stopped")

    # Now it is safe to check to see if the Auramod screensaver is showing
    # If we checked before the screensaver was stopped then it would think
    # the active window was the screensaver, rather than the auramod screensaver xml
    backRequired = 'true'
    if not xbmc.getCondVisibility("Window.IsVisible(1166)"):
        log("AuraModScreen: Navigating to Auramod screensaver xml")

        # Load the screensaver window
        xbmc.executebuiltin("ActivateWindow(1166)", True)
    else:
        log("AuraModScreen: Auramod Screensaver already active")
        backRequired = 'false'

    # Give a little bit of time for everything to shake out before starting the screensaver
    # waiting another few seconds to start a screensaver is not going to make a difference
    # to the user
    maxWait = 30
    while (not xbmc.abortRequested) and (not xbmc.getCondVisibility("Window.IsVisible(1166)")) and (maxWait > 0):
        log("AuraModScreen: waiting for Auramod screensaver xml to load")
        xbmc.sleep(100)
        maxWait = maxWait - 1

    xbmc.executebuiltin('RunScript(%s,%s)' % (os.path.join(CWD, "monitor.py"), backRequired))

    log("AuraModScreen Finished")
