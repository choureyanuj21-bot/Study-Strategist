import csv
from datetime import datetime
import os

# --- 1. Data Structure and File Handling Globals ---
# In your final project, this file handling logic should be moved to a separate 'DataHandler' class/module.
DATA_FILE = "assignments.csv"
ASSIGNMENTS = []

def load_data():
    """Loads assignment data from the CSV file."""
    global ASSIGNMENTS
    ASSIGNMENTS.clear() # Start fresh
    if not os.path.exists(DATA_FILE):
        print("Starting with an empty assignment list.")
        return

    try:
        with open(DATA_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert string scores/points back to numbers, if applicable
                try:
                    if row.get('Score'):
                        row['Score'] = float(row['Score'])
                    row['Total_Points'] = int(row['Total_Points'])
                except ValueError:
                    # Basic error handling for corrupted data
                    print(f"Skipping corrupt row: {row}")
                    continue
                ASSIGNMENTS.append(row)
        print(f"Data loaded successfully. {len(ASSIGNMENTS)} assignments found.")
    except Exception as e:
        print(f"Error loading data: {e}")

def save_data():
    """Saves current assignment data to the CSV file."""
    if not ASSIGNMENTS:
        # If the list is empty, delete the file or just skip saving
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        return

    fieldnames = list(ASSIGNMENTS[0].keys())
    try:
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ASSIGNMENTS)
        print("\nData saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

# --- 2. Module 1: Assignment Data Management (Core CRUD Functions) ---

def add_assignment():
    """FR 1.1: Prompts user for details and adds a new assignment."""
    print("\n--- ADD NEW ASSIGNMENT ---")
    name = input("Assignment Name: ")
    course = input("Course Name: ")
    
    # Basic input validation for date (NFR 2.1 will require better handling)
    while True:
        due_date_str = input("Due Date (YYYY-MM-DD): ")
        try:
            # Check date format validity
            datetime.strptime(due_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            
    # Basic input validation for points (NFR 2.1)
    while True:
        try:
            points = int(input("Total Points: "))
            if points < 1:
                print("Points must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Total Points must be a number.")
            
    assignment = {
        'Name': name,
        'Course': course,
        'Due_Date': due_date_str,
        'Total_Points': points,
        'Status': 'Pending',
        'Score': '', # Will be updated later
    }
    ASSIGNMENTS.append(assignment)
    print(f"\n[CONFIRMATION] Assignment '{name}' successfully added.") # NFR 1.2

def update_assignment():
    """FR 1.2: Finds and updates status or score."""
    display_assignments(show_index=True)
    if not ASSIGNMENTS:
        return

    try:
        index = int(input("\nEnter the number of the assignment to UPDATE: ")) - 1
        if 0 <= index < len(ASSIGNMENTS):
            
            new_status = input("New Status (Pending/Submitted/Graded): ").title()
            ASSIGNMENTS[index]['Status'] = new_status
            
            if new_status == 'Graded':
                # NFR 2.1: You need robust score validation here
                score = input(f"Enter Score received (out of {ASSIGNMENTS[index]['Total_Points']}): ")
                ASSIGNMENTS[index]['Score'] = score
            elif new_status == 'Submitted':
                 ASSIGNMENTS[index]['Score'] = 'N/A' # Clear old score if submitted
                 
            print(f"\n[CONFIRMATION] Assignment '{ASSIGNMENTS[index]['Name']}' updated.") # NFR 1.2
            
        else:
            print("Invalid selection number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# --- 3. Module 2 & 3 Helper Functions ---

def display_assignments(assignment_list=None, title="ALL ASSIGNMENTS", show_index=False):
    """FR 2.1: Displays a list of assignments in a formatted table."""
    
    if assignment_list is None:
        assignment_list = ASSIGNMENTS
        
    if not assignment_list:
        print(f"\n--- {title} ---\nNo assignments found.")
        return

    print(f"\n--- {title} ---")
    
    # Basic Table Formatting (you can improve this with f-strings padding)
    print(f"{'#':<4}{'Assignment Name':<30}{'Course':<15}{'Due Date':<12}{'Status':<10}{'Score':<10}")
    print("-" * 81)
    
    for i, a in enumerate(assignment_list):
        index_str = f"{i + 1:<4}" if show_index else ""
        due_date = a['Due_Date']
        status = a['Status']
        score = f"{a['Score']}/{a['Total_Points']}" if a['Score'] else "N/A"
        
        print(f"{index_str}{a['Name']:<30}{a['Course']:<15}{due_date:<12}{status:<10}{score:<10}")

def filter_assignments():
    """FR 2.2: Allows filtering by Course or Status."""
    print("\n--- FILTER ASSIGNMENTS ---")
    
    filter_by = input("Filter by (C)ourse or (S)tatus? ").upper()
    
    if filter_by == 'C':
        course_name = input("Enter Course Name to filter: ")
        filtered = [a for a in ASSIGNMENTS if a['Course'].lower() == course_name.lower()]
        display_assignments(filtered, f"ASSIGNMENTS FOR COURSE: {course_name}")
        
    elif filter_by == 'S':
        status = input("Enter Status (Pending/Submitted/Graded): ").title()
        filtered = [a for a in ASSIGNMENTS if a['Status'] == status]
        display_assignments(filtered, f"ASSIGNMENTS WITH STATUS: {status}")
        
    else:
        print("Invalid filter option.")

def priority_view():
    """FR 3.3: Displays assignments due in the next 7 days."""
    
    today = datetime.now().date()
    seven_days_later = today + timedelta(days=7)
    
    def is_due_soon(assignment):
        try:
            due_date = datetime.strptime(assignment['Due_Date'], "%Y-%m-%d").date()
            return today <= due_date <= seven_days_later and assignment['Status'] == 'Pending'
        except ValueError:
            return False # Skip if date is invalid

    priority_list = [a for a in ASSIGNMENTS if is_due_soon(a)]
    display_assignments(priority_list, "PRIORITY VIEW (Due in next 7 days)")

# --- 4. Main Menu and Execution ---

def main_menu():
    """NFR 1.1: Displays the main menu."""
    print("\n\n--- STUDENT ASSIGNMENT TRACKER ---")
    print("1. Add New Assignment (Module 1)")
    print("2. Update Assignment Status/Score (Module 1)")
    print("3. View All Assignments (Module 2)")
    print("4. Filter Assignments (Module 2)")
    print("5. Priority View (Due Soon) (Module 3)")
    print("6. Exit & Save (Module 3)")
    return input("Enter your choice (1-6): ")

if __name__ == "__main__":
    from datetime import timedelta # Used by priority_view
    load_data() # FR 3.1: Load data on startup
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            add_assignment()
        elif choice == '2':
            update_assignment()
        elif choice == '3':
            display_assignments(show_index=False, title="ALL ASSIGNMENTS")
        elif choice == '4':
            filter_assignments()
        elif choice == '5':
            priority_view()
        elif choice == '6':
            save_data() # FR 3.2: Save data before exiting
            print("Thank you for using the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")