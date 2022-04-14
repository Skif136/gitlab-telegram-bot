#!/usr/bin/env python3

import json
from vars import *
from flask import Flask
from flask import request
from flask import jsonify
from bot import Bot
app = Flask(__name__)

f = open('authmsg', 'w')
f.write(secret_message)   
f.close()

class GitlabBot(Bot):
    def __init__(self):
        try:
            self.authmsg = open('authmsg').read().strip()
        except:
            raise Exception("The authorization messsage file is invalid")

        super(GitlabBot, self).__init__()
        self.chats = {}
        try:
            chats = open('chats', 'r').read()
            self.chats = json.loads(chats)
        except:
            open('chats', 'w').write(json.dumps(self.chats))

        self.send_to_all(one_post)

    def text_recv(self, txt, chatid):
        ''' registering chats '''
        txt = txt.strip()
        if txt.startswith('/'):
            txt = txt[1:]
        if txt == self.authmsg:
            if str(chatid) in self.chats:
                self.reply(chatid, ".")
            else:
                self.reply(chatid, correct_key)
                self.chats[chatid] = True
                open('chats', 'w').write(json.dumps(self.chats))
        elif txt == 'shutupbot':
            del self.chats[chatid]
            self.reply(chatid, stop_bot)
            open('chats', 'w').write(json.dumps(self.chats))
        else:
            self.reply(chatid, invalid_key)

    def send_to_all(self, msg):
        for c in self.chats:
            self.reply(c, msg)

b = GitlabBot()

@app.route("/", methods=['GET', 'POST'])
def webhook():
    data = request.json
    kind = data['object_kind']
    if kind == 'push':
        msg = generatePushMsg(data)
    elif kind == 'tag_push':
        msg = generatePushMsg(data)
    elif kind == 'issue':
        msg = generateIssueMsg(data)
    elif kind == 'note':
        msg = generateCommentMsg(data)
    elif kind == 'merge_request':
        msg = generateMergeRequestMsg(data)
    elif kind == 'wiki_page':
        msg = generateWikiMsg(data)
    elif kind == 'pipeline':
        msg = generatePipelineMsg(data)
    elif kind == 'build':
        msg = generateBuildMsg(data)
    b.send_to_all(msg)
    return jsonify({'status': 'ok'})

def generatePushMsg(data):
    msg = (message)\
        .format(data['project']['namespace'], data['ref'].replace("refs/tags/", ""), data['project']['name'], data['project']['default_branch'], data['project']['web_url'])
    for commit in data['commits']:
        msg = msg + ''
    return msg

if __name__ == "__main__":
    b.run_threaded()
    app.run(host='0.0.0.0', port=10111)
