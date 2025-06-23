import os
import sys 
import json

from . import Terminal as myTerminal

myTerminal.clearTerminal()

#group our preferences together in a directory
#to avoid conflicts with other applications
applicationNameRoot = "DNDG"

#give each application or code snippet a unique preferences file name
preferences_File = "Personal-Knowledge-Vault.json"

#empty preferences file
_exampleEmptyPreferences = {
    "pkv_root":"PKV", #root folder name of the personal knowledge vault
    "attachments_root":"_Attachments", #name of the folder in the PKV where attachments are stored
    "projects_root":"_Projects", #name of the folder in the PKV where projects are stored
    "archive_root":".Archive", #name of where soft deleted projects will be sent
    "timestamp_id_format":"%y%m%d%H%M%S", #format for note unique identifiers
    "date_format":"%Y-%m-%d", #format for displaying dates in notes
    "datetime_format":"%Y-%m-%d %H:%M:%S", #format for displaying date and time in notes
    "documents_path": "os default", #where documents are stored, use 'os default' to let the OS decide
    "attachmentPickUp_path": "os default", #where we can look for new attachment, use 'os default' to let the OS return the downloads folder
    "screenCapture_path": "os default", #where we can look for new screen captures, use 'os default' to let the OS return the screenshots folder
    "default_editor": "code" #default editor to use for opening files, can be 'code' for VS Code, 'zed' for Zed, or any other editor command
    }

_preferences = {}

# each OS might be saving preferences and docs in a different paths
preferences_Path = ""
os_documents_Path = ""
if sys.platform in ('linux', 'linux2',"darwin"):
    preferences_Path = os.path.expanduser('~/Library/Preferences/')
    os_documents_Path = os.path.expanduser('~/Documents')
elif sys.platform in ('win32','windows'):
    preferences_Path = os.path.join(os.environ['APPDATA'], 'Preferences')
    os_documents_Path = os.path.join(os.environ.get("USERPROFILE", ""), "Documents")
else:
    print(f"Unsupported platform: {sys.platform}")
    sys.exit(1)

# shared preferences
_pkv_baseFolderName = ""
_attachment_root = ""
_projects_root = ""
_archive_root = ""
_timestamp_id_format = ""
_datetime_format = ""
_date_format = ""
_documents_path = ""
_attachmentPickUp_path = ""
_screenCaptures_path = ""

def root_pkv() -> str:
    """Returns the documents subfolder for the pkv."""
    return os.path.join (_documents_path,_pkv_baseFolderName)

def root_attachments() -> str:
    """returns the attachments root."""
    return os.path.join(root_pkv(), _attachment_root)

def root_archive() -> str:
    """Returns soft delete location."""
    return os.path.join(root_pkv(),_archive_root)

def root_projects() -> str:
    """Returns the projects root."""
    return os.path.join(root_pkv(), _projects_root)

def timestamp_id_format() -> str:
    """Returns the timestamp format for IDs."""
    return _timestamp_id_format

def datetime_format() -> str:
    """Returns the datetime format for display."""
    return _datetime_format

def date_format() -> str:
    """Returns the date format for display."""
    return _date_format

def documents_path() -> str:
    """Returns the path to the documents directory."""
    return _documents_path

def attachmentPickUp_path() -> str:
    """Returns the path to the attachment pickup directory."""
    return _attachmentPickUp_path

def screenCapture_Path() -> str:
    """Returns the path to the attachment pickup directory."""
    return _screenCaptures_path

def default_editor() -> str:
    """Returns the default editor to use for opening files."""
    return _preferences.get("default_editor", "code")  # Default to 'code' if not set

def preferences() -> dict:
    """Returns the loaded preferences."""
    return _preferences

    
preferences_Path = os.path.join(preferences_Path, applicationNameRoot)
preferences_File_Path = os.path.join(preferences_Path, preferences_File)

if not os.path.exists(preferences_Path):
    print(f"Creating preferences directory at: {preferences_Path}")
    os.makedirs(preferences_Path)

if not os.path.exists(preferences_File_Path):
    print(f"\tCreating preferences file in: {preferences_Path}")
    with open(os.path.join(preferences_Path,preferences_File), 'w') as file:
        json.dump(_exampleEmptyPreferences, file, indent=4)

try:
    with open(preferences_File_Path, 'r') as file:
        _preferences = json.load(file)
        _pkv_baseFolderName = _preferences["pkv_root"]
        _attachment_root = _preferences["attachments_root"]
        _projects_root = _preferences["projects_root"]
        _archive_root = _preferences["archive_root"]
        _timestamp_id_format = _preferences["timestamp_id_format"]
        _datetime_format = _preferences["datetime_format"]
        _date_format = _preferences["date_format"]
        _documents_path = _preferences["documents_path"]
        if _documents_path == "os default":
            _documents_path = os_documents_Path
        
        
        _attachmentPickUp_path = _preferences["attachmentPickUp_path"]
        if _attachmentPickUp_path in ("os default",""):
            if sys.platform in ('linux', 'linux2', 'darwin'):
                _attachmentPickUp_path = os.path.expanduser('~/Downloads')
            elif sys.platform in ('win32', 'windows'):
                _attachmentPickUp_path = os.path.join(os.environ.get("USERPROFILE", ""), "Downloads")
            else:
                _attachmentPickUp_path = ""

        if not os.path.exists(_attachmentPickUp_path):
            print(f"""{myTerminal.ERROR}Attachment pickup path '{_attachmentPickUp_path}' does not exist, 
                  consider creating it or editing your preferences.{myTerminal.RESET} """)

        _screenCaptures_path = _preferences["screenCapture_path"]
        if _screenCaptures_path in ("os default",""):
            if sys.platform in ('linux', 'linux2', 'darwin'):
                _screenCaptures_path = os.path.expanduser('~/Pictures/ScreenShots')
            elif sys.platform in ('win32', 'windows'):
                _screenCaptures_path = os.path.join(os.environ.get("USERPROFILE", ""), "Pictures", "Screenshots")
            else:
                _screenCaptures_path = ""

        if not os.path.exists(_screenCaptures_path):
            print(f"""{myTerminal.ERROR}Screen capture pickup path '{_screenCaptures_path}' does not exist, 
                  consider creating it or editing your preferences.{myTerminal.RESET} """)
         
    #print(f"{len(_preferences)} preferences loaded successfully")

except Exception as e:
    print("Error loading preferences:", e)
    sys.exit(1)

try:
    if not os.path.exists(root_pkv()):
        print(f"Creating PKV root directory at: {root_pkv()}")
        os.makedirs(root_pkv())

    if not os.path.exists(root_projects()):
        print(f"Creating PKV project directory at: {root_projects()}")
        os.makedirs(root_projects())
    
    if not os.path.exists(root_attachments()):
        print(f"Creating PKV attachments directory at: {root_attachments()}")
        os.makedirs(root_attachments())

    if not os.path.exists(root_archive()):
        print(f"Creating PKV archive directory at: {root_archive()}")
        os.makedirs(root_archive())

        
except Exception as e:
    print("Error creating PKV directory:", e)
    sys.exit(1)

def main():
    print("This is a placeholder for the main function in libTools.py")

if __name__ == "__main__":
   main()