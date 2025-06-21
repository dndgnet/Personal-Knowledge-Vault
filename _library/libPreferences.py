import os
import sys 
import json

#group our preferences together in a directory
#to avoid conflicts with other applications
applicationNameRoot = "_DNDG"

#give each application or code snippet a unique preferences file name
preferences_File = "Personal-Knowledge-Vault.json"

#empty preferences file
_exampleEmptyPreferences = {
    "pkv_root":"PKV",
    "attachments_root":"attachments",
    "projects_root":"projects",
    "archive_root":".archive",
    "timestamp_id_format":"%y%m%d%H%M%S",
    "datetime_format":"%Y-%m-%d %H:%M:%S"
    }

_preferences = {}

# each OS might be saving preferences and docs in a different paths
preferences_Path = ""
documents_Path = ""
if sys.platform in ('linux', 'linux2',"darwin"):
    preferences_Path = os.path.expanduser('~/Library/Preferences/')
    documents_Path = os.path.expanduser('~/Documents')
elif sys.platform in ('win32','windows'):
    preferences_Path = os.path.join(os.environ['APPDATA'], 'Preferences')
    documents_Path = os.path.join(os.environ.get("USERPROFILE", ""), "Documents")
else:
    print(f"Unsupported platform: {sys.platform}")
    sys.exit(1)

# shared preferences
_pkv_root = ""
_attachment_root = ""
_projects_root = ""
_archive_root = ""
_timestamp_id_format = ""
_datetime_format = ""

def root_pkv() -> str:
    """Returns the documents subfolder for the pkv."""
    return os.path.join (documents_Path,_pkv_root)

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
    # "pkv_root":"PKV",
    # "attachments_root":"attachments",
    # "projects_root":"projects",
    # "archive_root":".archive",
    # "timestamp_id_format":"%y%m%d%H%M%S",
    # "datetime_format":"%Y-%m-%d %H:%M:%S"
        _preferences = json.load(file)
        _pkv_root = _preferences["pkv_root"]
        _attachment_root = _preferences["attachments_root"]
        _projects_root = _preferences["projects_root"]
        _archive_root = _preferences["archive_root"]
        _timestamp_id_format = _preferences["timestamp_id_format"]
        _datetime_format = _preferences["datetime_format"]
                        
    print(f"{len(_preferences)} preferences loaded successfully")

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