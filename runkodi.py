import subprocess
import time
import pathlib
import logging
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def SetupKodi(cls):
    logger.debug("SetupKodi starting")
'''
    Version = cls.Version
    Bitness = cls.Bitness
    KodiInfo = cls.KodiInfo
    URL = KodiInfo['build'][Bitness]['URL']

    #KodiDir = SetupDir / f'Kodi{Version}_{Bitness}'
    KodiDir = SetupDir / 'Kodi{0}_{1}'.format(Version, Bitness)
    filename = CacheDir / pathlib.Path(urlparse(URL).path).name
    if not filename.exists():
        response = requests.get(URL)
        filename.write_bytes(response.content)
        del response

    dstdir = KodiDir / 'portable_data'
    #if not dstdir.exists():
    if not KodiDir.exists():
        #SevenZip = ['7z.exe', 'x', '-y', str(filename), f'-o{KodiDir}']
        SevenZip = ['7z.exe', 'x', '-y', str(filename), '-o{KodiDir}'.format(KodiDir=KodiDir)]
        #proc = subprocess.run(SevenZip, stdout=subprocess.PIPE)
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
        #dstdir.write_text(str(guisettings), 'utf-8')
        try:
            dstdir.write_text(unicode(guisettings), 'utf-8')
        except NameError:
            dstdir.write_text(str(guisettings), 'utf-8')

    #dstdir = KodiDir / 'portable_data' / r"userdata\upnpserver.xml"
    dstdir = KodiDir / 'portable_data' / "userdata/upnpserver.xml"
    if not dstdir.exists():
    #      upnpserver =  f"""\
#  <upnpserver>
    #  <UUIDRenderer>{UUID[Version][Bitness]}</UUIDRenderer>
#  </upnpserver>
#  """
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

'''
    logger.debug("SetupKodi ending")
    return pathlib.Path('.')
    return KodiDir


def RunKodi(KodiDir):
    KodiCmd = [str(KodiDir / 'kodi.exe'), '-p']
    return subprocess.Popen(KodiCmd)


def StartKodi(cls):
    logger.debug("StartKodi starting")
    KodiDir = SetupKodi(cls)
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
