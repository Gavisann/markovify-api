import markovify
import json
from flask import Flask
from flask import request
import threading

app = Flask(__name__)
e = threading.Event()

responses = []

def create_responses(user = None):
    
    response_list = []

    with open("/data/models/{0}.json".format(user)) as f:
        model_json = json.load(f)

    f.close()
    reconstituted_model = markovify.Text.from_json(model_json)
    x = 0
    while x < 50:
        #print(reconstituted_model.make_short_sentence(60))
        #print(reconstituted_model.make_sentence(tries=100, max_words=13))
        temp = reconstituted_model.make_sentence(tries=100, max_words=13)
        if (temp != None):
            response_list.append(temp)
            x += 1



    with open('/data/responses/{0}-responses.json'.format(user), 'w') as f:
        json.dump(response_list, f)
    f.close()

    #return "Output for {0} has been saved to file".format(user)


@app.route('/create-responses')
def create_responses_route():
    user = request.args.get('user')
    t2 = threading.Thread(name='create_responses',
                      target=create_responses,
                      args=(user,))
    t2.start()


@app.route('/response')
def response():
    user = request.args.get('user')
    global responses
    
    if len(responses) <= 10:
        t2 = threading.Thread(name='create_responses',
                      target=create_responses,
                      args=(user,))
        t2.start()

    with open('/data/responses/{0}-responses.json'.format(user), 'r+') as f:

        responses = json.load(f)
        out = responses.pop()
        f.seek(0)        
        json.dump(responses, f)
        f.truncate()
    f.close()
    print (len(responses))
    return out
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')