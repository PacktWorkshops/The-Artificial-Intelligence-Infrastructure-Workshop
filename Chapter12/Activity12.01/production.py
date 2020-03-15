from flask import Flask, jsonify, request
import pickle

# load the model from pickle file
file = open('model.pkl', 'rb')  # read bytes
model = pickle.load(file)
file.close()

# get predictions from the model
print(model.predict([[1,0,36,2,0,14.67]]))  # male, survived, low fare
print(model.predict([[0,1,42,1,1,96.61]]))  # female, died, high fare

# create an API with Flask
app = Flask('ClassPredictor')


# create an API with Flask
app = Flask('ClassPredictor')


# call this: curl -X GET http://127.0.0.1:5000/foo
@app.route('/hi', methods=['GET'])
def bar():
    result = 'hello!'
    return result


# call this: curl -X POST -H "Content-Type: application/json" -d \
# '{"Survived": 1, "Sex": 0, "Age": 72, "SibSb": 2, "Parch": 0, "Fare": 8.35}' http://127.0.0.1:5000/class
@app.route('/class', methods=['POST'])
def predict_class():
    payload = request.get_json()
    person = [payload['Survived'], payload['Sex'], payload['Age'], payload['SibSb'], payload['Parch'], payload['Fare']]
    result = model.predict([person])
    print(f'{person} -> {str(result)}')
    return f'I predict that person {person} was in class {result} of the Titanic\n'


app.run()
