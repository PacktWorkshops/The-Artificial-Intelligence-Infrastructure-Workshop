import pickle
import pandas as pd


# load the datasets
train = pd.read_csv('../../Datasets/Titanic/train.csv')
test = pd.read_csv('../../Datasets/Titanic/test.csv')

# prepare the dataset
train.Sex = train.Sex.map({'male': 0, 'female': 1})
y = train.Pclass.copy()  # use the values in the Pclass column as output targets
X = train.drop(['Pclass'], axis=1)
X.drop(['Name'], axis=1, inplace=True)
X.drop(['Embarked'], axis=1, inplace=True)
X.drop(['PassengerId'], axis=1, inplace=True)
X.drop(['Cabin'], axis=1, inplace=True)
X.drop(['Ticket'], axis=1, inplace=True)
# X.drop(['Fare'], axis=1, inplace=True) # removing the Fare column will result in a much worse prediction!
X.Age.fillna(X.Age.mean(), inplace=True)

# create and train a simple model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# evaluate the model
model.score(X, y)

# export the model to pickle file
file = open('model.pkl', 'wb')  # write in bytes
pickle.dump(model, file)
file.close()
