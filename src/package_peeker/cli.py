from simple_term_menu import TerminalMenu
import subprocess

def viewPackages(packages):
    subprocess.run('clear')

    terminal_menu = TerminalMenu(packages, title="Installed Packages")
    menu_entry_index = terminal_menu.show()

    if menu_entry_index is not None:
        return menu_entry_index

def managePackage(package, description, version, license, size, date):
    subprocess.run('clear')

    print(f"Editing package: {package}\n")
    print(f"{description}\n")
    print(f"Version: {version}")
    print(f"License: {license}")
    print(f"Size: {size}")
    print(f"Date: {date}\n")

    menu_items = ["Delete", "Close"]
    terminal_menu = TerminalMenu(menu_items, title=package)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index is not None:
        return menu_items[menu_entry_index]

def searchPackages():
    print("Search packages:")
    return input("[?]: ")

if __name__ == "__main__":
    viewPackages()
