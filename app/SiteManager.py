import os
from dotenv import dotenv_values

from app.WpSite import WpSite;
from app.constants import SITES_DIR

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
