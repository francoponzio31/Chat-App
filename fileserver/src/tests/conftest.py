"""
This module provides shareable fixtures for all test files.
"""

import pytest
import os


@pytest.fixture
def test_image_content():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, "test.png")
    with open(image_path, "rb") as test_image:
        return test_image.read()