import os
import shutil

from app.constants import SITES_DIR, TEMPLATES_DIR
from app.ConfigHelper import ConfigHelper


class WpSite:
    path = None

    def create(self, name: str, ports: dict):
        site_name = self._sanitize_site_name(name)
        self.path = self._create_site_path(site_name)
        if not os.path.exists(self.path):
            shutil.copytree(TEMPLATES_DIR, self.path)

        ConfigHelper.update_compose_file(self.path, site_name, ports)
        return site_name

    def load(self, name: str):
        path = self._create_site_path(name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Folder '{path}' not found.")
        self.path = path

    def remove(self):
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError as e:
            print(f"Folder '{self.path}' not found.")
            raise e
        except PermissionError as e:
            print(f"Permission denied to remove folder '{self.path}'.")
            raise e
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    def set_ssh_details(self, user: str, domain: str, password: str):
        if self.path is None:
            raise ValueError("Site path is not set. Please load or create a site first.")

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Site path: '{self.path}' not found.")

        env_path = os.path.join(self.path, ".env")
        properties = {"SSH_USER": user, "SSH_DOMAIN": domain, "SSH_PASSWORD": password}

        ConfigHelper.update_env_file(env_path, properties)

    def package(self, name: str):
        # Zips all source and database files from site path
        pass

    def upload(self):
        # Uploads packaged site files to remote server
        pass

    def download(self):
        # Downloads source and database files from remote server
        pass

    def _create_site_path(self, name: str) -> str:
        return os.path.join(SITES_DIR, name)

    def set_domain(self, domain: str):
        pass

    def _sanitize_site_name(self, name: str):
        # Remove any special characters
        return (
            name.replace(" ", "-")
            .replace(".", "")
            .replace("/", "")
            .replace("\\", "")
            .replace("?", "")
            .replace(":", "")
        )
