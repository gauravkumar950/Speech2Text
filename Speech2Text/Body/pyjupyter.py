import os
def runshell(text):
    # Define the directory you want to change to
    directory = r"C:\Users\kesha\miniconda3"

    # Define the command to activate the virtual environment (assuming Miniconda)
    activate_command = r'scripts\activate.bat pydata-book'

    # Define the command you want to run in the activated environment
    jupyter_notebook_command = text

    # Open a new Command Prompt window and run the combined command
    os.system(f'start cmd /k "cd /d {directory} && {activate_command} && {jupyter_notebook_command}"')
