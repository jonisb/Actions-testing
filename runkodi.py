import socket
import subprocess
import time
import requests
from bs4 import BeautifulSoup
import pathlib
import logging
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)
from jsbc.compat.urllib.urlparse import urlparse
from jsbc.Toolbox import DefaultSettings, settings
from jsbc import KodiLib
#from jsbc.KodiLib import jsonrpc
from jsbc.KodiLib.KodiInfo import KodiInfo

settingsDefaults = [
    ('client', [
        ('name', 'KodiLib.testing'),
        ('network', [
            ('jsonrpc', [
                ('enabled', False),
                ('buffersize', 4096),
                ('timeout', 1),
                ('retrys', 10),
                ('notifications', [
                    ('enabled', False),
                ]),
            ]),
        ]),
    ]),
    ('server', [
        ('network', [
            ('tcp', [
                ('port', 9090)
            ]),
        ]),
    ]),
    ('servers', [
        (str, []),
    ]),
]


def SetupKodi(cls):
    logger.debug("SetupKodi starting")
    Version = cls.Version
    Bitness = cls.Bitness
    KodiInfo = cls.KodiInfo
    URL = KodiInfo['build'][Bitness]['URL']
    KodiDir = SetupDir / 'Kodi{0}_{1}'.format(Version, Bitness)
    filename = CacheDir / pathlib.Path(urlparse(URL).path).name
    if not filename.exists():
        response = requests.get(URL)
        filename.write_bytes(response.content)
        del response
    dstdir = KodiDir / 'portable_data'
    if not KodiDir.exists():
        SevenZip = ['7z.exe', 'x', '-y', str(filename), '-o{KodiDir}'.format(KodiDir=KodiDir)]
        proc = subprocess.call(SevenZip, stdout=subprocess.PIPE)
    logger.debug("SetupKodi KodiDir.exists() = %s", KodiDir.exists())
    dstdir = dstdir / r"userdata\guisettings.xml"
    if not dstdir.exists():
        dstdir.parent.mkdir(parents=True, exist_ok=True)
        guisettings =  """\
<settings>
    <general>
        <settinglevel>3</settinglevel>
    </general>
    <services>
        <upnprenderer>true</upnprenderer>
        <upnpannounce>false</upnpannounce>
        <webserver>true</webserver>
        <webserverauthentication>false</webserverauthentication>
    </services>
    <viewstates>
    </viewstates>
</settings>
"""
        guisettings = BeautifulSoup(guisettings, 'html.parser')
        if Version < 18:
            guisettings.settings.general.append(guisettings.new_tag("addonupdates"))
            guisettings.settings.general.addonupdates.string = str(2)
            guisettings.settings.services.append(guisettings.new_tag("esallinterfaces"))
            guisettings.settings.services.esallinterfaces.string = 'true'
        else:
            guisettings.settings['version'] = str(2)
            tag = guisettings.new_tag("setting")
            tag['id'] = "general.addonupdates"
            tag.string = str(2)
            guisettings.settings.append(tag)
            tag = guisettings.new_tag("setting")
            tag['id'] = "services.esallinterfaces"
            tag.string = 'true'
            guisettings.settings.append(tag)
            tag = guisettings.new_tag("setting")
            tag['id'] = "services.upnp"
            tag.string = 'true'
            guisettings.settings.append(tag)
        try:
            dstdir.write_text(unicode(guisettings), 'utf-8')
        except NameError:
            dstdir.write_text(str(guisettings), 'utf-8')
    dstdir = KodiDir / 'portable_data' / "userdata/upnpserver.xml"
    if not dstdir.exists():
        try:
            UUID[str(Version)]
        except KeyError:
            UUID[str(Version)] = {}

        try:
            UUID[str(Version)][Bitness]
        except KeyError:
            import uuid
            UUID[str(Version)][Bitness] = str(uuid.uuid4())
            settings.save()
        upnpserver =  """\
<upnpserver>
    <UUIDRenderer>{0}</UUIDRenderer>
</upnpserver>
""".format(UUID[str(Version)][Bitness])
        dstdir.write_text(upnpserver, 'utf-8')
    logger.debug("SetupKodi ending")

    return KodiDir


def RunKodi(KodiDir):
    KodiCmd = [str(KodiDir / 'kodi.exe'), '-p']
    return subprocess.Popen(KodiCmd)


def ConnectKodi():
    logger.debug("settings: %s", settings.export(True))
    #settings['client']['network']['jsonrpc']['enabled'] = True
    logger.debug("ConnectKodi starting")
    #Kodi = KodiLib.kodi()
    #Kodi.connect()
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.settimeout(30)
    try:
        _socket.connect(('127.0.0.1', 9090))
    except Exception:
        logger.exception('connect: %s, %s', '127.0.0.1', 9090)
        try:
            _socket.connect(('127.0.0.1', 8080))
        except Exception:
            logger.exception('connect: %s, %s', '127.0.0.1', 8080)
            raise
    logger.debug("ConnectKodi ending")
    return Kodi


def StartKodi(cls):
    logger.debug("StartKodi starting")
    KodiDir = SetupKodi(cls)
    cls.KodiProc = RunKodi(KodiDir)
    logger.debug("RunKodi: %s", cls.KodiProc.poll())
    #ssdp.waitForDevice(id=UUID[cls.Version][cls.Bitness])
    time.sleep(30)
    logger.debug("RunKodi: %s", cls.KodiProc.poll())
    cls.Kodi = ConnectKodi()
    logger.debug("RunKodi: %s", cls.KodiProc.poll())
    logger.debug("StartKodi ending")


def StopKodi(cls):
    cls.KodiProc.terminate()
    cls.KodiProc.wait()


class base():
    Version = 19
    Bitness = '64bit'
    KodiInfo = KodiInfo()[Version]


cls = base()

DefaultSettings(settingsDefaults)
UUID = settings['servers']
CacheDir = pathlib.Path('.')
SetupDir = CacheDir / "TestInstall"

StartKodi(cls)
time.sleep(10)
StopKodi(cls)
