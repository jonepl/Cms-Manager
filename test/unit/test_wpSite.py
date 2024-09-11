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

    actual = site.create(name, ports)

    assert actual == name
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

    actual = site.create(name, ports)

    assert actual == expected_name
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


@mock.patch("app.ConfigHelper.ConfigHelper.update_env_file")
@mock.patch("os.path.exists", return_value=True)
def test_set_ssh_details_for_empty_env_file(
    mock_exists: mock.MagicMock, mock_update_env_file: mock.MagicMock
):
    user = "testUser"
    domain = "testDomain"
    password = "testPassword"
    site.path = "test/path"
    expected_path = os.path.join(site.path, ".env")

    site.set_ssh_details(user, domain, password)

    mock_update_env_file.assert_called_with(
        expected_path, {"SSH_USER": user, "SSH_DOMAIN": domain, "SSH_PASSWORD": password}
    )


def test_set_ssh_details_for_missing_site_path():
    site.path = None

    with pytest.raises(ValueError):
        site.set_ssh_details("testUser", "testDomain", "testPassword")


@mock.patch("os.path.exists", return_value=False)
def test_set_ssh_details_for_invalid_env_file(tmp_path: str):
    site.path = tmp_path

    with pytest.raises(FileNotFoundError):
        site.set_ssh_details("testUser", "testDomain", "testPassword")


@mock.patch("os.path.exists", return_value=False)
def test_set_ssh_details_for_missing_env_file(tmp_path: str):
    site.path = tmp_path

    with pytest.raises(FileNotFoundError):
        site.set_ssh_details("testUser", "testDomain", "testPassword")
