import os
import pytest
from pathlib import Path
from unittest import mock

from app.ConfigHelper import ConfigHelper, _get_substitutions, SUBSTITUTIONS

MOCK_DOCKER_COMPOSE = """version: '3'
services:
  mysql:
    container_name: ${MYSQL_CONTAINER_NAME}
    environment:
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
    networks:
      - ${NETWORK_NAME}
  wordpress:
    container_name: ${WORDPRESS_CONTAINER_NAME}
    ports:
      - "${WORDPRESS_PORT}:80"
    environment:
      - WORDPRESS_DB_NAME=${WORDPRESS_DB_NAME}
      - WORDPRESS_DB_USER=${WORDPRESS_DB_USER}
      - WORDPRESS_DB_PASSWORD=${WORDPRESS_DB_PASSWORD}
      - WORDPRESS_DB_HOST=${WORDPRESS_DB_HOST}
      - WORDPRESS_TABLE_PREFIX=${WORDPRESS_TABLE_PREFIX}
    networks:
      - ${NETWORK_NAME}
  phpmyadmin:
    container_name: ${PHPMYADMIN_CONTAINER_NAME}
    ports:
      - "${PHPMYADMIN_PORT}:80"
    environment:
      - PMA_HOST=${PMA_HOST}
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
"""


def test_update_compose_file(
    tmp_path,
):
    # Create a temporary directory with a docker-compose.yml file
    compose_file: Path = tmp_path / "docker-compose.yml"
    compose_file.write_text(MOCK_DOCKER_COMPOSE)

    # Create a temporary file with environment variables
    env_file: Path = tmp_path / "env_file.txt"
    env_file.write_text(
        "MYSQL_CONTAINER_NAME=mysql-default\n"
        "WORDPRESS_CONTAINER_NAME=wordpress-default\n"
        "PHPMYADMIN_PORT=8080\n"
        "MYSQL_PORT=3306\n"
        "WORDPRESS_PORT=80\n"
    )

    # Define the substitution values
    site_name = "my_site"
    ports = {"phpmyadmin": 8081, "wordpress": 81}

    # Call the update_compose_file method
    ConfigHelper.update_compose_file(str(tmp_path), site_name, ports)

    # Check the updated docker-compose.yml file
    updated_compose_file = compose_file.read_text()
    assert "mysql_my_site" in updated_compose_file
    assert "8081:80" in updated_compose_file
    assert "wordpress_my_site" in updated_compose_file
    assert "81:80" in updated_compose_file
    assert "phpmyadmin_my_site" in updated_compose_file


@mock.patch("os.path.join", return_value="env.txt")
@mock.patch("os.path.exists", return_value=True)
def test_update_env_file(
    mock_exists: mock.MagicMock, mock_join: mock.MagicMock, tmp_path: str
):
    user = "testUser"
    domain = "testDomain"
    password = "testPassword"
    env_path = os.path.join("test/path", ".env")
    with open(env_path, "w") as file:
        file.write("")
    mock_join.return_value = env_path

    ConfigHelper.update_env_file(
        env_path, {"SSH_USER": user, "SSH_DOMAIN": domain, "SSH_PASSWORD": password}
    )

    with open(env_path, "r") as f:
        content = f.read()
        assert f"SSH_USER={user}" in content
        assert f"SSH_DOMAIN={domain}" in content
        assert f"SSH_PASSWORD={password}" in content


@mock.patch("os.path.join", return_value="env.txt")
@mock.patch("os.path.exists", return_value=True)
def test_update_env_file_for_partially_filled_env_file(
    mock_exists: mock.MagicMock, mock_join: mock.MagicMock, tmp_path: str
):
    user = "testUser"
    domain = "testDomain"
    password = "testPassword"
    env_path = os.path.join("test/path", ".env")
    with open(env_path, "w") as file:
        file.write("SSH_USER=previousValue\n" "OTHER_VALUE=value\n")
    mock_join.return_value = env_path

    ConfigHelper.update_env_file(
        env_path, {"SSH_USER": user, "SSH_DOMAIN": domain, "SSH_PASSWORD": password}
    )

    with open(os.path.join(env_path, ".env"), "r") as f:
        content = f.read()
        assert f"SSH_USER={user}" in content
        assert f"SSH_DOMAIN={domain}" in content
        assert f"SSH_PASSWORD={password}" in content
        assert "OTHER_VALUE=value" in content


@mock.patch("os.path.exists", return_value=False)
def test_update_env_file_for_invalid_env_file(mock_exists: mock.MagicMock):
    with pytest.raises(FileNotFoundError):
        ConfigHelper.update_env_file(
            "test/path/.env",
            {
                "SSH_USER": "testUser",
                "SSH_DOMAIN": "testDomain",
                "SSH_PASSWORD": "testPassword",
            },
        )


def test_get_substitutions():
    site_name = "test-site"
    phpmyadmin_port = 8080
    wordpress_port = 80

    substitutions = _get_substitutions(site_name, phpmyadmin_port, wordpress_port)

    assert isinstance(substitutions, dict)
    assert len(substitutions) > 0
    assert substitutions.get("MYSQL_CONTAINER_NAME") == SUBSTITUTIONS.get(
        "MYSQL_CONTAINER_NAME"
    ).format(site=site_name)
    assert substitutions.get("WORDPRESS_CONTAINER_NAME") == SUBSTITUTIONS.get(
        "WORDPRESS_CONTAINER_NAME"
    ).format(site=site_name)
    assert substitutions.get("PHPMYADMIN_CONTAINER_NAME") == SUBSTITUTIONS.get(
        "PHPMYADMIN_CONTAINER_NAME"
    ).format(site=site_name)
    assert substitutions.get("PHPMYADMIN_PORT") == SUBSTITUTIONS.get(
        "PHPMYADMIN_PORT"
    ).format(phpmyadmin_port=phpmyadmin_port)
    assert substitutions.get("WORDPRESS_PORT") == SUBSTITUTIONS.get(
        "WORDPRESS_PORT"
    ).format(wordpress_port=wordpress_port)
    assert substitutions.get("NETWORK_NAME") == SUBSTITUTIONS.get("NETWORK_NAME").format(
        site=site_name
    )


def test_get_substitutions_empty_site_name():
    site_name = ""
    phpmyadmin_port = 8080
    wordpress_port = 80

    with pytest.raises(ValueError):
        _get_substitutions(site_name, phpmyadmin_port, wordpress_port)


def test_get_substitutions_invalid_port():
    site_name = "test-site"
    phpmyadmin_port = "invalid"
    wordpress_port = 80

    with pytest.raises(TypeError):
        _get_substitutions(site_name, phpmyadmin_port, wordpress_port)
