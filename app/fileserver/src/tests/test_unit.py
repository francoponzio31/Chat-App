import pytest
from services.files_service import files_service
from utilities.utils import validate_uuid_format


@pytest.mark.asyncio
async def test_files_service(test_image_content):
    """Test for uploading, getting and deleting a file"""

    # Upload a file
    file_id = await files_service.upload_file(test_image_content)
    assert validate_uuid_format(file_id) == True

    # Get uploaded file
    file_content, filename, mime_type = await files_service.get_file_by_id(file_id, format="bytes")
    assert file_content == test_image_content
    assert filename == f"{file_id}.png"
    assert mime_type == "image/png"

    # Delete uploaded file
    await files_service.delete_file_by_id(file_id)
    with pytest.raises(FileNotFoundError):
        await files_service.get_file_by_id(file_id, format="bytes")
    