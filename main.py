from retriveIcal import WebScraping
import dropbox
from dropbox.exceptions import AuthError

def upload_to_dropbox(access_token, local_file_path, dropbox_path):
    try:
        # Connect to Dropbox using the access token
        dbx = dropbox.Dropbox(access_token)
        
        # Upload the file
        with open(local_file_path, 'rb') as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))

        print("File uploaded successfully.")
    except AuthError as e:
        print(f"Error connecting to Dropbox: {e}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    # Replace these variables with your own values
    dropbox_access_token = 'sl.Bu9msPx7Nm7x7fJ-NexbyzA-UM3oAzAvk7IThAgF1zJr0OrcFz7cvte7HD584Z0N7YRLGYFMW8Lx3rhFPAvRezbLAGMThX6z-05daNQpq7N4YgC2PtErS72qeZlcuMf42yugYJcI2w1zleelkyW6'
    local_file_path = 'files/my.ics'
    dropbox_path = '/my.ics'

    updater = WebScraping()
    updater.get_ical()
    upload_to_dropbox(dropbox_access_token, local_file_path, dropbox_path)
