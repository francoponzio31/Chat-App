import re


def bytes_to_mb(bytes:int) -> int:
    return bytes / 1048576

def validate_uuid_format(file_id:str) -> bool:
    uuid_regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    return bool(re.match(uuid_regex, file_id))
