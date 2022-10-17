# Import the sockets library
import socket
from gameboard import BoardClass

def get_connection(connection, player1_name):
    player2_name = ''
    while True:
        # prompt the user to input
        serverAddress = input("Please enter the host name(127.0.0.1):")
        serverPort = input("Please enter the port number(8000): ")
        print("Connecting to Player2.............")
        try:
            # try to connect
            serverPort = int(serverPort)
            # Attempt to connect to the server
            connectionSocket.connect((serverAddress, serverPort))
            # Send data to server
            connectionSocket.send(player1_name.encode())
            # Wait for a message from my server
            serverData = connectionSocket.recv(1024)
            player2_name = serverData.decode('ascii')
            print("Connect Successfully.")
            break
        except Exception:
            # prompt to input again
            exitFlag = input("Can't connect to server.Do you want to play angain?")
            if exitFlag != 'y':
                print("Goodbye!")
                exit(0)
    return player2_name
    

if __name__ == "__main__":
    # create a socket object on my server
    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player1_name = "player1"
    player2_name = get_connection(connectionSocket, "player1")
    board = BoardClass(player1_name, player2_name, 'X', connectionSocket)
    board.program.mainloop()
    connectionSocket.close()
