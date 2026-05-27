from package_peeker import cli
from importlib import metadata
import subprocess
import shutil
import sys
import os
import pacman

packages = []

def ensureRoot():
    if os.geteuid() == 0:
        return

    print("Elevating with sudo privledges...")

    os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

def selectPackage():
    selected_pkg = cli.viewPackages(packages)
    selected_pkg_name = packages[selected_pkg]

    if selected_pkg_name == "Search Packages":
        return selected_pkg_name, "You are searching", "Null", "Null", "Null", "Null"
    elif selected_pkg_name == "Clear Search Results":
        return selected_pkg_name, "Clearing search results", "Null", "Null", "Null", "Null"
    else:
        info_raw = pacman.get_info(selected_pkg_name)
        description = info_raw.get("Description")
        version = info_raw.get("Version")
        license = info_raw.get("Licenses")
        size = info_raw.get("Installed Size")
        date = info_raw.get("Install Date")

        return {'name': selected_pkg_name,
        'description': description,
        'version': version,
        'license': license,
        'size': size,
        'date': date}

def selectFunction(pkg_information):
    function = cli.managePackage(pkg_information['name'], pkg_information['description'], pkg_information['version'], pkg_information['license'], pkg_information['size'], pkg_information['date'])
    return function

def removePackage(packageName):
    try:
        pacman_path = shutil.which('pacman')
        subprocess.run([pacman_path, '-Rns', packageName])
    except:
        return

def getAllPackages():
    global packages
    result = subprocess.run(['pacman', '-Qq'], capture_output=True, text=True)

    newPackageList = result.stdout.splitlines()
    newPackageList.insert(0, "Search Packages")
    newPackageList.insert(1, "Clear Search Results")

    return newPackageList

def main():
    global packages
    ensureRoot()
    packages = getAllPackages()

    while True:
        pkg_information = selectPackage()

        if pkg_information['name'] == "Search Packages":
            search_query = cli.searchPackages()
            packages = [pkg for pkg in packages if pkg.startswith(search_query) or pkg == "Search Packages" or pkg == "Clear Search Results"]
            continue
        elif pkg_information['name'] == "Clear Search Results":
            packages = getAllPackages()
            continue

        function = selectFunction(pkg_information)

        if function == "Close":
            continue
        elif function == "Delete":
            print(f"Deleting package: {pkg_name}")
            removePackage(pkg_name)
            packages = getAllPackages()
            continue
