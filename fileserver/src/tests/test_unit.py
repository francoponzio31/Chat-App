import pytest
import re
from config.app_config import config
from repositories.fs_files_repository import FSFilesRepository
from repositories.s3_files_repository import S3FilesRepository


@pytest.fixture
def repository():
    repository = S3FilesRepository() if config.persistance_type == "S3" else FSFilesRepository()
    return repository

@pytest.mark.asyncio
async def test_files_repository(repository, test_image_content):
    """Test for uploading, getting and deleting a file"""

    # Upload a file
    file_id = await repository.upload_file(test_image_content)
    uuid_regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert re.match(uuid_regex, file_id)

    # Get uploaded file
    file_content, filename, mime_type = await repository.get_file_by_id(file_id, format="bytes")
    assert file_content == test_image_content
    assert filename == f"{file_id}.png"
    assert mime_type == "image/png"

    # Delete uploaded file
    await repository.delete_file_by_id(file_id)
    with pytest.raises(FileNotFoundError):
        await repository.get_file_by_id(file_id, format="bytes")
    