from enum import Enum
from typing import List
import os
from exceptions import UnrecognizedYAMLTemplate
import re
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

class UpdatableKindTypes(Enum):
    CronJob = "CronJob"
    Deployment = "Deployment"
    ScaledJob = "ScaledJob"
    Job = "Job"
    Pod = "Pod"

class KindTypes(Enum):
    CronJob = "CronJob"
    Deployment = "Deployment"
    ScaledJob = "ScaledJob"
    Job = "Job"
    Pod = "Pod"
    Service = "Service"
    Ingress = "Ingress"
    PersistentVolume = "PersistentVolume"
    PersistentVolumeClaim = "PersistentVolumeClaim"
    ConfigMap = "ConfigMap"

    @property
    def is_updatable(self):
        try:
            UpdatableKindTypes(self.value)
        except ValueError:
            return False
        return True


def load_yaml_file(file: str) -> List[dict]:
    """
    Load a yaml file.

    :param file: yaml file
    :return: list of yaml files
    """
    with open(file, "r") as f:
        return [file for file in yaml.load_all(f)]


def dump_yaml_file(file: str, yaml_files: List[dict]):
    """
    Dump a yaml file.

    :param file: yaml file
    :param yaml_files: list of yaml files
    """
    with open(file, "w") as f:
        yaml.dump_all(yaml_files, f)

def get_yaml_files(dirs: List[str]) -> List[str]:
    """
    Get all yaml files in a list of directories.

    :param dirs: list of directories to search
    :return: list of yaml files
    """
    files = []
    for directory in dirs:
        for file in os.listdir(directory):
            if file.endswith(".yaml"):
                files.append(os.path.join(directory, file))
    return files

def get_resource_name(yaml_file: dict) -> str:
    """
    Get the name from a yaml file.

    :param yaml_file: yaml file
    :return: name
    """
    try:
        return yaml_file["metadata"]["name"]
    except KeyError:
        return "Unknown"


def get_container_name_from_url(image_url: str) -> str:
    """
    Get the container name from an image url.

    :param image_url: image url
    :return: container name
    """

    return re.search(r"/([^/]+):", image_url).group(1).replace("-", "_")


def get_yaml_kind(yaml_file) -> KindTypes:
    if "kind" in yaml_file:
        return KindTypes(yaml_file["kind"])

    raise UnrecognizedYAMLTemplate("Yaml file does not have a kind")

def get_containers(yaml_file):
    """
    Get the containers from a yaml file.
    :param yaml_file:
    :return:
    """

    kind = get_yaml_kind(yaml_file)

    match kind:
        case KindTypes.CronJob:
            return yaml_file["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"]
        case KindTypes.ScaledJob:
            return yaml_file["spec"]["jobTargetRef"]["template"]["spec"]["containers"]
        case KindTypes.Job | KindTypes.Deployment | KindTypes.Pod:
            return yaml_file["spec"]["template"]["spec"]["containers"]

    raise UnrecognizedYAMLTemplate(f"Yaml file does not have a known kind {kind}")


