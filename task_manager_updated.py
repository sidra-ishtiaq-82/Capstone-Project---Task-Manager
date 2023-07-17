#========================== Task 17 ===============================#

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

# Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["username"] = task_components[0]
    curr_t["title"] = task_components[1]
    curr_t["description"] = task_components[2]
    curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t["completed"] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

    #====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

logged_in = False
curr_user = None

while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")


    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Defining function to register a user with their username and password.
def reg_user():
    '''Add a new user to the user.txt file'''
    new_username = input("New Username: ")
    
    # Check if the username already exists
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

     # If the new password matches the confirmed password, add the new user.
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        # Write username and password to the user.txt file.
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    else:
        print("Passwords Do Not Match, Please Try Again!")


# Defining function to add a new task.
def add_task():
    # Prompt for the name of the person assigned to the task.
    task_username = input("Name of person assigned to task: ")

    # Check if the entered username exists in the username_password dictionary.
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    # Prompt for the title and description of the task.
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

     # Prompt for the due date of the task, validating the format.
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date.
    curr_date = date.today()

# Add the data to the file task.txt and include 'No' to indicate if the task is incomplete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Append the new task to the task_list and write the task_list data to the tasks.txt file.
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t["completed"] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# Defining function to view all tasks.
def view_all():
    #In this code, for each task in the task_list, it creates a disp_str string that contains the task information, 
    # including the task title, assigned username, assigned date, due date, and task description. 
    # The disp_str is then printed, followed by a separator (---------------------) to visually separate each task.
    for t in task_list:
        print ("---------------------\n")
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print ("---------------------\n")

# Defining function for users to view and edit their own tasks.
def view_mine():
    # In this code, for each task in the task_list, it checks if the username of the task matches the curr_user. 
    # If it does, it creates a disp_str string that contains the task information, including the task number, title, 
    # assigned username, assigned date, due date, task description, and completion status. 
    # The disp_str is then printed to display the task information.
    while True:
        print("Your Tasks:")
        for i, t in enumerate(task_list):
            if t['username'] == curr_user:
                # Displaying task information.
                print ("---------------------\n")
                disp_str = f"Task {i+1}:\n"
                disp_str += f"Title: {t['title']}\n"
                disp_str += f"Assigned to: {t['username']}\n"
                disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: {t['description']}\n"
                disp_str += f"Completed: {t['completed']}\n"
                print(disp_str)
                print ("---------------------\n")
        
        task_selection = input("Enter the task number you want to select (or -1 to return to the main menu): ")
        
        # If -1 is entered, break the loop and return to the main menu.
        if task_selection == "-1":
            break
        
        try:
            task_index = int(task_selection) - 1
            selected_task = task_list[task_index]
            
            # If the selected task is already completed, inform the user and continue to the next iteration
            if selected_task['completed']:
                print("Task is already completed and cannot be edited.")
                continue
            
            edit_selection = input("Enter 'c' mark the task as complete or 'e' to edit the task: ")
            
            if edit_selection == "c":
                selected_task['completed'] = True
                print("Task marked as complete.")

    # Update the tasks.txt file by replacing "No" with "Yes" for the selected task to show its complete.
                with open("tasks.txt", "r+") as file:
                    lines = file.readlines()    # Read over all the lines in tasks.txt file.
                    task_line = lines[task_index]   # Find the line corresponding to the task being edited.
                    updated_task_line = task_line.replace(";No", ";Yes")    # Replace task status "No" with "Yes"
                    lines[task_index] = updated_task_line
                    file.seek(0)    # Move the file cursor to the beginning of the file.
                    file.writelines(lines)  # Write the updated lines back to the file.
                    file.truncate() # Truncate any remaining content beyond the updated portion.

            # Following code will execute if user selects to edit the task.
            elif edit_selection == "e":
                new_username = input("Enter the new username for the task: ")
                new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
                
                selected_task['username'] = new_username
                selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                
                print("Task successfully edited.")
               
               # Update the tasks.txt file with the updated user name and due date.
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = [] # To store the updated task information in list format for the file.
                    for t in task_list:
                        str_attrs = [
                            t['username'],
                            t['title'],
                            t['description'],
                            t['due_date'].strftime(DATETIME_STRING_FORMAT),
                            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                            "Yes" if t['completed'] else "No"
                        ]
                        task_list_to_write.append(";".join(str_attrs))  # Joins the individual attributes of the task into a single string using a ';' as the separator.
                    task_file.write("\n".join(task_list_to_write))  # combining all task strings and writing it to the file, overwriting its previous contents.


            else:
                print("Invalid input. Please try again.")
        
        except (ValueError, IndexError):
            print("Invalid task number. Please try again.")

