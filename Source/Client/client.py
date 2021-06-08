from socket import *

IPaddress = '127.0.0.1'
Port = 2121


clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((IPaddress, Port))
except:
    print('connection refused !!')

def enter_dwld(new_port, file_name):
    DataChannel = socket(AF_INET, SOCK_STREAM)
    try:
        print('\nconnecting to Data channel...')
        DataChannel.connect((IPaddress, int(new_port)))
        print('\nconnected successfully ...')
    except:
        print('\nconnection refused !!\n')
        return False
    print('\nDownloading file ...')
    data = b""
    counter = 0
    while True:
        binary_data_file = DataChannel.recv(1024)
        data += binary_data_file
        counter +=1
        if not binary_data_file:
            break
    print(counter)
    print('\nFile Downloaded ...')
    with open(file_name, 'wb') as new_file:
        new_file.write(data)
        print('\nCreate file successfully ...')
    print('\nClosing Data Channel...')
    DataChannel.close()
    return True




def main():

    # input commands in loop
    while True:
        command = input('>> ')
        clientSocket.sendall(command.encode())

        if command[:5].upper() == 'DWLD ':
            new_port = clientSocket.recv(1024).decode()
            if new_port == 'FALSE':
                print('\nFile Not Found ...!!!\n')
                continue
            if not enter_dwld(new_port, command[5:]):
                continue

        ans = clientSocket.recv(1024)
        if command.upper() == 'HELP':
            print('\n'+ans.decode()+'\n')
        elif command.upper() == 'LIST':
            print('\n'+ans.decode()+'\n')
        elif command[:5].upper() == 'DWLD ':
            print('\n'+ans.decode()+'\n')
        elif command.upper() == 'PWD':
            print('\n'+ans.decode()+'\n')
        elif command[:3].upper() == 'CD ':
            print('\n'+ans.decode()+'\n')
        elif command.upper() == 'QUIT':
            print('\nexit from program...!!!\n\n')
            clientSocket.close()
            exit()

        else:
            print('command Not found !!')


if __name__ == '__main__':
    main()