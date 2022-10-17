import socket
import select
from gameboard import BoardClass


if __name__ == '__main__':
    # using the loopback address as my server IP address
    serverAddress = '127.0.0.1'

    # define a port number for my server
    port = 8000

    # create a socket object on my server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind my host with my port number
    serverSocket.bind((serverAddress, port))

    # setup my socket using listen function
    # 5 designates the max number of connections my socket
    serverSocket.listen(5)

    player2_name = 'player2'
    player1_name = ''
    # begin accepting incoming connection requests
    clientSocket, clientAddress = serverSocket.accept()

    # Printing the client address
    print("Client connected from: ", clientAddress)

    # Wait for a message from my client
    clientData = clientSocket.recv(1024)
    player1_name = clientData.decode('ascii')

    # Send a message to my client
    clientSocket.send(player2_name.encode())
    # Construct board class
    board = BoardClass(player2_name, player1_name, 'O', clientSocket)
    board.program.mainloop()


        
