import socket
import os
import sys
import time

import requests


if not os.path.exists("accept_token"):
    os.makedirs("accept_token")

if not os.path.exists("history"):
    os.makedirs("history")

server = "irc.twitch.tv"  #settings
channel = raw_input("What is your Twitch name")
log_file = None

botnick = "CruBot"
password = "oauth:ca3muz1anz4eddy93v1f2a41lyotiqg"
auth_file = open('accept_token/' + channel + '.txt', 'w')
auth_file = open('accept_token/' + channel + '.txt', 'r')
botAuth = str(auth_file.readlines())
print botAuth
auth_file.close()
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #defines the socket
print "connecting to:" + server
irc.connect((server, 6667))
irc.send("PASS " + password + "\n")  #connects to the server
irc.send("USER " + botnick + " " + botnick + " " + botnick + " :This is a fun bot!\n")  #user authentication
irc.send("NICK " + botnick + "\n")  #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")  #auth
irc.send("JOIN " + channel + "\n")  #join the chan


def handle_command(str_cmd):
    cmd = str_cmd[str_cmd.find(':!'):str_cmd.find('\s')]
    #Bot commands
    if cmd == '!join':
        irc.send("JOIN " + channel + "\n")
    elif cmd == ':!setToken':
        t = text.split(':!setToken')
        storeAuth(t[1])
    #public commands
    elif cmd == ':!hap':
        send_msg('IDS HABBENING')
    elif cmd == ':!searchGame':
        t = text.split(':!searchGame ')
        search_game(t[1])
    #mod only
    else:
        user = get_user_posting(str_cmd)

        if cmd == ':!setTitle':
            t = text.split(':!setTitle')
            chan_update(t[1])
        elif cmd  == ':!setGame':
            t = text.split(':!setGame')
            print t[1]
            game_update(t[1])
        elif text == ':!exit':
            if text.find(':kimonorex') != -1 or text.find(':cruor99') != -1:
                irc.send('PRIVMSG ' + channel + ' :bai \r\n')
                stop_logging_history()

def send_msg(str_msg):
    irc.send('PRIVMSG #' + channel + ' :' + str_msg + '\r\n')


def get_user_posting(str_msg):
    return text[text.find(":") + 1:text.find("!")]


def chan_update(*title):  #updates channel title

    example = str(title)
    print example
    print title

    url = 'https://api.twitch.tv/kraken/channels/' + channel.strip('#') + '?oauth_token=niyi9fepwmus1pge3rosn2lqn4wy46n'
    headers = {"Accept ": "application/vnd.twitchtv.v3+json", " Authorization": " " + botAuth}
    channelobj = {'channel[status]': title}
    r = requests.put(url, data=channelobj, headers=headers)
    print r.text


def search_game(search_str):
    print search_str
    url = 'https://api.twitch.tv/kraken/search/games/?q=' + search_str.strip(' ').strip('').strip('\n').strip(
        '\r\n') + '&type=suggest'
    #   url = 'https://api.twitch.tv/kraken/search/games/'
    headers = {'Accept ': 'application/vnd.twitchtv.v3+json'}
    #  query = {'q ': search_str.strip(' ').strip(''), 'type ': 'suggest'}
    r = requests.get(url, headers=headers)
    print r.text


def game_update(*title):  #updates channel title

    example = str(title)
    print example
    print title

    url = 'https://api.twitch.tv/kraken/channels/' + channel.strip('#') + '?oauth_token=niyi9fepwmus1pge3rosn2lqn4wy46n'
    headers = {"Accept ": "application/vnd.twitchtv.v3+json", " Authorization": " " + botAuth}
    channelobj = {'channel[game]': title}
    r = requests.put(url, data=channelobj, headers=headers)
    print r.text


def storeAuth(accepttoken):  #Saves the accept token in a file
    workPath = os.getcwd()
    os.chdir(workPath + "/accept_token")
    auth_token = open(channel + ".txt", "w")
    auth_token.write(accepttoken)


def start_logging_history():
    workPath = os.getcwd()
    os.chdir(workPath + "/history")
    global log_file
    log_file = open(time.strftime("%d-%m-%Y") + '.txt', 'a')
    log_file.write("Starting logging session at " + time.strftime("%H:%M:%S") + "\n")
    print "Logging..."


def stop_logging_history():
    log_file.write("Ending logging session at " + time.strftime("%H:%M:%S") + "\n")
    log_file.close()
    sys.exit(0)


start_logging_history()
users = []
while 1:  # puts it in a loop
    text = irc.recv(2040)  # receive the text
    print text  # print text to console
    log_file.write(time.strftime("%H:%M:%S") + ' ' + text + '\n')
    if text.find(':jtv MODE #that_other_vidya_stream +o'):
        users.append(text[text.find('+o') + 2:])
    if text.find('PING') != -1:  # check if 'PING' is found
        irc.send('PONG ' + text.split()[1] + '\r\n')  # returnes 'PONG' back to the server (prevents pinging out!)
    if text.find('PRIVMSG #that_other_vidya_stream :!'):
        handle_command(text)
    else:
        if text.find(':hue') != -1:
            send_msg('HUEHUEHUEHUEHUEHU')
        if text.find(':Kappa') != -1:
            send_msg('kappa')
        if text.find(':WHITE POWER') != -1:
            send_msg('WHITE POWER TO ' + get_user_posting(text).upper())
        if text.find(':frankerZ') != -1:
            send_msg('frankerz')
        if text.find(':cru33') != -1 and text.find(':crubot') == -1:
            # print 'CRU REALLY IS A FAG'
            send_msg('Cru is a fag')

            #https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=33u2pg1xqnjj6okkg2ld4o9wclmztb1&redirect_uri=http://thatothervidyastream.webs.com/auth.html&scope=channel_editor+channel_read+user_read


            #niyi9fepwmus1pge3rosn2lqn4wy46n

            #vidya stream auth: 9jhojix8jia8lfon1agqxl914swtr72