import urllib.request
import shutil
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
import platform

def create(d):
    path = Path(d["name"])
    # print("Creating", str(path))
    Path(path.parent).mkdir(parents=True, exist_ok=True)
    with open(d["name"], "wb") as f:
        c = d["contents"].strip()
        i = 0
        while i < len(c):
            if c[i] in "0123456789ABCDEFabcdef":
                assert c[i+1] in "0123456789ABCDEFabcdef"
                k = c[i:i+2]
                f.write(bytes([int(k, base=16)]))
                i += 2
            else:
                i += 1

def install():
    root = ET.parse("archive.xml").getroot()
    version = root.attrib["version"]
    print("Installing version %s"%version)
    for file in root:
        assert file.tag == "file", elem.tag
        d = {}
        for child in file:
            assert child.tag in { "name", "contents" }, child.tag
            d[child.tag] = child.text.strip()
        create(d)
    fl = Path("harmony")
    fl.chmod(0o755)
    print("Compiling model checker...")
    ec = os.system("gcc -O3 -std=c99 -DNDEBUG charm.c -m64 -o charm.exe -lpthread")
    if ec != 0 or not os.path.exists("charm.exe"):
        exe = "charm." + platform.system() + ".exe"
        if os.path.exists(exe):
            ec = os.system(exe + " -x")
            if ec == 0:
                shutil.copyfile(exe, "charm.exe")
    if not os.path.exists("charm.exe"):
        print("  Failed to compile the model checker (using gcc)")
        print("  Please compile charm.c and put the result in charm.exe")
        print("  Use a 64-bit C (C99) compiler")
        print("  Use the following compilation flags: -std=c99 -DNDEBUG -m64 -lpthread")

def check():
    url = urllib.request.urlopen('https://harmony.cs.cornell.edu/version.xml')
    remote = ET.parse(url).getroot()
    rv = remote.attrib["version"]
    local = ET.parse("archive.xml").getroot()
    lv = local.attrib["version"]
    print("Local version:", lv)
    print("Remote version:", rv)

def update():
    print("Downloading the latest version...")
    with urllib.request.urlopen("https://harmony.cs.cornell.edu/archive.xml") as c, open("archive.xml", 'wb') as f:
        shutil.copyfileobj(c, f)
    install()
    sys.exit(0)

if len(sys.argv) == 1:
    file = Path("archive.xml")
    if file.exists():
        install()
    else:
        update()
    print("Install complete")
    sys.exit(0)

if sys.argv[1] == "--reinstall":
    install()
    print("Reinstall complete")
    sys.exit(0)

if sys.argv[1] == "--check":
    check()
    sys.exit(0)

if sys.argv[1] == "--update":
    update()
    print("Update complete")
    sys.exit(0)

if sys.argv[1] == "--version":
    os.system("./harmony -v")
    sys.exit(0)

if sys.argv[1] != "--help":
    print("Unknown option", sys.argv[1])

print("Usage:", sys.argv[0], "[command]")
print("""
   where command is one of:
       <empty>:     basic installation
       --reinstall: install again
       --update:    download and install latest version
       --version:   print version number
       --check:     check for updates
""")
