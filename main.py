import csv
import os
import re

FILE_NAME = "contacts.csv"
HEADERS = ["Name", "Phone", "Email"]


# file handeling stuff

def initialize_file():
    """Create CSV file with headers if missing."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
            csv.DictWriter(f, fieldnames=HEADERS).writeheader()


def load_contacts():
    """Load all contacts from the CSV."""
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, 'r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_contacts(contacts):
    """Write contacts back to CSV."""
    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(contacts)


# vaidators bla bla bla

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) > 0


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def contact_exists(name, contacts):
    return any(c['Name'].lower() == name.lower() for c in contacts)


# crud operations

def view_contacts():
    """Display contacts nicely."""
    contacts = load_contacts()
    if not contacts:
        print("\nNo contacts found.")
        return

    print("\n" + "="*65)
    print(f"{'NAME':<25} | {'PHONE':<15} | {'EMAIL':<20}")
    print("-" * 65)

    for c in contacts:
        print(f"{c['Name']:<25} | {c['Phone']:<15} | {c['Email']:<20}")

    print("="*65)


def add_contact():
    contacts = load_contacts()
    print("\n--- Add New Contact ---")

   
    while True:
        name = input("Enter Name: ").strip()
        if not name:
            print("Name cannot be empty.")
            continue
        if contact_exists(name, contacts):
            print(f"Error: Contact '{name}' already exists.")
            return
        break

    
    while True:
        phone = input("Enter Phone (digits only): ").strip()
        if is_valid_phone(phone):
            break
        print("Invalid phone. Please enter digits only.")

    
    while True:
        email = input("Enter Email: ").strip()
        if is_valid_email(email):
            break
        print("Invalid email format. Please try again (e.g., user@example.com).")

    contacts.append({"Name": name, "Phone": phone, "Email": email})
    save_contacts(contacts)

    print(f"\nSuccess: Contact '{name}' added!")


def search_contact():
    query = input("\nEnter name to search: ").strip().lower()
    contacts = load_contacts()

    print(f"\nSearch Results for '{query}':")
    print("-" * 65)

    found_any = False
    for c in contacts:
        if query in c['Name'].lower():
            print(f"Name: {c['Name']}, Phone: {c['Phone']}, Email: {c['Email']}")
            found_any = True

    if not found_any:
        print("No matching contacts found.")


def update_contact():
    contacts = load_contacts()
    target = input("\nEnter the exact name of the contact to update: ").strip()

    index = next((i for i, c in enumerate(contacts) if c['Name'].lower() == target.lower()), -1)
    if index == -1:
        print("Contact not found.")
        return

    print(f"\nUpdating contact: {contacts[index]['Name']}")
    print("1. Update Name")
    print("2. Update Phone")
    print("3. Update Email")
    print("4. Cancel")

    choice = input("Choose an option: ")

    if choice == '1':
        new_name = input("Enter new name: ").strip()
        if new_name.lower() != contacts[index]['Name'].lower() and contact_exists(new_name, contacts):
            print("Error: That name already exists.")
            return
        contacts[index]['Name'] = new_name

    elif choice == '2':
        while True:
            new_phone = input("Enter new phone: ").strip()
            if is_valid_phone(new_phone):
                contacts[index]['Phone'] = new_phone
                break
            print("Invalid phone. Digits only.")

    elif choice == '3':
        while True:
            new_email = input("Enter new email: ").strip()
            if is_valid_email(new_email):
                contacts[index]['Email'] = new_email
                break
            print("Invalid email format.")

    elif choice == '4':
        return
    else:
        print("Invalid option.")
        return

    save_contacts(contacts)
    print("\nContact updated successfully.")


def delete_contact():
    contacts = load_contacts()
    name_to_delete = input("\nEnter the name of the contact to delete: ").strip().lower()

    new_list = [c for c in contacts if c['Name'].lower() != name_to_delete]

    if len(new_list) == len(contacts):
        print("Contact not found.")
        return

    save_contacts(new_list)
    print(f"\nContact '{name_to_delete}' deleted successfully.")


# the main loop

def main_menu():
    initialize_file()

    while True:
        print("\n=== CONTACT BOOK MANAGER ===")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            add_contact()
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main_menu()


