from flask import Flask, request, jsonify  
from baidu_ai_assistant import Baidu

app = Flask(__name__)
ai = Baidu()
input("等待手动打开界面并登陆，完成后按回车键继续")
print('AI工具启动完毕！')


@app.route('/api', methods=['GET', 'POST'])  
def api():
    if request.method == 'POST':
        form_data = request.form
        query = str(form_data['query'])
    else:
        query = request.args.get('query')
        print(request.args)
        # response_text = text.upper()
    print(f'User: {query}')
    ai_response = ai.run_with_api(query)
    print(f'AI: {ai_response}')
    return jsonify({'response': ai_response}) 


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=False)