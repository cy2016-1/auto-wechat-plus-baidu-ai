# wechat UI automation


from uiautomation import WindowControl, MenuControl
import requests

wx = WindowControl(Name='微信')
wx.SwitchToThisWindow()


def get_all_messages():
    all_message = wx.ListControl(Name='消息').GetChildren()
    return all_message


def get_latest_message(num):
    all_message = wx.ListControl(Name='消息').GetChildren()
    laset_msg = all_message[num:]
    msg_list = []
    for msg in laset_msg:
        print(f'收到消息：{msg.Name}')
        msg_list.append(msg.Name)
    return '。'.join(msg_list)


def send_to_ai(query):
    url = 'http://127.0.0.1:5000/api'
    form_data = {
        'query': query
    }
    response = requests.post(url, data=form_data)
    if response.status_code == 200:
        data = response.json()
        # print(data)
    else:
        print(f"Request failed with status code {response.status_code}")
    return data.get('response')


last_message_num = len(get_all_messages())
while True:
    current_message_num = get_all_messages()
    if last_message_num < len(current_message_num):
        latest_message = get_latest_message(last_message_num)
        result = send_to_ai(latest_message)
        print(f'发送消息：{result}')
        wx.SendKeys(result, waitTime=1)
        wx.SendKeys('{Enter}', waitTime=1)
        last_message_num = len(current_message_num) + 1
        