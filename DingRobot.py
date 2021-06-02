import requests
import re
# import json


class Robot:

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": {"content": ""},
        "at": {
            "atMobiles": [],
            "atUserIds": [],
            "isAtAll": False
        }
    }


    def __init__(self, webhook, keyword=None, bind=[]):
        self.webhook = webhook
        self.keyword = keyword
        self.bind = bind
    

    def init(self):
        Robot.data = {
                "msgtype": "text",
                "text": {"content": ""},
                "at": {
                    "atMobiles": [],
                    "atUserIds": [],
                    "isAtAll": False
                }
            }


    def parse(self, content, is_at_all):
        # @的使用
        if "@all=" in content:  # @all=用于@全体成员
            is_at_all = True
            content.replace('@all=', '@all')
        Robot.data["at"]["isAtAll"] = is_at_all
        if not is_at_all:

            if "@phone" in content:  # 用@phone电话 来@人
                phone_li = re.findall('@phone(\d+) ', content)
                Robot.data["at"]["atMobiles"] = phone_li
                for phone in phone_li:
                    content = content.replace(f'@phone{phone} ', f'@{phone}')

            if "@id" in content:  # 用@userID 来@人
                ids = re.findall('@id(\d+) ', content)
                Robot.data["at"]["atUserIds"] = ids
                for id in ids:
                    content = content.replace(f'@id{id} ', f'@{id}')
        
            if self.bind and "@=" in content:  # 用@=某人= 来快速@他人（需要绑定电话号码）
                regex = re.compile('@=(.*?)=')
                li = regex.findall(content)
                for name in li:
                    try:
                        content = content.replace(f'@={name}=', f'@{self.bind[name]}')
                        Robot.data["at"]["atMobiles"].append(self.bind[name])
                    except:
                        pass
        return content


    def quick_send(self, content, is_at_all=False, at_mobiles_list=[], atUserIds_list=[]):
        # set data
        content = Robot.parse(self, content, is_at_all)
        if self.keyword:
            Robot.data["text"]["content"] = self.keyword + ":\n" + content
        else:
            Robot.data["text"]["content"] = content
        
        # post data use json
        r = requests.post(url=self.webhook, json=Robot.data)  # json传入字典，data传入json数据,且要加headers
        print(r.text)
        Robot.init(self)
        return r.text


    def send_text(self, content, is_at_all=False, at_mobiles_list=[], atUserIds_list=[]):
        # set data
        if self.keyword:
            Robot.data["text"]["content"] = self.keyword + ": " + content
        else:
            Robot.data["text"]["content"] = content
        Robot.data["at"]["isAtAll"] = is_at_all
        Robot.data["at"]["atMobiles"] = at_mobiles_list
        Robot.data["at"]["atUserIds"] = atUserIds_list

        # # post data use data
        # post_data = json.dumps(Robot.data)
        # r = requests.post(url=self.webhook, headers=Robot.headers, data=post_data)

        # post data use json
        r = requests.post(url=self.webhook, json=Robot.data)  # json传入字典，data传入json数据,且要加headers
        print(r.text)
        Robot.init(self)
        return r.text
