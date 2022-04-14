import requests, random, ctypes
from threading import Thread

cookie = ''
req = requests.Session()
req.cookies['.ROBLOSECURITY'] = cookie

totalPages = req.get('https://privatemessages.roblox.com/v1/messages?messageTab=inbox&pageNumber=0&pageSize=20').json()['totalPages']
messagesFailed = messagesArchived = messagesSkipped = 0

def cmdTitle():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Messages Archived: {messagesArchived} | Messages Skipped: {messagesSkipped} | Messages Failed: {messagesFailed}')

def findMessages():
    global messagesSkipped
    nextPage = random.randint(0, int(totalPages))
    while True:
        firstPage = req.get(f'https://privatemessages.roblox.com/v1/messages?messageTab=inbox&pageNumber={nextPage}&pageSize=20')
        if firstPage.status_code == 200:
            data = firstPage.json()['collection']
            random.randint(0, firstPage.json()['totalPages'])
            toArchive = []
            for message in data:
                if message['sender']['id'] == 1:
                    toArchive.append(message['id'])
                else: messagesSkipped += 1
            if len(toArchive) != 0:
                archiveMessages(toArchive)
        else:
            print(firstPage.text)

def grabCsrf():
    return req.post('https://auth.roblox.com/v1/logout').headers['X-CSRF-TOKEN']

def archiveMessages(toArchive):
    global messagesArchived, messagesFailed
    currentCsrf = grabCsrf()
    json = {"messageIds":toArchive}
    archiveReq = req.post('https://privatemessages.roblox.com/v1/messages/archive', json=json, headers={'X-CSRF-TOKEN': currentCsrf})
    if archiveReq.json()['failedMessages'] == []: messagesArchived += len(toArchive)
    else: messagesFailed += len(archiveReq.json()['failedMessages'])

Thread(target=cmdTitle).start()
for i in range(10):
    Thread(target=findMessages).start()
