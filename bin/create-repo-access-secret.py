#!/usr/bin/env python3
import argparse
import shlex
import subprocess
import sys

from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("key_file_base_name", help="ssh key file name")
    parser.add_argument("-d", "--directory", help="directory to use for keyfiles and known_hosts, defaults to ~/.ssh",
                        default=str(Path.home() / '.ssh'))
    args = parser.parse_args()

    private_key = Path(args.key_file_base_name)
    if private_key.exists():
        known_hosts = private_key.parent / "known_hosts"
    else:
        private_key = Path(args.directory) / args.key_file_base_name
        known_hosts = Path(args.directory) / "known_hosts"

    if not private_key.exists():
        print(f"Error: unable to find key file: {private_key}")
        sys.exit(-1)

    sys.exit(subprocess.call(shlex.split(f"""
kubectl create secret generic team-viewer-repo-access --from-file=ssh-privatekey={private_key} --from-file={known_hosts}
""")))