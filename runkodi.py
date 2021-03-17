import subprocess
import time
import pathlib
import logging
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def RunKodi(KodiDir):
    KodiCmd = [str(KodiDir / 'kodi.exe'), '-p']
    return subprocess.Popen(KodiCmd)


def StartKodi(cls):
    logger.debug("StartKodi starting")
#    KodiDir = SetupKodi(cls)
    KodiDir = pathlib.Path('.')
    cls.KodiProc = RunKodi(KodiDir)
    logger.debug("RunKodi: %s", cls.KodiProc.poll())
    #ssdp.waitForDevice(id=UUID[cls.Version][cls.Bitness])
    time.sleep(10)
    #cls.Kodi = ConnectKodi()
    logger.debug("StartKodi ending")


def StopKodi(cls):
    cls.KodiProc.terminate()
    cls.KodiProc.wait()

class base():
    pass

cls = base()

StartKodi(cls)
time.sleep(10)
StopKodi(cls)
