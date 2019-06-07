#python script to add new users using base64 to encrypt passwords in password file

#import stuff
import getpass
import base64
import os
import sys

user = input("Enter the name of the user you like to gain access to the wonderful world of containers: ")
print(user + " will not know what hit 'm")

password = getpass.getpass('Enter the password: ')
password2 = getpass.getpass('Enter the password again: ')

if password != password2:
    print("learn how to type")
    sys.exit()

toEncode = password.encode()
encryptedPassword = base64.b64encode(toEncode).decode("utf-8")
print("user to be stored: " + user)
print("encrypted password to be stored: " + encryptedPassword)


with open("passwords.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if user == line.split(" ")[0]:
            overwriteInput = input("Overwrite current password?(y/n): ")
            if overwriteInput == "n":
                sys.exit()
            if overwriteInput == "y":
                os.system("sed -i 's/^" + user + " .*$/" + user + " " + encryptedPassword + "/' passwords.txt")
                sys.exit()
            else:
                print("you didn't type y or n")
                sys.exit()
            
os.system("echo " + user + " " + encryptedPassword + " >> passwords.txt")

