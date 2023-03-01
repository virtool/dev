from enum import Enum
import requests
from abc import ABC


class BaseImage(ABC):
    base_container_url = ""

    def __init__(self, container_name: str, repository_name: str):
        self.container_name = container_name
        self.repo_name = repository_name
        self.tag = None

    @property
    def base_image_url(self) -> str:
        return f"{self.base_container_url}/{self.container_name}"

    async def get_latest_tag(self) -> str:
        if self.tag is None:
            self.tag = await self._get_latest_tag()
        return self.tag

    async def _get_latest_tag(self) -> str:
        ...

    async def get_latest_image_url(self) -> str:
        return f"{self.base_image_url}:{await self.get_latest_tag()}"

    def __str__(self):
        return f"{self.repo_name}:{self.tag}"


class GHCRImage(BaseImage):
    base_container_url = "ghcr.io/virtool"

    async def _get_latest_tag(self) -> str:
        url = f"https://api.github.com/repos/virtool/{self.repo_name}/releases/latest"
        response = requests.get(url)
        return response.json()["tag_name"]


class VirtoolRepositories(Enum):
    virtool = GHCRImage("virtool", "virtool")
    pathoscope = GHCRImage("pathoscope", "workflow-pathoscope")
    ui = GHCRImage("ui", "virtool-ui")
    migration = GHCRImage("migration", "virtool-migration")
    create_sample = GHCRImage("create-sample", "workflow-create-sample")
    create_subtraction = GHCRImage("create-subtraction", "workflow-create-subtraction")
    build_index = GHCRImage("build-index", "workflow-build-index")
    nuvs = GHCRImage("nuvs", "workflow-nuvs")
