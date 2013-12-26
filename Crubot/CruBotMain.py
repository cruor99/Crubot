
import socket
import sys
import json
import requests
import os

server = "irc.twitch.tv"       #settings
channel = raw_input("What is your Twitch name")

botnick = "CruBot"
password = "oauth:ca3muz1anz4eddy93v1f2a41lyotiqg"
auth_file = open('accept_token/'+channel+'.txt', 'w')
auth_file = open('accept_token/'+channel+'.txt', 'r')
botAuth = str(auth_file.readlines())
print botAuth
auth_file.close()
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print "connecting to:"+server
irc.connect((server, 6667))
irc.send("PASS "+ password +"\n")                                                         #connects to the server
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n")                            #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n")    #auth
irc.send("JOIN #"+ channel +"\n")        #join the chan

def chanUpdate (*title): #updates channel title
  
    example = str(title)
    print example
    print title
    
    url = 'https://api.twitch.tv/kraken/channels/'+channel+'?oauth_token=niyi9fepwmus1pge3rosn2lqn4wy46n'
    headers = {"Accept ": "application/vnd.twitchtv.v2+json", " Authorization": " "+botAuth}
    channelobj = {'channel[status]': title}
    r = requests.put(url, data=channelobj, headers=headers)
    print r.text

def storeAuth(accepttoken): #Saves the accept token in a file
	workPath = os.getcwd()
	os.chdir(workPath +"/accept_token")
	auth_token = open(channel + ".txt", "w")
	auth_token.write(accepttoken)
	
	
while 1:    #puts it in a loop
    text=irc.recv(2040)  #receive the text
    print text   #print text to console

    if text.find('PING') != -1:                          #check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
    if text.find('!join '):
        irc.send("JOIN "+ channel +"\n")
    if text.find(':!hap')!=-1:
        t = text.split(':!hap')
        to = t[1].strip()
        irc.send('PRIVMSG '+channel+' :IDS HABBENING \r\n')
    if text.find(':hue')!=-1:
        t = text.split(':hue')
        to = t[1].strip()
        irc.send('PRIVMSG '+channel+' :HUEHUEHUEHUEHUEHU  \r\n')
    if text.find(':!setTitle')	!=-1:
        t = text.split(':!setTitle')
        strTest = "Vidya: ".join(t[1:])
        print strTest
        chanUpdate(strTest)
    if text.find(':!setToken') !=-1:
		t = text.split(':!setToken') 
		storeAuth(t[1])


#https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=33u2pg1xqnjj6okkg2ld4o9wclmztb1&redirect_uri=http://thatothervidyastream.webs.com/auth.html&scope=channel_editor+channel_read+user_read


#niyi9fepwmus1pge3rosn2lqn4wy46n
#vidya stream auth: 9jhojix8jia8lfon1agqxl914swtr72