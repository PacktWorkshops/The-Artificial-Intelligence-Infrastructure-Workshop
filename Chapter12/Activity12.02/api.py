from flask import Flask, request
import pickle

# load the model from pickle file
file = open('model.pkl', 'rb')  # read bytes
model = pickle.load(file)
file.close()

# create an API with Flask
app = Flask('Titanic')


# call this: curl -X POST -H "Content-Type: application/json" \
# -d '{"Survived": 1, "Sex": 0, "Age": 72, "SibSb": 2, "Parch": 0, "Fare": 68.35}' http://127.0.0.1:5000/class
@app.route('/class', methods=['POST'])
def predict_class():
    payload = request.get_json()
    person = [payload['Survived'], payload['Sex'], payload['Age'], payload['SibSb'], payload['Parch'], payload['Fare']]
    result = model.predict([person])
    print(f'{person} -> {str(result)}')
    return f'I predict that person {person} was in passenger class {result} of the Titanic\n'


app.run()
