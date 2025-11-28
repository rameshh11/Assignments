"""
================================================================================
ATTENDANCE TRACKER - PYTHON ASSIGNMENT
================================================================================
Name: Ramesh Kumar
Roll No: 2501940086
Course: MCA (AI & ML)
Assignment: Attendance Tracker System
Description: A comprehensive tool to record and manage student attendance
             with validation, summary generation, and file export features.
================================================================================
"""
import os
from datetime import datetime

# ANSI Color codes for enhanced formatting
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_welcome():
    """Display welcome message and tool purpose"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print("STUDENT ATTENDANCE TRACKING SYSTEM")
    print(f"{'='*70}{Colors.ENDC}")
    print(f"\n{Colors.OKCYAN}Welcome to the Attendance Tracker!{Colors.ENDC}")
    print(f"{Colors.OKBLUE}This tool helps you efficiently record and manage student attendance.")
    print("Features:")
    print("  > Record student check-in times")
    print("  > Validate entries to prevent errors")
    print("  > Generate formatted attendance reports")
    print("  > Calculate absentee statistics")
    print(f"  > Export records to file{Colors.ENDC}\n")


def validate_name(name, attendance_dict):
    """
    Validate student name
    Returns: (is_valid, error_message)
    """
    # Check if name is empty
    if not name or name.strip() == "":
        return False, f"{Colors.FAIL}Error: Name cannot be empty.{Colors.ENDC}"
    
    # Check for duplicates
    if name in attendance_dict:
        return False, f"{Colors.WARNING}Warning: {name} has already been recorded.{Colors.ENDC}"
    
    return True, ""


def validate_time(time_str):
    """
    Validate time format
    Returns: (is_valid, error_message)
    """
    if not time_str or time_str.strip() == "":
        return False, f"{Colors.FAIL}Error: Time cannot be empty.{Colors.ENDC}"
    
    # Basic validation - checking if time has some content
    # More sophisticated validation could use regex or datetime parsing
    time_str = time_str.strip()
    if len(time_str) < 4:
        return False, f"{Colors.WARNING}Warning: Time format seems invalid. Please use format like '09:15 AM'{Colors.ENDC}"
    
    return True, ""


def collect_attendance():
    """
    Main function to collect attendance data with validation
    Returns: dictionary of attendance records
    """
    attendance = {}
    
    # Get number of entries
    while True:
        try:
            num_entries = int(input(f"\n{Colors.OKGREEN}How many students do you want to record? {Colors.ENDC}"))
            if num_entries <= 0:
                print(f"{Colors.WARNING}Please enter a positive number.{Colors.ENDC}")
                continue
            break
        except ValueError:
            print(f"{Colors.FAIL}Invalid input! Please enter a number.{Colors.ENDC}")
    
    # Collect attendance data
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}--- Recording Attendance ---{Colors.ENDC}")
    
    for i in range(num_entries):
        print(f"\n{Colors.OKBLUE}Entry {i + 1} of {num_entries}:{Colors.ENDC}")
        
        # Get and validate student name
        while True:
            name = input(f"  Enter student name: ").strip()
            is_valid, error_msg = validate_name(name, attendance)
            
            if is_valid:
                break
            else:
                print(f"  {error_msg}")
                print(f"  {Colors.OKCYAN}Please try again.{Colors.ENDC}")
        
        # Get and validate check-in time
        while True:
            check_in_time = input(f"  Enter check-in time (e.g., 09:15 AM): ").strip()
            is_valid, error_msg = validate_time(check_in_time)
            
            if is_valid:
                break
            else:
                print(f"  {error_msg}")
                print(f"  {Colors.OKCYAN}Please try again.{Colors.ENDC}")
        
        # Store the record
        attendance[name] = check_in_time
        print(f"  {Colors.OKGREEN}Recorded successfully!{Colors.ENDC}")
    
    return attendance


def display_attendance_summary(attendance, total_students=None):
    """
    Display formatted attendance summary
    """
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print("                    ATTENDANCE SUMMARY REPORT")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    # Header
    print(f"{Colors.BOLD}{Colors.OKCYAN}{'Student Name':<30}{'Check-in Time':<20}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'-'*50}{Colors.ENDC}")
    
    # Display each entry
    for name, time in attendance.items():
        print(f"{Colors.OKGREEN}{name:<30}{time:<20}{Colors.ENDC}")
    
    print(f"{Colors.BOLD}{'-'*50}{Colors.ENDC}")
    
    # Statistics
    total_present = len(attendance)
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}Total Students Present: {total_present}{Colors.ENDC}")
    
    # Calculate absentees if total students provided
    if total_students is not None and total_students > 0:
        total_absent = total_students - total_present
        print(f"{Colors.WARNING}{Colors.BOLD}Total Students Absent: {total_absent}{Colors.ENDC}")
        
        if total_absent > 0:
            attendance_rate = (total_present / total_students) * 100
            print(f"{Colors.OKCYAN}Attendance Rate: {attendance_rate:.1f}%{Colors.ENDC}")
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def save_to_file(attendance, total_students=None):
    """
    Save attendance record to a text file
    """
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(script_dir, 'attendance_log.txt')
        
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%B %d, %Y")
        formatted_time = current_datetime.strftime("%I:%M:%S %p")
        
        with open(log_file_path, 'w', encoding='utf-8') as file:
            file.write("="*70 + "\n")
            file.write("            STUDENT ATTENDANCE RECORD\n")
            file.write("="*70 + "\n\n")
            file.write(f"Report Generated: {formatted_date} at {formatted_time}\n\n")
            
            file.write(f"{'Student Name':<30}{'Check-in Time':<20}\n")
            file.write("-"*50 + "\n")
            
            for name, time in attendance.items():
                file.write(f"{name:<30}{time:<20}\n")
            
            file.write("-"*50 + "\n")
            file.write(f"\nTotal Students Present: {len(attendance)}\n")
            
            if total_students is not None and total_students > 0:
                total_absent = total_students - len(attendance)
                file.write(f"Total Students Absent: {total_absent}\n")
                attendance_rate = (len(attendance) / total_students) * 100
                file.write(f"Attendance Rate: {attendance_rate:.1f}%\n")
            
            file.write("\n" + "="*70 + "\n")
            file.write("End of Report\n")
            file.write("="*70 + "\n")
        
        print(f"{Colors.OKGREEN}{Colors.BOLD}Attendance log saved successfully to 'attendance_log.txt'{Colors.ENDC}")
        return True
        
    except Exception as e:
        print(f"{Colors.FAIL}Error saving file: {e}{Colors.ENDC}")
        return False


def main():
    """
    Main program execution
    """
    # Task 1: Welcome message
    print_welcome()
    
    # Task 2 & 3: Collect and validate attendance data
    attendance_records = collect_attendance()
    
    # Task 5: Optional absentee calculation
    total_class_size = None
    print(f"\n{Colors.OKCYAN}Would you like to calculate absentee statistics? (yes/no): {Colors.ENDC}", end="")
    calc_absentees = input().strip().lower()
    
    if calc_absentees in ['yes', 'y']:
        while True:
            try:
                total_class_size = int(input(f"{Colors.OKGREEN}Enter total number of students in the class: {Colors.ENDC}"))
                if total_class_size < len(attendance_records):
                    print(f"{Colors.WARNING}Total class size cannot be less than present students ({len(attendance_records)}).{Colors.ENDC}")
                    continue
                break
            except ValueError:
                print(f"{Colors.FAIL}Invalid input! Please enter a number.{Colors.ENDC}")
    
    # Task 4: Display attendance summary
    display_attendance_summary(attendance_records, total_class_size)
    
    # Task 6: Save to file (Bonus)
    print(f"{Colors.OKCYAN}Would you like to save the attendance report to a file? (yes/no): {Colors.ENDC}", end="")
    save_choice = input().strip().lower()
    
    if save_choice in ['yes', 'y']:
        save_to_file(attendance_records, total_class_size)
    
    # Exit message
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Thank you for using the Attendance Tracker!{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Session completed successfully.{Colors.ENDC}\n")


# Program entry point
if __name__ == "__main__":
    main()
3