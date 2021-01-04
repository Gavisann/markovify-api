import markovify
import json
from flask import Flask
from flask import request
app = Flask(__name__)

responses = []

@app.route('/create-responses')
def create_responses(user = None):
    user = request.args.get('user')
    response_list = []

    with open("/data/models/{0}.json".format(user)) as f:
        model_json = json.load(f)

    f.close()
    reconstituted_model = markovify.Text.from_json(model_json)
    for x in range(5):
        #print(reconstituted_model.make_short_sentence(60))
        #print(reconstituted_model.make_sentence(tries=100, max_words=13))
        temp = reconstituted_model.make_sentence(tries=100, max_words=13)
        if (temp != None):
            response_list.append(temp)


    with open('/data/responses/{0}-responses.json'.format(user), 'w') as f:
        json.dump(response_list, f)
    f.close()

    return "Output for {0} has been saved to file".format(user)

@app.route('/response')
def response():
    user = request.args.get('user')
    global responses
    if len(responses) <= 1:
        create_responses(user)

    with open('/data/responses/{0}-responses.json'.format(user), 'r+') as f:

        responses = json.load(f)
        out = responses.pop()
        f.seek(0)        
        json.dump(responses, f)
        f.truncate()
    f.close()
    return out
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')