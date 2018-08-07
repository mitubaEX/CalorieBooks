import os
from cek import Clova
import json

# application_id is used to verify requests.
application_id = "com.github.mitubaEX.test"
# Set debug_mode=True if you are testing your extension. If True, this disables request verification
clova = Clova(application_id=application_id,
              default_language="ja", debug_mode=False)


@clova.handle.launch
def launch_request_handler(clova_request):
    return clova.response("こんにちは世界。スキルを起動します")


@clova.handle.default
def default_handler(clova_request):
    if clova_request.slot_value('Foods') == 'たこ焼き':
        return clova.response("たこ焼きのカロリーは32キロカロリーです")
    if clova_request.slot_value('Foods') == 'お好み焼き':
        return clova.response("お好み焼きのカロリーは518キロカロリーです")
    return clova.response("もう一度お願いします")


from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/app', methods=['POST'])
def my_service():
    resp = clova.route(request.data, request.headers)
    resp = jsonify(resp)
    # make sure we have correct Content-Type that CEK expects
    resp.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return resp


if __name__ == "__main__":
    app.run()
