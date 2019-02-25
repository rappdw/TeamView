#!/usr/bin/env python3
import argparse
import os
import shlex
import subprocess
import sys
import shutil

from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key_file", help="ssh key file (private key)", required=True)
    parser.add_argument("-d", "--directory", help="keys directory (defaul: ~/.ssh)", default=str(Path.home() / '.ssh'))
    parser.add_argument("-c", "--config_file", help="Configuration file", required=True)
    parser.add_argument("-m", "--mailmap_file", help="Mail map file")
    args = parser.parse_args()

    os.makedirs(os.path.join(os.path.expanduser("~"), '.local/share/cache'), exist_ok=True)

    if shutil.which('kubectl'):
        kubectl = 'kubectl'
    elif shutil.which('microk8s.kubectl'):
        kubectl = 'microk8s.kubectl'
    else:
        print("Unable to find kubectl. Please ensure that kubernetes is propertly setup.")
        sys.exit(-1)

    private_key = Path(args.key_file)
    if private_key.exists():
        known_hosts = private_key.parent / "known_hosts"
    else:
        private_key = Path(args.directory) / args.key_file_base_name
        known_hosts = Path(args.directory) / "known_hosts"

    if not private_key.exists():
        print(f"Error: unable to find key file: {private_key}")
        sys.exit(-1)

    if not known_hosts.exists():
        print(f"Error: known_hosts not found in directory: {private_key.parent}")
        sys.exit(-1)

    config_file = Path(args.config_file)
    if not config_file.exists():
        print(f"Error: configuration file, {config_file}, not found.")

    mailmap_file = Path(args.mailmap_file)

    subprocess.call(shlex.split(f"{kubectl} delete secret team-view-access"))
    subprocess.call(shlex.split(f"{kubectl} delete configmap team-view-configuration"))

    rc = subprocess.call(shlex.split(f"""
{kubectl} create secret generic team-view-access --from-file=ssh-privatekey={private_key} --from-file=known_hosts={known_hosts} --from-file=config={config_file}
"""))

    if rc:
        sys.exit(rc)

    if mailmap_file.exists():
        sys.exit(subprocess.call(shlex.split(f"""
        {kubectl} create configmap team-view-configuration --from-file=extract.json={config_file} --from-file=.mailmap={mailmap_file}
        """)))
    else:
        sys.exit(subprocess.call(shlex.split(f"""
        {kubectl} create configmap team-view-configuration --from-file=extract.json={config_file}
        """)))
