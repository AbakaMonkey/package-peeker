from package_peeker import cli
from importlib import metadata
import subprocess
import shutil
import sys
import os

packages = []

def ensureRoot():
    if os.geteuid() == 0:
        return

    print("Elevating with sudo privledges...")

    os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

def selectFunction():
    selected_pkg = cli.viewPackages(packages)
    selected_pkg_name = packages[selected_pkg]
    function = cli.managePackage(selected_pkg_name)

    return function, selected_pkg_name

def removePackage(packageName):
    try:
        pacman_path = shutil.which('pacman')
        subprocess.run([pacman_path, '-Rns', packageName])
    except:
        return

def main():
    ensureRoot()

    global packages
    result = subprocess.run(['pacman', '-Qq'], capture_output=True, text=True)

    packages = result.stdout.splitlines()

    while True:
        function, pkg_name = selectFunction()

        if function == "Close":
            continue
        elif function == "Delete":
            print(f"Deleting package: {pkg_name}")
            removePackage(pkg_name)
            continue
