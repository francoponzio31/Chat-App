from config.app_config import config
from requests.exceptions import HTTPError
import requests
from io import BytesIO
import mimetypes


class FileserverClient:
    
    fileserver_url = config.FILESERVER_BASE_URL

    def upload_file(self, file_content:bytes, filename:str) -> str:
        """
        Uploads a file and returns the file id in the fileserver.
        """
        file = BytesIO(file_content)
        mimetype, _ = mimetypes.guess_type(filename)
        file = {"file": (filename, file, mimetype)}

        url = f"{self.fileserver_url}/api/files"
        headers = {
            "accept": "application/json",
        }
        response = requests.post(url, headers=headers, files=file)

        if not response.status_code == 200:
            raise HTTPError

        file_data = response.json()
        return file_data["file_id"]


    def get_file_content(self, file_id:str) -> str:
        """
        Obtains the b64 encoded file content for the given id.
        """
        url = f"{self.fileserver_url}/api/files/{file_id}/content"
        headers = {
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers)

        if not response.status_code == 200:
            raise HTTPError

        file_data = response.json()
        return file_data["content"]


fs_client = FileserverClient()