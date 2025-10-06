import xbmcgui
import xbmc
import urllib.request

BUILD_URL = "https://www.dropbox.com/scl/fo/ko8c3abxbtyukuovirrxv/ANA9nB2VxHjZQxMeJKigkio?rlkey=kg14lw8x139u6co9pj515msqp&st=jua9t5o4&dl=1"

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
