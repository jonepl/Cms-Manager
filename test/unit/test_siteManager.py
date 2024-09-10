from unittest import mock

from app.SiteManager import SiteManager


MOCK_CONFIG = {"PHPMYADMIN_PORT": 8000, "WORDPRESS_PORT": 9000}


def setup_function(function):
    global manager
    manager = SiteManager(False)


@mock.patch("app.SiteManager.dotenv_values", return_value=MOCK_CONFIG)
@mock.patch("os.listdir", return_value=["TestProject"])
def test_constructor(mock_listdir: mock.MagicMock, mock_dotenv_values: mock.MagicMock):
    manager = SiteManager()

    assert manager.site is not None
    assert manager.reserved_ports == [8000, 9000]


def test_create_site_no_reserverd_ports():
    manager.site = mock.MagicMock()

    manager.create_site("TestProject")

    assert manager.site.create.called_with(
        "TestProject", {"phpmyadmin": 8000, "wordpress": 9000}
    )


def test_create_site_with_reserverd_ports():
    manager.site = mock.MagicMock()
    manager.reserved_ports = [8000, 8003, 9001, 9004]

    manager.create_site("TestProject")

    assert manager.site.create.called_with(
        "TestProject", {"phpmyadmin": 8005, "wordpress": 9005}
    )


def test_get_site():
    manager.site = mock.MagicMock()

    actual = manager.get_site("TestProject")

    assert actual == manager.site
    assert manager.site.load.called_with("TestProject")


@mock.patch("os.listdir")
def test_get_site_names(mock_listdir: mock.MagicMock):
    actual = manager.get_site_names()

    assert actual == mock_listdir.return_value
