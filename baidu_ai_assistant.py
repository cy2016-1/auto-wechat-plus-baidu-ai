from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time
import re
import datetime


class Baidu:
    def __init__(self):
        self.browser = None
        # self.launch_firefox()
        # self.launch_edge()
        self.remote_control_edge()

    def launch_firefox(self):
        print('启动浏览器')
        self.browser = webdriver.Firefox()
        self.open_url()

    def launch_edge(self):
        print('启动浏览器')
        self.browser = webdriver.Edge()
        self.open_url()

    def remote_control_edge(self):
        print('远程控制浏览器')
        edge_op = Options()
        edge_op.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Edge(options=edge_op)

    def open_url(self):
        print('打开网页')
        self.browser.get("https://www.baidu.com")

    def check_if_ele_exit(self, by, value):
        try:
            self.browser.find_element(by=by, value=value)
            return True
        except:
            return False

    def wait_for_ele_display(self, by, value, timeout=30):
        for i in range(timeout):
            if self.check_if_ele_exit(by, value):
                return True
            time.sleep(0.3)
        print('等待元素Timeout')
        return False
    
    def get_ele_text(self, by, value):
        try:
            text = self.browser.find_element(by=by, value=value).text
            return text
        except:
            return ''

    def get_total_session_num(self):
        # 找到会话编号
        try:
            session_num = len(self.browser.find_elements(by=By.XPATH, value="//div[@class='assistant-container']"))
        except Exception as e:
            print(e)
            session_num = 0
        return session_num


    def send_message(self, _message):
        # 找到输入框并输入文字
        input_box = self.browser.find_element(by=By.XPATH, value="//textarea[@placeholder='请在此输入']")
        input_box.click()
        input_box.send_keys(_message)
        input_box.send_keys(Keys.RETURN)

    def get_answer_text(self):
        return self.browser.find_elements(by=By.XPATH, value="//div[@class='placeholder']")[-1].text

    def get_answer_text_from_html(self):
        answer_html = self.browser.find_elements(by=By.XPATH, value="//div[@class='placeholder']")[-1].get_attribute("innerHTML")
        answer_html = re.sub(r'<sup .*?sup>', '', answer_html)
        answer_html = answer_html.replace('<li>', '<li>*')
        answer_html = f'<div>{answer_html}</div>'
        text_code_block_list = []
        if 'code class' in answer_html:
            code_block_list = re.findall(r'<code class="language.*?</code>', answer_html)
            for key, code_block_html in enumerate(code_block_list):
                answer_html = answer_html.replace(code_block_html, 'tmp_code_separator')
                code_block_html = code_block_html.replace('<br>', '\n')
                soup_code_block = BeautifulSoup(code_block_html, "html.parser")
                text_code_block = soup_code_block.find('pre').code.text
                language = soup_code_block.find('span', {'class': 'hljs-chat-lang'}).text
                text_code_block_list.append({'language': language, 'code': text_code_block})
                answer_html = answer_html.replace('tmp_code_separator', f'{language} code:\n{"-"*40}\n{text_code_block}\n{"-"*40}\n')
        soup = BeautifulSoup(answer_html, "html.parser")
        answer_text = soup.find("div").text
        return answer_text, text_code_block_list

    def check_session_and_get_answer(self):
        start_time = time.time()
        time.sleep(2)
        is_finished = self.wait_for_ele_display(by=By.XPATH, value="//span[text()='重新回答']", timeout=400)
        # is_responding = self.check_if_ele_exit(by=By.XPATH, value="//div[text()='停止回答']", timeout=30)
        end_time = time.time()
        duration_time = datetime.timedelta(seconds=(end_time - start_time))
        print(f"耗时: {duration_time}s")
        if is_finished:
            answer = self.get_answer_text_from_html()
            # print(answer)
            return answer
        return 'Timeout'

    def run_with_api(self, query):
        # total_session_num = self.get_total_session_num()
        # print("当前会话数：", total_session_num)
        self.send_message(query)
        answer = self.check_session_and_get_answer()
        return answer[0]

    def run(self):
        # self.open_ai_page()
        input("等待登陆，完成后按回车键继续")
        print('环境已准备好！')
        while True:
            total_session_num = self.get_total_session_num()
            print("当前会话数：", total_session_num)
            query = input("You> ")
            if query in ["exit", "quit", "退出"]:
                break
            self.send_message(query)
            answer = self.check_session_and_get_answer()
            answer_text = answer[0]
            answer_code = answer[1]
            print("AI: ")
            print(answer_text)
            # print(answer_code)
        # 关闭浏览器
        self.browser.quit()


if __name__ == '__main__':
    baidu = Baidu()
    baidu.run()
