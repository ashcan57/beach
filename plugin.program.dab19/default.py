import xbmcgui
import xbmc
import urllib.request

BUILD_URL = "https://raw.githubusercontent.com/ashcan57/beach/main/builds/dab19.zip"

def main():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("DAB19 Build", "Download and install dab19.zip?"):
        path = xbmc.translatePath("special://home/addons/packages/dab19.zip")
        urllib.request.urlretrieve(BUILD_URL, path)
        xbmc.executebuiltin(f"InstallAddon({path})")
        dialog.ok("DAB19", "Installation triggered.")
    else:
        dialog.ok("DAB19", "Cancelled.")

if __name__ == "__main__":
    main()
