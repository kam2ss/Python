""" Password Manager Project for CS50 with Python """

from tabulate import tabulate
import bcrypt
import os
import pyfiglet
import json


def main():
    text = "Passwd Manager"
    print(pyfiglet.figlet_format(text))
    create_master_password()
    validate_master_password()
    select_mode()


def create_master_password():
    if not os.path.exists("master_password.txt"):
        while True:
            """ Creating master password to access the password vault """
            password1 = input("Create a master password: ")
            password2 = input("Confirm the master password: ")

            """ Comparing two input. If correct; salting and hashing them with bcrypt """
            if password1 == password2:
                master_password = password2.encode()
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(master_password, salt)

                """ Storing a master password in a seperate file"""
                with open('master_password.txt', 'w') as file:
                    file.write(hashed_password.decode())

                print("Your master password has been successfully created\n")
                break

            else:
                print("Passwords do not match. Try again!!!\n") 


def validate_master_password():
    attempts = 3   
    
    """ If the file is already created then instead of overwriting, read the hashed password """
    with open('master_password.txt', 'r') as file:
        hashed_password = file.readline().strip()
    
    while attempts > 0:
        compare_password = input("Enter Master Password: ").encode()

        """ comparing passwords to check if the user has provided the correct password """
        if bcrypt.checkpw(compare_password, hashed_password.encode()):
            break

        else:
            print("Incorrect Master Password\n")
            attempts -= 1

    """ Breaking out of the loop if more than 3 attempts have failed """
    if attempts == 0:
        print("Too many failed attempts. Exiting ...\n")
        exit()
            

def select_mode():
    while True:
        mode = input("Type 1: Add a new password \n"
                    "Type 2: View the password vault \n"
                    "Type 3: Exit the password manager\n"
                    "")
        
        """ Opening correct function according to the chosen mode """
        if mode == '1':
            store_password()
            return store_password

        elif mode == '2':
            view_password()
            return view_password
        
        elif mode == '3':
            exit()

        else:
            print("Please choose mode 1, 2 or 3: \n")
                

def store_password():
    email_username = input("Email or Username: ")
    password = input("Password: ").encode()
    website = input("Website URL: ")
    notes = input("Notes: ")

    """ Only Salting and Hasing the password """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    """ Storing details in a dictonary """
    entry = {
        'username': email_username,
        'password': hashed_password.decode(),
        'website': website,
        'notes': notes,
    }

    """ Writing to a file in json format as it is a structured and machine-readable format """
    with open('password.txt', 'a') as file:
        json.dump(entry, file)
        file.write('\n')
                

def view_password():
    """ Error handling if the user choose to view the file before it is created """
    try:
        with open('password.txt', 'r') as file:
            entries = []
            for line in file:
                entry = json.loads(line.strip())
                entries.append([entry['username'], entry['password'], entry['website'], entry['notes']])

            """ Displaying the stored details in a tabular format """
            if entries:
                headers = ['Username', 'Password', 'Website', 'Notes']
                print(tabulate(entries, headers, tablefmt='grid'))
                print()
            
            else:
                print("No password entries found.\n")
    
    except FileNotFoundError:
        print("Password file does not exist.")
        print("Select 1 to create a password file.\n")
        select_mode()


if __name__ == "__main__":
    main()