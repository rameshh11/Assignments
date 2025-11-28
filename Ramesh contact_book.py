"""
Contact Manager Application
Name: Ramesh Kumar
Roll No: 2501940086
Course: MCA (AI & ML)
Project Title: Contact Book Management System
"""

# ============================================================================
# IMPORT STATEMENTS
# ============================================================================
import csv          # For reading/writing CSV files
import json         # For JSON import/export functionality
from datetime import datetime  # For timestamping log entries
import os           # For file system operations

# ============================================================================
# CONFIGURATION - Set working directory to script location
# ============================================================================
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Change working directory to script location
os.chdir(SCRIPT_DIR)

# ============================================================================
# COLOR CODES FOR TERMINAL OUTPUT (ANSI Escape Sequences)
# ============================================================================
class Colors:
    """Class containing ANSI color codes for terminal output"""
    # Text colors
    RED = '\033[91m'        # For errors and warnings
    GREEN = '\033[92m'      # For success messages
    YELLOW = '\033[93m'     # For warnings and prompts
    BLUE = '\033[94m'       # For information and headers
    MAGENTA = '\033[95m'    # For menu items
    CYAN = '\033[96m'       # For contact details
    WHITE = '\033[97m'      # For general text
    
    # Text styles
    BOLD = '\033[1m'        # Bold text
    UNDERLINE = '\033[4m'   # Underlined text
    
    # Reset code
    RESET = '\033[0m'       # Reset to default color



