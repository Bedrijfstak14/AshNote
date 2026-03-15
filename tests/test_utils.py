import pytest
from unittest.mock import MagicMock
from app.utils import _allowed_file


class TestAllowedFile:
    def test_jpg_allowed(self):
        assert _allowed_file("foto.jpg") is True

    def test_jpeg_allowed(self):
        assert _allowed_file("foto.jpeg") is True

    def test_png_allowed(self):
        assert _allowed_file("foto.png") is True

    def test_gif_allowed(self):
        assert _allowed_file("animatie.gif") is True

    def test_webp_allowed(self):
        assert _allowed_file("modern.webp") is True

    def test_exe_not_allowed(self):
        assert _allowed_file("virus.exe") is False

    def test_php_not_allowed(self):
        assert _allowed_file("shell.php") is False

    def test_no_extension(self):
        assert _allowed_file("bestandzonderextensie") is False

    def test_uppercase_extension(self):
        # Extensie-check is case-insensitive
        assert _allowed_file("FOTO.JPG") is True

    def test_double_extension(self):
        # Alleen de laatste extensie telt
        assert _allowed_file("shell.php.jpg") is True