# Defining function to generate reports when logged in as admin.
def generate_reports():
    # Following code is to generate the Task Overview Report which will be written to task_overview.txt.
    # It will calculate the 'total number of tasks', 'number of completed tasks', 'number of uncompleted tasks',
    # 'number of overdue tasks', '% of incomplete tasks', and '% of overdue tasks'. 

    total_tasks = len(task_list)    
    completed_tasks = sum(t['completed'] for t in task_list) 
    uncompleted_tasks = total_tasks - completed_tasks  
    overdue_tasks = sum(
        t['due_date'] < datetime.combine(date.today(), datetime.min.time()) and not t['completed'] for t in task_list)
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100   
    overdue_percentage = (overdue_tasks / total_tasks) * 100    

   # Create a formatted string task_overview_report, that contains the information for the report. 
    task_overview_report = f"Task Overview Report\n" \
                           f"---------------------\n" \
                           f"Total Tasks: {total_tasks}\n" \
                           f"Completed Tasks: {completed_tasks}\n" \
                           f"Uncompleted Tasks: {uncompleted_tasks}\n" \
                           f"Overdue Tasks: {overdue_tasks}\n" \
                           f"Incomplete Percentage: {incomplete_percentage:.2f}%\n" \
                           f"Overdue Percentage: {overdue_percentage:.2f}%\n"

     # Write the task_overview_report to task_overview.txt file.
    with open("task_overview.txt", "w") as task_report_file:
        task_report_file.write(task_overview_report)

    # following code is to generate the User Overview Report which will be written to user_overview.txt.
    # It will calculate the 'total number of users', 'total users tasks', '% of tasks assigned to users',
    # '% of tasks completed', '% of tasks incomplete', and '% of tasks overdue'.
    total_users = len(username_password)

    with open("user_overview.txt", "w") as user_report_file:
        # Iterate over each username and password in the username_password dictionary
        for username, password in username_password.items():
            user_tasks = [t for t in task_list if t['username'] == username]
            total_user_tasks = len(user_tasks)
            percentage_assigned = (total_user_tasks / total_tasks) * 100

            # Initialize default values for completion and overdue percentages.
            percentage_completed = 0  # Default value when there are no tasks
            percentage_incomplete = 100
            percentage_overdue = 0

        # Calculate completion and overdue percentages only if the user has tasks assigned.
            if total_user_tasks > 0:
                percentage_completed = (sum(t['completed'] for t in user_tasks) / total_user_tasks) * 100
                percentage_incomplete = 100 - percentage_completed
                overdue_user_tasks = sum(
                    t['due_date'] < datetime.combine(date.today(), datetime.min.time()) and not t['completed']
                    for t in user_tasks)
                percentage_overdue = (overdue_user_tasks / total_user_tasks) * 100

# Create a formatted string user_overview_report, that contains the information for the report. 
            user_overview_report = f"User Overview Report\n" \
                                   f"---------------------\n" \
                                   f"Total Users: {total_users}\n" \
                                   f"Total Tasks: {total_tasks}\n" \
                                   f"Username: {username}\n" \
                                   f"Total Tasks Assigned: {total_user_tasks}\n" \
                                   f"Percentage Assigned: {percentage_assigned:.2f}%\n" \
                                   f"Percentage Completed: {percentage_completed:.2f}%\n" \
                                   f"Percentage Incomplete: {percentage_incomplete:.2f}%\n" \
                                   f"Percentage Overdue: {percentage_overdue:.2f}%\n" \
                                   f"---------------------\n"

    # Write the user overview report to user_overview.txt file
            user_report_file.write(user_overview_report)    


# Defining function to display statistics when logged in as admin.
def display_statistics():
    # Read task overview report from file.
    with open("task_overview.txt", "r") as task_report_file:
        task_overview_report = task_report_file.read()

    # Read user overview report from file.
    with open("user_overview.txt", "r") as user_report_file:
        user_overview_report = user_report_file.read()

    # Print the task_overview and user_overview reports.
    print("---------------------")
    print(task_overview_report)
    print("---------------------")
    print(user_overview_report)

# Printing/Displaying the Main Menu.
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Register user
a - Add task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()  #converting user input/selection to a uniform lower case.

    # If selection is 'r', then the funtion 'reg_user'(register a new user and password) will be called and executed.
    if menu == 'r':
        reg_user()

    # Else if selection is 'a', then the function 'add_task' (adding a new task) will be called and executed.    
    elif menu == 'a':
        add_task()
        
    # Else if selection is 'va', then the function 'view_all' (viewing all tasks) will be called and executed.    
    elif menu == 'va':
        view_all()
        
    # Else if selection is 'vm', then the function 'view_mine' (viewing and editing user's own tasks) will be called and executed.
    elif menu == 'vm':
        view_mine()

    # Else if selection is 'gr', then the function 'generate_reports' will generate reports in 
    # task_overview.txt and user_overview.txt files.    
    # Only when logged in as admin, the user will be able to execute the 'gr' and 'ds' options.
    # If other users try to use this option they will get the message 'You Have Made a Wrong Choice. Please Try Again!'.    
    elif menu == 'gr' and curr_user == 'admin':
        generate_reports()
        
    # Else if selection is 'ds', then the function 'display_statistics' will print/display the contents of
    # task_overview.txt and user_overview.txt files to the terminal/screen.    
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()

    # Selection to exit the program.    
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You Have Made A Wrong Choice. Please Try Again!")

