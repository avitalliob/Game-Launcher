import socket
import os
from _thread import *
import actions
import database
import passwords


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        data = data.decode('utf-8')
        data = data.split(':')
        if data[0] == 'user':
            send = 'you are user'
        response = 'Server message: '
        if not data:
            break
        #connection.sendall(str.encode(send))
    connection.close()


def receive(sock):
    """
    receives and returns message from client
    catch an error if connection brakes
    :param sock:
    :return:
    """
    input_line = None
    try:
        input_line = sock.recv(1024)
    except:
        print("Unexpected error")

    return input_line


def send(sock, message):
    """
    sends message through socket to client
    catch an error if connection brakes
    :param sock:
    :param message:
    :return:
    """


def register(sock):
    """
    register user func
    create user in database
    :param sock:
    :return:
    """
    print("Registering...")

    is_taken = True
    username = None

    while is_taken:
        send(sock, actions.USERNAME_ACTION)
        username = receive(sock)                           # get username
        if not database.is_username_taken(username):        # check if username is free
            is_taken = False
        else:
            sock.send("Username already taken, try something else")

    # username is free

    is_valid = False
    password = None

    while not is_valid:
        send(sock, actions.PASSWORD_ACTION)
        password = receive(sock)
        send(sock, "Repeat password \n")
        send(sock, actions.PASSWORD_ACTION)
        password_repeat = receive(sock)
        if password_repeat != password:
            send(sock, "Passwords don't match, try again")
            continue
        if passwords.is_password_valid(password):
            is_valid = True
        else:
            send(sock, "Password is invalid (should have more than 7 characters, at least one digit, "
                      "one lowercase and one uppercase)")

        # password is valid

        hashed_password, salt = passwords.hash_password_generate_salt(password)
        database.create_user(username, hashed_password, salt)

        send(sock, "User succesfully registered! \nNow you can log in")


def login(sock):
    """
    login user function
    give an access for succesfully logged user
    :param sock:
    :return:
    """
    print("Login...")

    sock.send(actions.USERNAME_ACTION)
    username = receive(sock)

    print(username)

    hashed_password = None
    salt = None
    hash_and_salt = database.get_password(username)     # get salt and hashed password from db
    if hash_and_salt:
        hashed_password = hash_and_salt[0]
        salt = hash_and_salt[1]

    if not salt:                                        # user does not exist in db
        salt = passwords.get_salt()                     # to not reveal if username exists or not
                                                        # behave naturally with newly generated salt
    nonce = passwords.get_salt()
    send(sock, actions.NONCE_ACTION + ":" + salt + ":" + nonce)
    send(sock, actions.PASSWORD_ACTION)
    password = receive(sock)

    if hashed_password is not None and passwords.check_password(password, nonce, hashed_password):
        send(sock, "Successfully login")                # passwords matched
        logged(sock, username)                                # access granted
    else:
        send(sock, "Userame or password incorrect")     # passwords do not match


def change_password(sock, username):
    """
    change password user function
    change password for user in db if everything succeed
    :param sock:
    :param username:
    :return:
    """
    print("Changing password")

    is_valid = False
    password = None

    while not is_valid:
        send(sock, actions.PASSWORD_ACTION)
        password = receive(sock)                                    # get password
        send(sock, "repeat password \n")
        send(sock, actions.PASSWORD_ACTION)
        password_repeat = receive(sock)                             # get repeated password
        if password_repeat != password:                             # compare them
            send(sock, "Passwords do not match, try again")         # passwords not the same
            continue                                                # prompt for passwords again
        if passwords.is_password_valid(password):                   # passwords the same -> check if password is valid
            is_valid = True
        else:
            send(sock, "Password is invalid (should have more than 7 characters,"    # pass invalid
                          " at last one digit, one lowercase and one uppercase)")    # send validate pass rules
        # password is valid

        hashed_password, salt = passwords.hash_password_generate_salt(password)         # create hash
        database.change_password(username, hashed_password, salt)           # change pass for user in db

        send(sock, "Password successfully changed \nNow you can log in with a new one")     # confirm successful ction


def logged(sock, username):
    """
    function to handle logged user
    shows menu with actions for logged users
    :param sock:
    :param username:
    :return:
    """

    send(sock, "Access granted!")

    while True:
        send(sock, "\nWhat do you want to do? (ls/change_password/logout/delete_account)")  # menu for logged user
        send(sock, actions.TYPE_ACTION)
        current_type = receive(sock)            # get type
        if current_type is None:
            print("Connection lost")
            return
        elif current_type == "change_password":
            change_password(sock, username)
        #elif current_type == "ls":
            #send(sock, "root home etc lib media mnt")
        elif current_type == "delete_account":
            database.delete_user(username)
            send(sock, "Your account was removed from the system")
            return
        elif current_type == "logout":
            return
        else:
            send(sock, "unrecognized type")


def run(sock):
    """
    main function when thread starts
    to manage connection with client
    :return:
    """

    send(sock, "Connected to server")

    while True:
        send(sock, "\nWhat do you want to do? (register/login/quit)")
        send(sock, actions.TYPE_ACTION)
        current_type = receive(sock)            # get type
        if current_type is None:
            break
        elif current_type == "login":
            login(sock)
        elif current_type == "register":
            register(sock)
        elif current_type == "quit":
            send(sock, actions.QUIT_ACTION)
            break
        else:
            send(sock, "Unrecognized type")

    # user quit from server
    print("Client disconnected")
    sock.close()


def main():


if __name__ == '__main__':
    main()


