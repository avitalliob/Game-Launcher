import socket
import threading
import os
from _thread import *
import actions
import database
import passwords
from tcp_by_size3 import *

DEBUG = False
exit_all = False


def handle_client(sock, tid):
    """
    func to handle each client
    :param sock:
    :param tid:
    :param db:
    :return:
    """
    global exit_all
    print("New Client num " + str(tid))

    while not exit_all:
        try:
            data = recv_by_size(sock)
            print(data)
            if data == "":
                print("Error: Seems Client DC")
                break
            print("hi")
            to_send = do_action(data)
            print("to_send: " + to_send)
            #to_send = to_send.encode("utf-8")
            send_with_size(sock, to_send)

        except socket.error as err:
            if err.errno == 10054:
                # 'Connection reset by peer'
                print("Error %d Client is Gone. %s reset by peer." % (err.errno, str(sock)))
                break
            else:
                print("%d General Sock Error Client %s disconnected" % (err.errno, str(sock)))
                break

        except Exception as err:
            print("General Error:", err)
            break
    sock.close()


def do_action(data):
    #print("Do Action")
    to_send = "Not Set Yet"
    action = data[:5]
    action = action.decode("utf-8")
    print(action)
    data = data[6:]
    #print(data)
    data = data.decode("utf-8")
    fields = data.split('|')
    print(fields)

    if DEBUG:
        print("Got client request " + action + " -- " + str(fields))

    if action == "SGNUP": #creating a new account
        print(fields[0])
        print(fields[1])
        if signup(fields[0], fields[1])[0]:
            to_send = "SGNUP|" + "Success"
        else:
            if signup(fields[0], fields[1])[1] == 1:
                #to_send = "Can not complete registration, Username is already taken"
                to_send = "SGNUP|" + "Error"
            else:
                #to_send = "can not complete registration, Password is not valid. (Password should have more than 7 " \
                          #"characters, at least one digit, one lowercase and one uppercase "
                to_send = "SGNUP|" + "Error"

    elif action == "LOGIN": #log in existing user
        print(login(fields[0], fields[1]))
        if login(fields[0], fields[1]):
            #to_send = "User successfully logged in"
            to_send = "LOGIN|" + "Success"
        else:
            #to_send = "Login failed. Username or password are incorrect"
            to_send = "LOGIN|" + "Error"

    elif action == "CPASS": #change password for this username's account
        if change_password(fields[0]):
            #to_send = "Password was successfully changed"
            to_send = "CPASS|" + "Success"
        else:
            #to_send = "An error occurred. password was not changed"
            to_send = "CPASS|" + "Error"

    else:
        print("Got unknown action from client " + action)
        to_send = "ERR___R|001|" + "unknown action"

    return to_send


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


# fix?
def send(sock, message):
    """
    sends message through socket to client
    catch an error if connection brakes
    :param sock:
    :param message:
    :return:
    """#


def signup(username, password):
    """
    register user func
    create user in database
    :param username:
    :param sock:
    :return:
    """
    print("Registering...")

    is_taken = True
    #username = None

    while is_taken:
        #send(sock, actions.USERNAME_ACTION)
        #username = receive(sock)                           # get username
        if not database.is_username_taken(username):        # check if username is free
            is_taken = False
        else:
            #sock.send("Username already taken, try something else")
            return False, 1 #Username is Taken so can not continue registering

    # username is free

    is_valid = False
    #password = None

    while not is_valid:
        #send(sock, actions.PASSWORD_ACTION)
        #password = receive(sock)
        #send(sock, "Repeat password \n")
        #send(sock, actions.PASSWORD_ACTION)
        #password_repeat = receive(sock)
        #if password_repeat != password:
            #send(sock, "Passwords don't match, try again")
            #continue
        if passwords.is_password_valid(password):
            is_valid = True
        else:
            #send(sock, "Password is invalid (should have more than 7 characters, at least one digit, "
                      #"one lowercase and one uppercase)")
            return False, 2 # password is not valid, can not continue registering

        # password is valid

        hashed_password, salt = passwords.hash_password_generate_salt(password)
        database.create_user(username, hashed_password, salt)

        #send(sock, "User successfully registered! \nNow you can log in")
        return True, 0 #user successfully registered


def login(username, password):
    """
    login user function
    give an access for succesfully logged user
    :param sock:
    :return:
    """
    print("Login...")

    #sock.send(actions.USERNAME_ACTION)
    #username = receive(sock)

    print(username)
    print(password)

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
    #send(sock, actions.NONCE_ACTION + ":" + salt + ":" + nonce)
    #send(sock, actions.PASSWORD_ACTION)
    #password = receive(sock)

    if hashed_password is not None and passwords.check_password(password, nonce, hashed_password):
        #send(sock, "Successfully login")                # passwords matched
        #logged(sock, username)                                # access granted
        return True
    else:
        #send(sock, "Username or password incorrect")     # passwords do not match
        return False


def change_password(username):
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
        #send(sock, actions.PASSWORD_ACTION)
        #password = receive(sock)                                    # get password
        #send(sock, "repeat password \n")
        #send(sock, actions.PASSWORD_ACTION)
        #password_repeat = receive(sock)                             # get repeated password
        #if password_repeat != password:                             # compare them
            #send(sock, "Passwords do not match, try again")         # passwords not the same
            #continue                                                # prompt for passwords again
        if passwords.is_password_valid(password):                   # passwords the same -> check if password is valid
            is_valid = True
        else:
            #send(sock, "Password is invalid (should have more than 7 characters,"    # pass invalid
                          #" at last one digit, one lowercase and one uppercase)")    # send validate pass rules
            return False
        # password is valid

        hashed_password, salt = passwords.hash_password_generate_salt(password)         # create hash
        database.change_password(username, hashed_password, salt)           # change pass for user in db

        #send(sock, "Password successfully changed \nNow you can log in with a new one")     # confirm successful action
        return True


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
            change_password(username)
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


def main():
    global exit_all
    exit_all = False
    s = socket.socket()
    s.bind(("0.0.0.0", 33445))
    s.listen(4)
    print("after listen")
    threads = []
    i = 1
    while True:
        cli_s, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(cli_s, i))
        t.start()
        i += 1
        threads.append(t)

    exit_all = True
    for t in threads:
        t.join()

    s.close()


if __name__ == '__main__':
    main()


