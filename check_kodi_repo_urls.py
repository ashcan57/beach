import urllib.request

# ===== CONFIGURATION =====
PROVIDER = "ashcan57"
REPO = "prism"
BRANCH = "main"
ADDON_ID = "Dropbox.downloader"

urls = {
    "addons.xml": f"https://raw.githubusercontent.com/{PROVIDER}/{REPO}/{BRANCH}/addons.xml",
    "addons.xml.md5": f"https://raw.githubusercontent.com/{PROVIDER}/{REPO}/{BRANCH}/addons.xml.md5",
    "Dropbox.downloader zip": f"https://raw.githubusercontent.com/{PROVIDER}/{REPO}/{BRANCH}/zips/{ADDON_ID}/{ADDON_ID}-1.0.0.zip"
}

print("🔎 Checking Kodi repo URLs...\n")

for name, url in urls.items():
    try:
        with urllib.request.urlopen(url) as response:
            code = response.getcode()
            if code == 200:
                print(f"✅ {name} reachable: {url}")
            else:
                print(f"❌ {name} returned status code {code}: {url}")
    except Exception as e:
        print(f"❌ {name} FAILED to connect: {url}\n   Error: {e}")

print("\n🎯 Check complete. If any URL failed, fix the repo path or network connection.")
