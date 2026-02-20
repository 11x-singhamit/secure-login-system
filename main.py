import tkinter as tk
from src.gui import launch_gui
from src.cli import run_cli
from src.admin_gui import launch_admin_gui
from src.security import init_databases


def show_menu():

    print("\nSecure Login System")
    print("========================")
    print("1. Launch GUI Login")
    print("2. Launch CLI Login")
    print("3. Launch Admin Dashboard")
    print("4. Exit")

    choice = input("\nEnter choice (1-4): ")

    return choice


def main():

    init_databases()

    while True:

        choice = show_menu()

        if choice == "1":

            launch_gui()

        elif choice == "2":

            run_cli()

        elif choice == "3":

            launch_admin_gui()

        elif choice == "4":

            print("Exiting system.")
            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    main()
