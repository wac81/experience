# -*- coding:utf-8 -*-
# coding=utf-8
# from gevent import monkey
# monkey.patch_all()

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json

from flask import Flask, request, abort,g,current_app
# from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

@app.route('/similar/<input_text>',methods=['GET', 'POST'])
def similar(input_text):
    re=object
    if request.method == 'POST':
        re = request.form['files']  # get post prarms
    else:
        try:
            re = input_text  # 获取GET参数，没有参数就赋值 0
        except ValueError:
            abort(404)      # 返回 404
    result = json.dumps(re)
    print result
    return result

if __name__ == '__main__':
    with app.app_context():
        print current_app.name
    app.run(debug=False, host='0.0.0.0', port=3001)
    # app.run()