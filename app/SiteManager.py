import os
from dotenv import dotenv_values

from app.WpSite import WpSite;
from app.constants import SITES_DIR
from app.ConfigHelper import ConfigHelper

class SiteManager():
  site = None
  reserved_ports = []

  def __init__(self, initialize_ports = True):
    self.site = WpSite()
    if (initialize_ports):
      self._initialize_reserved_ports()

  def create_site(self, name):
    ports = self._get_available_ports()
    self.site.create(name, ports)

  def get_site(self, name) -> WpSite:
    self.site.load(name)
    return self.site
  
  def get_site_names(self) -> list:
    return os.listdir(SITES_DIR)
  
  def _initialize_reserved_ports(self) -> None:
    for site in os.listdir(SITES_DIR):
      config = dotenv_values(f"{SITES_DIR}/{site}/.env")

      if (config.get("PHPMYADMIN_PORT") != None):
        self.reserved_ports.append(int(config.get("PHPMYADMIN_PORT")))

      if (config.get("WORDPRESS_PORT") != None):
        self.reserved_ports.append(int(config.get("WORDPRESS_PORT")))

  def _get_available_ports(self) -> dict:
    ports = {}

    for port in range(8000, 9000):
      if port not in self.reserved_ports and (port + 1000) not in self.reserved_ports:
        ports["wordpress"] = port 
        ports["phpmyadmin"] = port + 1000
        break

    return ports

  # def create_new_project(self, name) -> None:
  #   WpSite(name, f"projects/{self._sanitizeProjectName(name)}")
  #   os.mkdir(f"projects/{self._sanitizeProjectName(name)}")

  # def load_existing_project(self, name):
  #   pass

  # def package_project():
  #   pass

  # def download_project():
  #   pass

  # def upload_project():
  #   pass

  # @staticmethod
  # def getProjectList():
  #   pass
    

  # @staticmethod
  # def remove_project():
  #   pass

  # def findProject(self, name):
  #   sanitized_name = self._sanitizeProjectName(name)
  #   project_path = f"projects/{ sanitized_name}"
  #   if os.path.exists(project_path) :
  #     return project_path
  #   else:
  #     return None

  # def _sanitizeProjectName(self, name: str):
  #   # Remove any special characters
  #   return name.replace(" ", "-").replace(".", "").replace("/", "").replace("\\", "").replace("?", "").replace(":", "")

  # def _findOrCreateProject(self, name):
  #   sanitized_name = self._sanitizeProjectName(name)
  #   os.path.exists(f"projects/{ sanitized_name}")
  #   pass

  # def _isExistingProject(self, name):
  #   sanitized_name = self._sanitizeProjectName(name)
  #   return os.path.exists(f"projects/{ sanitized_name}")





