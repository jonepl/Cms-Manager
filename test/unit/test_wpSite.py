import os
import pytest
from unittest import mock

from app.WpSite import WpSite
from app.constants import SITES_DIR, TEMPLATES_DIR


def setup_function(function):
    global site
    site = WpSite()


def test_init():
    assert site.path is None


@mock.patch("app.WpSite.ConfigHelper.update_compose_file")
@mock.patch("shutil.copytree")
def test_create(mock_copytree: mock.MagicMock, mock_update_compose_file: mock.MagicMock):
    name = "testSite"
    ports = {"http": 8080, "https": 8443}
    expected_path = os.path.join(SITES_DIR, name)

    site.create(name, ports)

    mock_copytree.assert_called_with(TEMPLATES_DIR, expected_path)
    mock_update_compose_file.assert_called_with(expected_path, name, ports)


@pytest.mark.parametrize(
    "name,expected_name",
    [
        ("test site", "test-site"),
        ("test.site", "testsite"),
        ("test/site", "testsite"),
        ("test\\site", "testsite"),
        ("test?site", "testsite"),
        ("test:site", "testsite"),
    ],
)
@mock.patch("app.WpSite.ConfigHelper.update_compose_file")
@mock.patch("shutil.copytree")
def test_create_sanitize_site_name(
    mock_copytree: mock.MagicMock,
    mock_update_compose_file: mock.MagicMock,
    name: str,
    expected_name: str,
):
    ports = {"http": 8080, "https": 8443}
    expected_path = os.path.join(SITES_DIR, expected_name)

    site.create(name, ports)

    mock_copytree.assert_called_with(TEMPLATES_DIR, expected_path)
    mock_update_compose_file.assert_called_with(expected_path, expected_name, ports)


@mock.patch("os.path.exists", return_value=True)
def test_load(mock_exists: mock.MagicMock):
    site_name = "testSite"
    expected_path = os.path.join(SITES_DIR, site_name)

    site.load(site_name)

    assert site.path
    mock_exists.assert_called_with(expected_path)


@mock.patch("os.path.exists", return_value=False)
def test_load_path_not_exists(mock_exists: mock.MagicMock):
    with pytest.raises(FileNotFoundError):
        site.load("testSite")


@mock.patch("shutil.rmtree")
def test_remove(mock_rmtree: mock.MagicMock):
    site.path = os.path.join(SITES_DIR, "testSite")

    site.remove()

    mock_rmtree.assert_called_with("sites/testSite")


@mock.patch("shutil.rmtree", side_effect=FileNotFoundError)
def test_remove_path_not_exists(mock_exists: mock.MagicMock):
    with pytest.raises(FileNotFoundError):
        site.remove()


@mock.patch("shutil.rmtree", side_effect=PermissionError)
def test_remove_permission_denied(mock_exists: mock.MagicMock):
    with pytest.raises(PermissionError):
        site.remove()


@mock.patch("shutil.rmtree", side_effect=Exception)
def test_remove_exception(mock_exists: mock.MagicMock):
    with pytest.raises(Exception):
        site.remove()
