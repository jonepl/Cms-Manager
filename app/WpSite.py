import os
import shutil

from app.constants import SITES_DIR, TEMPLATES_DIR
from app.ConfigHelper import ConfigHelper

class WpSite():
  path = None

  def __init__(self):
    pass

  def create(self, name: str, ports: dict):
    site_name = self._sanitize_site_name(name)
    self.path = self._create_site_path(site_name)
    if (os.path.exists(self.path) == False):
      shutil.copytree(TEMPLATES_DIR, self.path)

    ConfigHelper.update_env_file(self.path, site_name, ports)


  def load(self, name: str):
    site_path = self._create_site_path(name)
    if (os.path.exists(site_path) == False):
      print(f"No site found at path '{site_path}'. Site not loaded.")
      return
    self.path = self._create_site_path(name)


  def package(self, name: str):
    # Zips all source and database files from site path
    pass

  def upload(self):
    # Uploads packaged site files to remote server
    pass

  def download(self):
    # Downloads source and database files from remote server
    pass

  def remove(self):
    try:
      shutil.rmtree(self.path)
    except FileNotFoundError:
        print(f"Folder '{self.path}' not found.")
    except PermissionError:
        print(f"Permission denied to remove folder '{self.path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

  def _create_site_path(self, name: str) -> str:
    return os.path.join(SITES_DIR, name)
  
  def set_domain(self, domain: str):
    pass
  
  def _sanitize_site_name(self, name: str):
    # Remove any special characters
    return name.replace(" ", "-").replace(".", "").replace("/", "").replace("\\", "").replace("?", "").replace(":", "")