import time
import threading


def send(text):
    pass

def prt(text):
    send(text)
    print(text)


def server():
    while True:
        time.sleep(10)
        prt('from server')

def client():
    while True:
        imp = input('>')
        send(imp)

tr = threading.Thread(target=server)
tr.start()

client()