import socket
import sys
import pyautogui

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.1.15', 3000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while(True):
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from %s %s' % client_address)

        # Receive the data in small chunks and retransmit it
        while(True):
            data = connection.recv(16)
            message = bytes.decode(data).rstrip()
            print("|%s|" % message)
            if message == "exit":
                break
            elif message == "lclick":
                pyautogui.click()
            elif message == "dbclick":
                pyautogui.doubleClick()
            elif message == "rclick":
                pyautogui.rightClick()
            elif "&" in message:
                x, y = message.split("&")
                print("x: %s y: %s" % (x,y))
                pyautogui.moveTo(int(x), int(y), 2)
            else:
                print("else %s" % message)
                pyautogui.press(str(message))
            # print('received "%s"' % bytes.decode(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no more data from %s %s' % client_address)
                break     
    finally:
        # Clean up the connection
        connection.close()
        break