#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess

def main():
    env_name = "smn_tools"
    display_name = "Python (smn_tools)"
    subprocess.check_call([sys.executable, "-m", "ipykernel", "install",
                           "--user", "--name", env_name, "--display-name", display_name])

if __name__ == "__main__":
    main()

