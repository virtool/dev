import asyncio
from typing import List

from ruamel.yaml import YAML

from exceptions import UnrecognizedYAMLTemplate
from images import VirtoolRepositories
from yaml import (
    get_yaml_kind,
    get_yaml_files,
    get_container_name_from_url,
    get_containers,
    load_yaml_file,
    dump_yaml_file,
    get_resource_name,
)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)


YAML_DIRECTORIES = [
    "manifests",
    "manifests/jobs",
    "manifests/tasks",
    "manifests/tasks/task_yaml",
]


async def update_yaml_files(files: List[str]):
    for file in files:
        yaml_files = load_yaml_file(file)

        for yaml_file in yaml_files:
            await update_yaml_file(yaml_file)

        dump_yaml_file(file, yaml_files)


async def update_yaml_file(yaml_file: dict):
    try:
        kind = get_yaml_kind(yaml_file)

        if not kind.is_updatable:
            return

        for container in get_containers(yaml_file):
            container_name = get_container_name_from_url(container["image"])
            image_url = await VirtoolRepositories[
                container_name
            ].value.get_latest_image_url()
            container["image"] = image_url

            print(f"Updated {get_resource_name(yaml_file)} to {image_url}")

    except (UnrecognizedYAMLTemplate, KeyError):
        name = yaml_file.get("metadata", {}).get("name", "unknown")
        print(f"Skipped updating {name}")


async def main():

    yaml_files = get_yaml_files(YAML_DIRECTORIES)

    await update_yaml_files(yaml_files)


asyncio.run(main())
