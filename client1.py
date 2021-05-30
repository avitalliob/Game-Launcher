import socket
import threading
from tcp_by_size3 import *


def handle_recv():
    print("1. Sign Up\n" + \
    "2. Log In\n" + \
    "3. Change Password\n" + \
    "0. exit\n\n>")

    data = input("Enter Num > ")

    if data == "0":
        return "q"
    elif data == "1":
        username = input("Enter Username > ")
        password = input("Enter Password > ")
        return "SGNUP|" + username + "|" + password
    elif data == "2":
        username = input("Enter Username > ")
        password = input("Enter Password > ")
        return "LOGIN|" + username + "|" + password
    elif data == "3":
        username = input("Enter Username > ")
        password = input("Enter New Password > ")
        return "CPASS|" + username + "|" + password
    else:
        return "RULIVE"


def main():
    cli_s = socket.socket()

    cli_s.connect(("127.0.0.1", 33445))

    while True:
        data = handle_recv()

        if data == "q":
            break
        send_with_size(cli_s, data)

        data = recv_by_size(cli_s)
        if data == "":
            print("seems server DC")
            break
        data = data.decode("utf-8")
        print("Got>>" + data)


if __name__ == '__main__':
    main()