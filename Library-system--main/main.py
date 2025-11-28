"""
Name: Replace with your name
Date: 2025-11-19
Assignment: Library System - main.py
"""

from library import Library

def print_welcome():
    print("******************************************")
    print("  Welcome to the Library Inventory System ")
    print("      Programming for Problem Solving     ")
    print("******************************************\n")

def main_menu():
    lib = Library()
    lib.load_data()
    print_welcome()

    while True:
        print("\nMenu:")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Library Report")
        print("6. List All Books")
        print("7. List All Members")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            ok = lib.add_book(title=title, author=author, isbn=isbn)
            if ok:
                lib.save_data()
                print("Book added successfully.")
            else:
                print("A book with that ISBN already exists.")

        elif choice == "2":
            name = input("Member Name: ").strip()
            member_id = input("Member ID: ").strip()
            ok = lib.register_member(name=name, member_id=member_id)
            if ok:
                lib.save_data()
                print("Member registered successfully.")
            else:
                print("Member ID already exists.")

        elif choice == "3":
            member_id = input("Member ID: ").strip()
            isbn = input("ISBN of book to borrow: ").strip()
            msg = lib.lend_book(member_id=member_id, isbn=isbn)
            print(msg)

        elif choice == "4":
            member_id = input("Member ID: ").strip()
            isbn = input("ISBN of book to return: ").strip()
            msg = lib.take_return(member_id=member_id, isbn=isbn)
            print(msg)

        elif choice == "5":
            print("\nLibrary Report")
            print("-----------------")
            print(lib.library_report())

        elif choice == "6":
            print("\nBooks:")
            for s in lib.list_all_books():
                print(" -", s)

        elif choice == "7":
            print("\nMembers:")
            for s in lib.list_all_members():
                print(" -", s)

        elif choice == "8":
            print("Saving data and exiting...")
            lib.save_data()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main_menu()
