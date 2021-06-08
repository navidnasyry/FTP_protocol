from socket import *
import os
import random

IPaddress = '127.0.0.1'
Port = 2121

socketServer = socket(AF_INET, SOCK_STREAM)
socketServer.bind((IPaddress, Port))
socketServer.listen()
os.chdir('files')
CURRENT_PATH = os.getcwd()
print(CURRENT_PATH)
print('The server is ready to receive...')


def help():
    print('HELP enter')
    str1 = 'HELP -> help you\n'
    str2 = 'LIST -> show files and size of files\n'
    str3 = 'PWD -> show current path\n'
    str4 = 'DWLD filePath -> download file from server\n'
    str5 = 'CD dirName -> open directory in server\n'
    str6 = 'QUIT -> exit \n'
    return str1+str2+str3+str4+str5+str6

def pwd():
    print('PWD enter')
    if os.getcwd() == CURRENT_PATH:
        return '/'
    return os.getcwd()[len(CURRENT_PATH):]

def list():
    print('LIST enter')
    totalSize = 0
    ans = ''
    files = os.listdir()
    for f in files:
        totalSize += os.path.getsize(f)
        str_1 = f + ' -> size : '+str(os.path.getsize(f)) + ' Bytes' + '\n'
        if os.path.isdir(f):
            str_1= 'd > '+str_1
        else:
            str_1 = 'f > '  + str_1

        ans += str_1

    guid = '\n\nf : folder \nd : directory\n'
    ans = 'Total Size : ' + str(totalSize) + ' Bytes' + '\n\n' + ans + guid
    return ans






def cd(path):
    try:
        current = os.getcwd()
        os.chdir(path)
        if CURRENT_PATH == os.getcwd()[:len(CURRENT_PATH)]:
            return '\ndirectory changed.\n'
        else:
            os.chdir(current)
            print('\nUser want  access to bad path ...!!!\n\n')
            return "\nYou can't access to this path .\n"
    except:
        print('\nbad request...!\n\n')
        return '\nNo such file or directory OR Not a directory !!!\n'



def dwld(contorol_channel,file_name):
    if file_name not in os.listdir():
        return 'FALSE'


    print('\nCreating random port between 3000 to 50000\n')
    new_port = random.randint(3000,50000)
    print('New Port : ' + str(new_port))
    DataChannel = socket(AF_INET, SOCK_STREAM)
    print('\nCreate Data Channel with client...')
    DataChannel.bind((IPaddress, new_port))
    print('\nBinding ...')
    print('\nListening ....')
    DataChannel.listen()
    contorol_channel.send(str(new_port).encode())
    print('\nsending new port to client ...')
    print('\nWaiting to accept ...')
    Connection_DataChannel , addr = DataChannel.accept()
    print('\nClient connected from : ' + str(addr))
    try:
        with open(file_name,'rb') as file:
            print('\nOpening file...')
            file_binary_data = file.read()
            print('\nSending file ...')
            Connection_DataChannel.send(file_binary_data)
        print('\nSend file successful...')
        Connection_DataChannel.close()
        print('\nClosing connection channel...')
        DataChannel.close()
        print('\nClosing Data Channel ...')
        return '\nDownload file successful...'


    except:
        print('\nFile Not Found ...!!!')
        Connection_DataChannel.close()
        print('\nClosing connection channel...')
        DataChannel.close()
        print('\nClosing Data Channel ...')
        return '\nNo such file ...!!!\n\n'

def main():
    try:
        connection_socket, addr = socketServer.accept()
        print('\nconnected to by address '+str(addr))
        print()
        while True:
            #RECIVE DATAS
            #SEND ANSWER
            print('waiting for enter command ...\n')
            command = connection_socket.recv(1024).decode()
            reply = ""
            if command.upper() == 'HELP':
                reply = help()

            elif command.upper() == 'LIST':
                #list(filter(os.path.isdir, os.listdir(<path>))) # show joust directory
                reply = list()

            elif command[:5].upper() == 'DWLD ':
                reply = dwld(connection_socket,command[5:])

            elif command.upper() == 'PWD':
                reply = pwd()

            elif command[:3].upper() == 'CD ':
                reply = cd(command[3:])
            elif command.upper() == 'QUIT':
                socketServer.close()
                connection_socket.close()
                print('\nConnection closed .\n\nexit from server...\n\n')
                exit()

            else:
                print('command not found !')
                reply = 'Command Not Found !!!'

            connection_socket.send(reply.encode())
    finally:
        socketServer.close()



if __name__ == '__main__':
    main()