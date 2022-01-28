from asyncio import subprocess
from curses import raw
from yaml import safe_load_all
import os
from typing import Iterator, Any
import subprocess
from pymongo.database import Database
from kubeql.constants import MANIFEST_COLLECTION

KUSTOMIZATION_YAML = "kustomization.yaml"
API_VERSION = "apiVersion"
KUSTOMIZE_CMD = ["kubectl", "kustomize"]


def _parse_yaml_str(raw_str: str, file_path: str) -> Iterator[dict[str, Any]]:
    content = safe_load_all(raw_str)
    for obj in content:
        if API_VERSION in obj:
            obj["_file_path"] = file_path
            yield obj


def crawl(dir_name: str, using_kustomization: bool = False) -> Iterator[dict[str, Any]]:
    for dir, _, files in os.walk(dir_name):
        for file in files:
            full_path = os.path.join(dir, file)
            if file == KUSTOMIZATION_YAML and using_kustomization:
                output = subprocess.run(KUSTOMIZE_CMD + [dir], capture_output=True)
                yield from _parse_yaml_str(output.stdout, full_path)
            elif file.endswith(".yaml") and not using_kustomization:
                with open(full_path) as f:
                    raw_yaml = f.read()
                yield from _parse_yaml_str(raw_yaml, full_path)


def load_into_db(db: Database, dir: str, using_kustomization: bool = False) -> None:
    collection = crawl(dir, using_kustomization)
    for obj in collection:
        db[MANIFEST_COLLECTION].insert_one(obj)
