import pytest
from pathlib import Path

from app.ConfigHelper import ConfigHelper, get_substitutions, SUBSTITUTIONS


def test_update_env_file(tmp_path,):
    # Create a temporary file with environment variables
    env_file: Path = tmp_path / "env_file.txt"
    env_file.write_text("MYSQL_CONTAINER_NAME=mysql-default\n"
                         "WORDPRESS_CONTAINER_NAME=wordpress-default\n"
                         "PHPMYADMIN_PORT=8080\n"
                         "MYSQL_PORT=3306\n"
                         "WORDPRESS_PORT=80\n")

    # Define the substitution values
    site_name = "my-site"
    mysql_port = 3307
    phpmyadmin_port = 8081
    wordpress_port = 81

    # Call the update_env_file method
    ConfigHelper.update_env_file(str(env_file), site_name, mysql_port, phpmyadmin_port, wordpress_port)

    # Check the updated environment file
    updated_env_file = env_file.read_text()
    assert updated_env_file == ("MYSQL_CONTAINER_NAME=mysql-my-site\n"
                                 "WORDPRESS_CONTAINER_NAME=wordpress-my-site\n"
                                 "PHPMYADMIN_PORT=8081\n"
                                 "MYSQL_PORT=3307\n"
                                 "WORDPRESS_PORT=81\n")


def test_update_env_file_file_not_found(tmp_path, capsys):
    # Create a non-existent file path
    env_file = tmp_path / "non_existent_file.txt"

    # Call the update_env_file method
    ConfigHelper.update_env_file(str(env_file), "test-site", 3306, 8080, 80)

    # Check the error message
    assert capsys.readouterr().out == f"Error: Environment file '{env_file}' not found.\n"

def test_update_env_file_general_exception(tmp_path, capsys):
    # Create a file with invalid permissions
    env_file = tmp_path / "env_file.txt"
    env_file.write_text("test content")
    env_file.chmod(0o000)  # Make the file unreadable

    # Call the update_env_file method
    ConfigHelper.update_env_file(str(env_file), "test-site", 3306, 8080, 80)

    # Check the error message
    assert capsys.readouterr().out.startswith("Error: ")


def test_get_substitutions():
    
    site_name = "test-site"
    mysql_port = 3306
    phpmyadmin_port = 8080
    wordpress_port = 80

    substitutions = get_substitutions(site_name, mysql_port, phpmyadmin_port, wordpress_port)

    assert isinstance(substitutions, dict)
    assert len(substitutions) > 0
    assert substitutions.get("MYSQL_CONTAINER_NAME") == SUBSTITUTIONS.get("MYSQL_CONTAINER_NAME").format(site=site_name)
    assert substitutions.get("WORDPRESS_CONTAINER_NAME") == SUBSTITUTIONS.get("WORDPRESS_CONTAINER_NAME").format(site=site_name)
    assert substitutions.get("PHPMYADMIN_CONTAINER_NAME") == SUBSTITUTIONS.get("PHPMYADMIN_CONTAINER_NAME").format(site=site_name)
    assert substitutions.get("PHPMYADMIN_PORT") == SUBSTITUTIONS.get("PHPMYADMIN_PORT").format(phpmyadmin_port=phpmyadmin_port)
    assert substitutions.get("MYSQL_PORT") == SUBSTITUTIONS.get("MYSQL_PORT").format(mysql_port=mysql_port)
    assert substitutions.get("WORDPRESS_PORT") == SUBSTITUTIONS.get("WORDPRESS_PORT").format(wordpress_port=wordpress_port)
    assert substitutions.get("NETWORK_NAME") == SUBSTITUTIONS.get("NETWORK_NAME").format(site=site_name)


def test_get_substitutions_empty_site_name():
    site_name = ""
    mysql_port = 3306
    phpmyadmin_port = 8080
    wordpress_port = 80

    with pytest.raises(ValueError):
        get_substitutions(site_name, mysql_port, phpmyadmin_port, wordpress_port)


def test_get_substitutions_invalid_port():
    site_name = "test-site"
    mysql_port = "invalid"
    phpmyadmin_port = 8080
    wordpress_port = 80

    with pytest.raises(TypeError):
        get_substitutions(site_name, mysql_port, phpmyadmin_port, wordpress_port)