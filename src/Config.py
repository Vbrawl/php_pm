import os, sys

app_name = "PHPPM"

if os.name == "nt":
    appdata = os.getenv("APPDATA")
    if appdata is None:
        appdata = "C:\\ProgramData"
    app_directory = os.path.join(appdata, app_name)
elif os.getenv("TERMUX_VERSION", None) is not None:
    app_directory = os.path.join("/data/data/com.termux/files/usr/etc", app_name)
else:
    app_directory = os.path.join("/etc", app_name)

if not os.path.exists(app_directory):
    os.mkdir(app_directory)



class Config:
    library_path = os.path.join(app_directory, "pm_library")

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
