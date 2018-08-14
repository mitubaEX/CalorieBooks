import os
from cek import Clova
import json

# application_id is used to verify requests.
application_id = "com.github.mitubaEX.CalorieBooks"
# Set debug_mode=True if you are testing your extension. If True, this disables request verification
clova = Clova(application_id=application_id,
              default_language="ja", debug_mode=False)


def getCalorieData(food_name):
    import requests
    r = requests.get(
        'https://apex.oracle.com/pls/apex/evangelist/shokuhindb/food/' + food_name)
    if len(r.json()['items']) != 0:
        return r.json()['items'][0]['calorie']
    else:
        return ''


@clova.handle.launch
def launch_request_handler(clova_request):
    return clova.response("聞きたい食材のカロリーを言ってください．終了したい場合は，終了と言ってください")


@clova.handle.end
def end_handler(clova_request):
    return


@clova.handle.intent("FoodsIntent")
def intent_handler(clova_request):
    try:
        food_name = clova_request.slot_value('Foods')
        calorie = getCalorieData(food_name)
        return clova.response(str(food_name) + "のカロリーは" + str(calorie) + "キロカロリーです")
    except:
        return clova.response("その食材は辞書に登録されていない可能性があります．別の単語をお試しください")


@clova.handle.default
def default_handler(clova_request):
    return clova.response("すみません．もう一度お願いします")


from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/app', methods=['POST'])
def my_service():
    resp = clova.route(request.data, request.headers)
    resp = jsonify(resp)
    # make sure we have correct Content-Type that CEK expects
    resp.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return resp


@app.route('/', methods=['GET'])
def echo():
    return 'echo'


if __name__ == "__main__":
    app.run()
