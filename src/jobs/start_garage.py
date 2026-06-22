import time
import pathlib

import docker

from src.utilities import get_base_directory

def start_garage(storage_path: str = None, size: int = 100):
    container_name = "comic-hub-s3"
    bucket_name = "comics"
    image_tag = "dxflrs/garage:v2.3.0"

    if not storage_path:
        base_dir = get_base_directory() / ".."
    else:
        base_dir = pathlib.Path(storage_path)
    
    config_dir = base_dir / "garage_config"
    data_dir = base_dir / "garage_data"
    meta_dir = base_dir / "garage_meta"
    config_file = config_dir / "garage.toml"

    for directory in [config_dir, data_dir, meta_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    client = docker.from_env()
    try:
        client.containers.get(container_name)
        print(f"Existing instance of {container_name} found. Aborting startup process.")
        return
    except docker.errors.NotFound:
        pass


    container = client.containers.run(
        image=image_tag,
        name=container_name,
        detach=True,
        restart_policy={"Name": "unless-stopped"},
        ports={
            "3900/tcp": 3900,  # S3 API
            "3901/tcp": 3901,  # RPC
            "3902/tcp": 3902,  # Web
            "3903/tcp": 3903   # Admin API
        },
        volumes={
            str(config_file): {"bind": "/etc/garage.toml", "mode": "ro"},
            str(meta_dir): {"bind": "/var/lib/garage/meta", "mode": "rw"},
            str(data_dir): {"bind": "/var/lib/garage/data", "mode": "rw"}
        }
    )

    time.sleep(5)

    node_id_res = container.exec_run("/garage status")
    node_id_output = node_id_res.output.decode("utf-8")
    node_id = [line for line in node_id_output.split("\n")][4].split()[0]

    container.exec_run(f"/garage layout assign {node_id} --zone local --capacity {size}G")
    container.exec_run("/garage layout apply --version 1")

    key_res = container.exec_run("/garage key create local-key")
    print(key_res.output.decode("utf-8"))

    bucket_res = container.exec_run(f"/garage bucket create {bucket_name}")
    if bucket_res.exit_code != 0:
        raise RuntimeError(bucket_res.output.decode("utf-8"))

    allow_res = container.exec_run(f"/garage bucket allow {bucket_name} --key local-key --read --write")
    if allow_res.exit_code != 0:
        raise RuntimeError(allow_res.output.decode("utf-8"))


if __name__ == "__main__":
    start_garage("G:\comichub")