# ============================================================================
# TASK 2: CREATE AND SAVE CONTACTS
# ============================================================================
def create_contact():
    """
    Accept contact details from user and save to CSV file.
    This function prompts for name, phone, and email, validates the input,
    and stores the contact in contacts.csv file.
    """
    try:
        # Display section header with color
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
        print(f"           ADD NEW CONTACT")
        print(f"{'='*60}{Colors.RESET}")
        
        # Prompt user for contact details with colored prompts
        print(f"\n{Colors.YELLOW}Please enter the contact details:{Colors.RESET}")
        name = input(f"{Colors.WHITE}Name: {Colors.RESET}").strip()
        phone = input(f"{Colors.WHITE}Phone Number: {Colors.RESET}").strip()
        email = input(f"{Colors.WHITE}Email Address: {Colors.RESET}").strip()
        
        # Validate inputs - ensure all fields are filled
        if not name or not phone or not email:
            raise ValueError("All fields (Name, Phone, Email) are required!")
        
        # Store contact as dictionary (key-value pairs)
        contact = {
            "Name": name,
            "Phone": phone,
            "Email": email
        }
        
        # Check if CSV file already exists
        file_exists = os.path.exists('contacts.csv')
        
        # Open CSV file in append mode to add new contact
        with open('contacts.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write header row only if file is newly created
            if not file_exists:
                writer.writeheader()
            
            # Write the contact data to CSV
            writer.writerow(contact)
        
        # Display success message with green color
        print(f"\n{Colors.GREEN}SUCCESS: Contact '{Colors.BOLD}{name}{Colors.RESET}{Colors.GREEN}' added successfully!{Colors.RESET}")
        
        # Log the successful operation
        log_error("INFO", f"Contact '{name}' added successfully")
        
        # Ask if user wants to add another contact (interactive feature)
        another = input(f"\n{Colors.YELLOW}Add another contact? (y/n): {Colors.RESET}").strip().lower()
        if another == 'y':
            create_contact()  # Recursive call for continuous adding
        
    except Exception as e:
        # Log the error to error_log.txt
        log_error("ERROR", f"Error adding contact: {str(e)}")
        # Display error message in red
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# ============================================================================
# TASK 3: READ AND DISPLAY CONTACTS
# ============================================================================
def display_contacts():
    """
    Read contacts from CSV file and display in tabular format.
    Includes proper exception handling for file not found and empty files.
    """
    try:
        # Check if contacts.csv file exists
        if not os.path.exists('contacts.csv'):
            raise FileNotFoundError("No contacts file found. Please add contacts first.")
        
        # Open and read the CSV file
        with open('contacts.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)  # Convert to list to check length
            
            # Check if file is empty
            if not contacts:
                print(f"\n{Colors.YELLOW}Warning: Contact list is empty!{Colors.RESET}")
                return
            
            # Display header with attractive formatting
            print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*80}")
            print(f"                    ALL CONTACTS")
            print(f"{'='*80}{Colors.RESET}")
            
            # Table header with cyan color
            print(f"{Colors.CYAN}{Colors.BOLD}")
            print(f"{'Name':<30} {'Phone':<20} {'Email':<30}")
            print(f"{'-'*80}{Colors.RESET}")
            
            # Display each contact with alternating colors for better readability
            for idx, contact in enumerate(contacts):
                # Alternate between white and cyan for each row
                color = Colors.WHITE if idx % 2 == 0 else Colors.CYAN
                print(f"{color}{contact['Name']:<30} {contact['Phone']:<20} {contact['Email']:<30}{Colors.RESET}")
            
            # Display footer with total count
            print(f"{Colors.BLUE}{Colors.BOLD}{'-'*80}")
            print(f"Total Contacts: {Colors.GREEN}{len(contacts)}{Colors.RESET}")
            print(f"{Colors.BLUE}{'='*80}{Colors.RESET}\n")
            
    except FileNotFoundError as e:
        # Log and display file not found error
        log_error("ERROR", str(e))
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")
    except Exception as e:
        # Log and display any other errors
        log_error("ERROR", f"Error displaying contacts: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# ============================================================================
# TASK 4: SEARCH, UPDATE, AND DELETE CONTACTS
# ============================================================================

# -------------------- SEARCH CONTACT --------------------
def search_contact():
    """
    Search for a contact by name (case-insensitive, partial match).
    Displays all matching contacts with their full details.
    """
    try:
        # Check if contacts file exists
        if not os.path.exists('contacts.csv'):
            raise FileNotFoundError("No contacts file found.")
        
        # Display search header
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*60}")
        print(f"           SEARCH CONTACT")
        print(f"{'='*60}{Colors.RESET}")
        
        # Get search term from user
        search_name = input(f"\n{Colors.YELLOW}Enter name to search: {Colors.RESET}").strip()
        
        # Read all contacts from CSV
        with open('contacts.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
            
            found = False
            # Search through contacts (case-insensitive)
            for contact in contacts:
                if search_name.lower() in contact['Name'].lower():
                    # Display matching contact with cyan color
                    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
                    print(f"Name:  {Colors.WHITE}{contact['Name']}{Colors.RESET}")
                    print(f"{Colors.CYAN}Phone: {Colors.WHITE}{contact['Phone']}{Colors.RESET}")
                    print(f"{Colors.CYAN}Email: {Colors.WHITE}{contact['Email']}{Colors.RESET}")
                    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
                    found = True
            
            # If no matches found
            if not found:
                print(f"\n{Colors.YELLOW}No contact found with name '{search_name}'{Colors.RESET}")
                
    except Exception as e:
        # Log and display error
        log_error("ERROR", f"Error searching contact: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# -------------------- UPDATE CONTACT --------------------
def update_contact():
    """
    Update the phone number of an existing contact.
    Prompts for contact name and new phone number.
    """
    try:
        # Check if contacts file exists
        if not os.path.exists('contacts.csv'):
            raise FileNotFoundError("No contacts file found.")
        
        # Display update header
        print(f"\n{Colors.YELLOW}{Colors.BOLD}{'='*60}")
        print(f"           UPDATE CONTACT")
        print(f"{'='*60}{Colors.RESET}")
        
        # Get contact name to update
        name = input(f"\n{Colors.YELLOW}Enter name of contact to update: {Colors.RESET}").strip()
        
        # Read all contacts from CSV
        with open('contacts.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        
        updated = False
        # Find and update the contact
        for contact in contacts:
            if contact['Name'].lower() == name.lower():
                # Display current phone number
                print(f"{Colors.CYAN}Current Phone: {contact['Phone']}{Colors.RESET}")
                
                # Get new phone number
                new_phone = input(f"{Colors.YELLOW}Enter new phone number: {Colors.RESET}").strip()
                contact['Phone'] = new_phone
                updated = True
                
                # Display success message
                print(f"\n{Colors.GREEN}SUCCESS: Contact '{Colors.BOLD}{name}{Colors.RESET}{Colors.GREEN}' updated successfully!{Colors.RESET}")
                log_error("INFO", f"Contact '{name}' updated")
                break
        
        # If contact not found
        if not updated:
            print(f"\n{Colors.YELLOW}No contact found with name '{name}'{Colors.RESET}")
            return
        
        # Write updated contacts back to CSV file
        with open('contacts.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)
            
    except Exception as e:
        # Log and display error
        log_error("ERROR", f"Error updating contact: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# -------------------- DELETE CONTACT --------------------
def delete_contact():
    """
    Delete a contact from the contact list by name.
    Prompts for confirmation before deletion.
    """
    try:
        # Check if contacts file exists
        if not os.path.exists('contacts.csv'):
            raise FileNotFoundError("No contacts file found.")
        
        # Display delete header
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*60}")
        print(f"           DELETE CONTACT")
        print(f"{'='*60}{Colors.RESET}")
        
        # Get contact name to delete
        name = input(f"\n{Colors.YELLOW}Enter name of contact to delete: {Colors.RESET}").strip()
        
        # Read all contacts from CSV
        with open('contacts.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        
        # Find the contact to display before deletion
        contact_to_delete = None
        for contact in contacts:
            if contact['Name'].lower() == name.lower():
                contact_to_delete = contact
                break
        
        # If contact not found
        if not contact_to_delete:
            print(f"\n{Colors.YELLOW}No contact found with name '{name}'{Colors.RESET}")
            return
        
        # Display contact details and ask for confirmation
        print(f"\n{Colors.CYAN}Contact Details:")
        print(f"Name:  {contact_to_delete['Name']}")
        print(f"Phone: {contact_to_delete['Phone']}")
        print(f"Email: {contact_to_delete['Email']}{Colors.RESET}")
        
        # Confirmation prompt (interactive feature)
        confirm = input(f"\n{Colors.RED}Are you sure you want to delete this contact? (y/n): {Colors.RESET}").strip().lower()
        
        if confirm != 'y':
            print(f"\n{Colors.YELLOW}Deletion cancelled.{Colors.RESET}")
            return
        
        # Remove the contact from list
        original_count = len(contacts)
        contacts = [c for c in contacts if c['Name'].lower() != name.lower()]
        
        # Write updated contacts back to CSV file
        with open('contacts.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)
        
        # Display success message
        print(f"\n{Colors.GREEN}SUCCESS: Contact '{Colors.BOLD}{name}{Colors.RESET}{Colors.GREEN}' deleted successfully!{Colors.RESET}")
        log_error("INFO", f"Contact '{name}' deleted")
        
    except Exception as e:
        # Log and display error
        log_error("ERROR", f"Error deleting contact: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# ============================================================================
# TASK 5: SAVE AND LOAD CONTACTS IN JSON FORMAT
# ============================================================================

# -------------------- EXPORT TO JSON --------------------
def export_to_json():
    """
    Export all contacts from CSV to JSON format.
    Creates a formatted JSON file with proper indentation.
    """
    try:
        # Check if contacts file exists
        if not os.path.exists('contacts.csv'):
            raise FileNotFoundError("No contacts file found.")
        
        # Display export header
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
        print(f"           EXPORT TO JSON")
        print(f"{'='*60}{Colors.RESET}")
        
        # Read contacts from CSV
        with open('contacts.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
        
        # Check if there are contacts to export
        if not contacts:
            print(f"\n{Colors.YELLOW}No contacts to export!{Colors.RESET}")
            return
        
        # Write contacts to JSON file with proper formatting (indent=4)
        with open('contacts.json', 'w', encoding='utf-8') as file:
            json.dump(contacts, file, indent=4)
        
        # Display success message
        print(f"\n{Colors.GREEN}SUCCESS: {Colors.BOLD}{len(contacts)}{Colors.RESET}{Colors.GREEN} contacts exported to 'contacts.json' successfully!{Colors.RESET}")
        log_error("INFO", f"Exported {len(contacts)} contacts to JSON")
        
    except Exception as e:
        # Log and display error
        log_error("ERROR", f"Error exporting to JSON: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# -------------------- IMPORT FROM JSON --------------------
def import_from_json():
    """
    Import and display contacts from JSON file.
    Validates JSON format and displays contacts in tabular format.
    """
    try:
        # Check if JSON file exists
        if not os.path.exists('contacts.json'):
            raise FileNotFoundError("No JSON file found.")
        
        # Display import header
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}")
        print(f"           IMPORT FROM JSON")
        print(f"{'='*60}{Colors.RESET}")
        
        # Read contacts from JSON file
        with open('contacts.json', 'r', encoding='utf-8') as file:
            contacts = json.load(file)
        
        # Check if JSON file is empty
        if not contacts:
            print(f"\n{Colors.YELLOW}JSON file is empty!{Colors.RESET}")
            return
        
        # Display contacts from JSON in tabular format
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'='*80}")
        print(f"                 CONTACTS FROM JSON")
        print(f"{'='*80}{Colors.RESET}")
        
        # Table header
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print(f"{'Name':<30} {'Phone':<20} {'Email':<30}")
        print(f"{'-'*80}{Colors.RESET}")
        
        # Display each contact with alternating colors
        for idx, contact in enumerate(contacts):
            color = Colors.WHITE if idx % 2 == 0 else Colors.CYAN
            print(f"{color}{contact['Name']:<30} {contact['Phone']:<20} {contact['Email']:<30}{Colors.RESET}")
        
        # Display footer with total count
        print(f"{Colors.MAGENTA}{Colors.BOLD}{'-'*80}")
        print(f"Total Contacts: {Colors.GREEN}{len(contacts)}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*80}{Colors.RESET}\n")
        
        log_error("INFO", f"Imported {len(contacts)} contacts from JSON")
        
    except FileNotFoundError as e:
        # Log and display file not found error
        log_error("ERROR", str(e))
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")
    except json.JSONDecodeError as e:
        # Log and display JSON format error
        log_error("ERROR", f"Invalid JSON format: {str(e)}")
        print(f"\n{Colors.RED}ERROR: Invalid JSON format{Colors.RESET}")
    except Exception as e:
        # Log and display any other errors
        log_error("ERROR", f"Error importing from JSON: {str(e)}")
        print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.RESET}")


# ============================================================================
# TASK 6: ERROR LOGGING
# ============================================================================
def log_error(level, message):
    """
    Log errors and operations to error_log.txt file.
    Creates structured log entries with timestamp, level, and message.
    
    Args:
        level (str): Log level (INFO, ERROR, WARNING)
        message (str): Message to log
    """
    try:
        # Get current timestamp in readable format
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format log entry with timestamp, level, and message
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # Append log entry to error_log.txt file
        with open('error_log.txt', 'a', encoding='utf-8') as file:
            file.write(log_entry)
            
    except Exception as e:
        # If logging fails, print warning (don't crash the program)
        print(f"{Colors.YELLOW}⚠ Warning: Could not write to log file: {str(e)}{Colors.RESET}")


# ============================================================================
# MAIN MENU AND APPLICATION ENTRY POINT
# ============================================================================
def main():
    """
    Main function with interactive menu-driven interface.
    Displays menu options and handles user choices.
    Runs in a loop until user chooses to exit.
    """
    while True:
        # Display main menu with attractive colors
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}")
        print(f"{Colors.GREEN}          CONTACT BOOK MANAGEMENT SYSTEM{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        
        # Menu options with numbers for better visual appeal
        print(f"{Colors.MAGENTA}{Colors.BOLD}1.{Colors.RESET} {Colors.WHITE}Add New Contact{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}2.{Colors.RESET} {Colors.WHITE}Display All Contacts{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}3.{Colors.RESET} {Colors.WHITE}Search Contact{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}4.{Colors.RESET} {Colors.WHITE}Update Contact{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}5.{Colors.RESET} {Colors.WHITE}Delete Contact{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}6.{Colors.RESET} {Colors.WHITE}Export to JSON{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}7.{Colors.RESET} {Colors.WHITE}Import from JSON{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}8.{Colors.RESET} {Colors.WHITE}Exit{Colors.RESET}")
        
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
        
        # Get user's choice
        choice = input(f"{Colors.YELLOW}Enter your choice (1-8): {Colors.RESET}").strip()
        
        # Handle user's choice using if-elif-else structure
        if choice == '1':
            create_contact()  # Add new contact
        elif choice == '2':
            display_contacts()  # Show all contacts
        elif choice == '3':
            search_contact()  # Search for contact
        elif choice == '4':
            update_contact()  # Update existing contact
        elif choice == '5':
            delete_contact()  # Delete contact
        elif choice == '6':
            export_to_json()  # Export contacts to JSON
        elif choice == '7':
            import_from_json()  # Import contacts from JSON
        elif choice == '8':
            # Exit the application
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}")
            print(f"     Thank you for using Contact Book Management System!")
            print(f"{'='*70}{Colors.RESET}\n")
            log_error("INFO", "Application closed")
            break  # Exit the while loop
        else:
            # Handle invalid input
            print(f"\n{Colors.RED}Invalid choice! Please enter a number between 1-8.{Colors.RESET}")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    """
    This block executes only when the script is run directly.
    Logs application start and calls the main function.
    """
    # Log application start
    log_error("INFO", "Application started")
    
    # Display welcome message
    print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}")
    print(f"     Welcome to Contact Book Management System!")
    print(f"{'='*70}{Colors.RESET}")
    
    # Start the main application
    main()

