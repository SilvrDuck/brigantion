import threading
import server



def commandline():
    while True:
        command = input()
        display(command)
        parse(command)



if __name__ == "__main__":

    serve = threading.Thread(target=server.run)
    serve.start()
    
    commandline()