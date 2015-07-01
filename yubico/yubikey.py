"""
module for accessing a YubiKey

In an attempt to support any future versions of the YubiKey which
might not be USB HID devices, you should always use the yubikey.find_key()
(or better yet, yubico.find_yubikey()) function to initialize
communication with YubiKeys.

Example usage (if using this module directly, see base module yubico) :

    import yubico.yubikey

    try:
        YK = yubico.yubikey.find_key()
        print "Version : %s " % YK.version()
    except yubico.yubico_exception.YubicoError as inst:
        print "ERROR: %s" % inst.reason
"""
# Copyright (c) 2010, 2011, 2012 Yubico AB
# See the file COPYING for licence statement.

__all__ = [
    # constants
    'RESP_TIMEOUT_WAIT_FLAG',
    'RESP_PENDING_FLAG',
    'SLOT_WRITE_FLAG',
    # functions
    'find_key',
    # classes
    'YubiKey',
    'YubiKeyTimeout',
]

from .yubico_version  import __version__
from .yubikey_base import YubiKeyError, YubiKeyTimeout, YubiKeyVersionError, YubiKeyCapabilities, YubiKey
from .yubikey_usb_hid import YubiKeyUSBHID, YubiKeyUSBHIDError
from .yubikey_neo_usb_hid import YubiKeyNEO_USBHID, YubiKeyNEO_USBHIDError

def find_key(debug=False, skip=0):
    """
    Locate a connected YubiKey. Throws an exception if none is found.

    This function is supposed to be possible to extend if any other YubiKeys
    appear in the future.

    Attributes :
        skip  -- number of YubiKeys to skip
        debug -- True or False
    """
    try:
        YK = YubiKeyUSBHID(debug=debug, skip=skip)
        if (YK.version_num() >= (2, 1, 4,)) and \
                (YK.version_num() <= (2, 1, 9,)):
            # YubiKey NEO BETA, re-detect
            YK2 = YubiKeyNEO_USBHID(debug=debug, skip=skip)
            if YK2.version_num() == YK.version_num():
                # XXX not guaranteed to be the same one I guess
                return YK2
            raise YubiKeyError('Found YubiKey NEO BETA, but failed on rescan.')
        return YK
    except YubiKeyUSBHIDError as inst:
        if 'No USB YubiKey found' in str(inst):
            # generalize this error
            raise YubiKeyError('No YubiKey found')
        else:
            raise
