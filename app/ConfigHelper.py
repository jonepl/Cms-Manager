import os
from string import Template

# Docker environment variables
SUBSTITUTIONS = {
    'MYSQL_CONTAINER_NAME': "mysql_{site}",
    'MYSQL_DATABASE': "mysqldb",
    'MYSQL_USER': "mysqluser",
    'MYSQL_PASSWORD': "mysqlpassword",
    'MYSQL_ROOT_PASSWORD': "password",

    'PHPMYADMIN_CONTAINER_NAME': "phpmyadmin_{site}",
    'PHPMYADMIN_PORT': "{phpmyadmin_port}",
    'PMA_HOST': "mysql",

    'WORDPRESS_CONTAINER_NAME': "wordpress_{site}",
    'WORDPRESS_DB_NAME': "mysqldb",
    'WORDPRESS_DB_USER': "mysqluser",
    'WORDPRESS_DB_PASSWORD': "mysqlpassword",
    'WORDPRESS_DB_HOST': "mysql",
    'WORDPRESS_TABLE_PREFIX': "sEi_",
    'WORDPRESS_PORT': "{wordpress_port}",
    'NETWORK_NAME': "{site}_network",
}

class ConfigHelper():
  
  @staticmethod
  def update_env_file(site_path: str, site_name: str, ports: dict):
    """
    Updates the environment file with the provided substitution values.

    Args:
        env_file (str): Path to the environment file.
        site_name (str): Site name to use for substitution.
        phpmyadmin_port (int): phpMyAdmin port to use for substitution.
        wordpress_port (int): WordPress port to use for substitution.
    """
    substitutions = get_substitutions(site_name, ports.get("phpmyadmin"), ports.get("wordpress"))
    env_filepath = os.path.join(site_path, '.env')
    compose_filepath = os.path.join(site_path, 'docker-compose.yml')

    try:
      # Read the file
      with open(env_filepath , 'r') as file:
          lines = file.readlines()

      # Replace the lines containing the variables
      with open(env_filepath, 'w') as file:
          for line in lines:
              key, sep, value = line.partition('=')
              if key in substitutions:
                  file.write(f"{key}={substitutions[key]}\n")
              else:
                  file.write(line)
    except FileNotFoundError:
       print(f"Error: Environment file '{env_filepath}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    # Read the existing docker-compose.yml file
    with open(compose_filepath, 'r') as compose_file:
        compose_content = compose_file.read()
    
    # Use Template to replace placeholders with dynamic values
    compose_template = Template(compose_content)
    updated_compose_content = compose_template.substitute(substitutions)

    # Write the updated content back to the same file
    with open(compose_filepath, 'w') as compose_file:
        compose_file.write(updated_compose_content)

    try:
      pass
    except Exception as e:
      print(f"Error: {e}")


def get_substitutions(site_name: str, phpmyadmin_port: int, wordpress_port: int):
  """
  Returns a dictionary of substitution values.

  Args:
      site_name (str): Site name to use for substitution.
      mysql_port (int): MySQL port to use for substitution.
      phpmyadmin_port (int): phpMyAdmin port to use for substitution.
      wordpress_port (int): WordPress port to use for substitution.
  """  
  if not site_name or not phpmyadmin_port or not wordpress_port:
    raise ValueError("site_name, mysql_port, phpmyadmin_port, and wordpress_port must be provided")
  
  if not isinstance(site_name, str) or not isinstance(phpmyadmin_port, int) or not isinstance(wordpress_port, int):
    raise TypeError("site_name, mysql_port, phpmyadmin_port, and wordpress_port must be strings and integers")
  
  updated_substitutions = {}
  
  for key, value in SUBSTITUTIONS.items():
      # Replace placeholders with actual site name and phpmyadmin port
      updated_value = value.format(site=site_name, phpmyadmin_port=phpmyadmin_port, wordpress_port=wordpress_port)
      updated_substitutions[key] = updated_value
  
  return updated_substitutions