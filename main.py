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
    dropbox_access_token = 'sl.Bu7y4AFjW9O40ELnU7lq-zeivjYJHI3BCT2zCq1rKLaq1MIQKeJTqm7_VQ0cFaVRNHFZyPt7JTjuW-xbFxkTeeZCtjcz9fWfqHOU5SsVi_VYclcsoESGMM2nJyrGGejH2cqBZiTP5LASIjKKpMJR'
    local_file_path = 'files/my.ics'
    dropbox_path = '/my.ics'

    updater = WebScraping()
    updater.get_ical()
    upload_to_dropbox(dropbox_access_token, local_file_path, dropbox_path)
