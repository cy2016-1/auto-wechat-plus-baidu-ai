# Before run
1. Make sure you have installed Microsoft Edge.
2. Make sure you have corresponding browser driver.
3. Make sure you have opened and loged WeChat in your PC

# Where to download browser driver
For Edge:
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# if you are using browser to do remote control (recommended)
You must start brower in your terminal like this:
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\your_project\edge"

# How to run
1. Run the server_baidu.py file to ensure local API is working
2. Run wechat_auto.py

百度“搜索AI伙伴”的网址如下：
https://chat.baidu.com/?source=pd_Page

注意：这里的baidu相关的页面控制只支持“搜索AI伙伴”，不支持“文心一言”，若由于百度的更新，导致有网页元素无法控制的情况，请自行debug修改。