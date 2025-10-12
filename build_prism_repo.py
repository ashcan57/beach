import os
import zipfile
import hashlib

# ===== CONFIGURATION =====
PROVIDER = "ashcan57"
REPO_ID = "repository.prism"
REPO_NAME = "Prism Repository"
ADDON_ID = "Dropbox.downloader"
ADDON_NAME = "Dropbox Downloader Wizard"
DROPBOX_URL = "https://www.dropbox.com/scl/fi/90rsb9oal9dc3fp3g1l8s/dab19.zip?rlkey=5st59x4bq5xpvljnf0rlflu1z&st=6jxh74dy&dl=1"

# ===== PATHS =====
root_dir = os.path.join(os.getcwd(), REPO_ID)
version_file = os.path.join(root_dir, "version.txt")
addon_dir = os.path.join(root_dir, ADDON_ID)
repo_subdir = os.path.join(root_dir, REPO_ID)
zips_dir = os.path.join(root_dir, "zips", ADDON_ID)

# ===== AUTO-INCREMENT VERSION =====
if not os.path.exists(root_dir):
    os.makedirs(root_dir, exist_ok=True)

if os.path.exists(version_file):
    with open(version_file, "r") as f:
        last_version = f.read().strip()
    major, minor, patch = map(int, last_version.split("."))
    patch += 1
else:
    major, minor, patch = 1, 0, 0  # starting version

VERSION = f"{major}.{minor}.{patch}"

with open(version_file, "w") as f:
    f.write(VERSION)

print(f"📦 Building version: {VERSION}")

# ===== CREATE DIRECTORIES =====
for d in [addon_dir, repo_subdir, zips_dir, os.path.join(addon_dir, "resources")]:
    os.makedirs(d, exist_ok=True)

# ===== 1. repository.prism/addon.xml =====
repo_addon_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<addon id="{REPO_ID}"
       name="{REPO_NAME}"
       version="{VERSION}"
       provider-name="{PROVIDER}">

    <extension point="xbmc.addon.repository"
               name="{REPO_NAME}">
        <dir>
            <info>https://raw.githubusercontent.com/{PROVIDER}/prism/main/addons.xml</info>
            <checksum>https://raw.githubusercontent.com/{PROVIDER}/prism/main/addons.xml.md5</checksum>
            <datadir zip="true">https://raw.githubusercontent.com/{PROVIDER}/prism/main/zips/</datadir>
        </dir>
    </extension>

    <requires>
        <import addon="xbmc.addon" version="12.0.0"/>
    </requires>

    <summary>{REPO_NAME}</summary>
    <description>Official repository for {ADDON_NAME} by {PROVIDER}.</description>
    <platform>all</platform>
</addon>
"""
with open(os.path.join(repo_subdir, "addon.xml"), "w", encoding="utf-8") as f:
    f.write(repo_addon_xml)

# ===== 2. Dropbox.downloader/addon.xml =====
addon_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<addon id="{ADDON_ID}"
       name="{ADDON_NAME}"
       version="{VERSION}"
       provider-name="{PROVIDER}">

    <extension point="xbmc.python.script" library="main.py">
        <provides>executable</provides>
    </extension>

    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
    </requires>

    <summary>{ADDON_NAME}</summary>
    <description>Downloads and extracts the dab19.zip build from Dropbox directly into Kodi.</description>
    <platform>all</platform>
</addon>
"""
with open(os.path.join(addon_dir, "addon.xml"), "w", encoding="utf-8") as f:
    f.write(addon_xml)

# ===== 3. Dropbox.downloader/main.py =====
main_py = f"""import xbmc
import xbmcgui
import xbmcaddon
import urllib.request
import zipfile
import os

addon = xbmcaddon.Addon()
addon_path = xbmc.translatePath(addon.getAddonInfo('path'))
zip_path = os.path.join(addon_path, "dab19.zip")

url = "{DROPBOX_URL}"

dialog = xbmcgui.Dialog()
dialog.notification("Dropbox Downloader", "Downloading dab19.zip...", xbmcgui.NOTIFICATION_INFO, 3000)

try:
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(xbmc.translatePath("special://home/"))
    dialog.notification("Dropbox Downloader", "Build installed successfully!", xbmcgui.NOTIFICATION_INFO, 5000)
except Exception as e:
    dialog.notification("Dropbox Downloader", f"Error: {{e}}", xbmcgui.NOTIFICATION_ERROR, 5000)
"""
with open(os.path.join(addon_dir, "main.py"), "w", encoding="utf-8") as f:
    f.write(main_py)

# ===== 4. Root addons.xml =====
addons_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<addons>
    <addon id="{ADDON_ID}"
           name="{ADDON_NAME}"
           version="{VERSION}"
           provider-name="{PROVIDER}">

        <extension point="xbmc.python.script" library="main.py">
            <provides>executable</provides>
        </extension>

        <requires>
            <import addon="xbmc.python" version="3.0.0"/>
        </requires>

        <summary>{ADDON_NAME}</summary>
        <description>Downloads and extracts the dab19.zip build from Dropbox directly into Kodi.</description>
        <platform>all</platform>
    </addon>
</addons>
"""
addons_xml_path = os.path.join(root_dir, "addons.xml")
with open(addons_xml_path, "w", encoding="utf-8") as f:
    f.write(addons_xml)

# ===== 5. addons.xml.md5 =====
md5_hash = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
with open(os.path.join(root_dir, "addons.xml.md5"), "w", encoding="utf-8") as f:
    f.write(md5_hash)

# ===== 6. Zip the Dropbox.downloader addon =====
zip_path = os.path.join(zips_dir, f"{ADDON_ID}-{VERSION}.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, _, filenames in os.walk(addon_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, os.path.dirname(addon_dir))
            zipf.write(file_path, arcname)

# ===== 7. Create repository.prism.zip =====
repo_zip_path = os.path.join(root_dir, f"{REPO_ID}-{VERSION}.zip")
with zipfile.ZipFile(repo_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".zip") and filename != f"{REPO_ID}-{VERSION}.zip":
                continue
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, os.path.dirname(root_dir))
            zipf.write(file_path, arcname)

print("\n✅ Build complete!")
print(f"Version: {VERSION}")
print(f"Dropbox.downloader ZIP: {zip_path}")
print(f"Repository ZIP: {repo_zip_path}")
print(f"Folder ready for GitHub: {root_dir}")

