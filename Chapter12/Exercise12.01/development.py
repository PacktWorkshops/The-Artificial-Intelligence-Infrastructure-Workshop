import pickle
import pandas as pd


# load the datasets
train = pd.read_csv('../../Datasets/Titanic/train.csv')
train.info()
test = pd.read_csv('../../Datasets/Titanic/test.csv')
test.info()

# prepare the dataset
train.Sex = train.Sex.map({'male': 0, 'female': 1})
y = train.Survived.copy()  # use the values in the Survived column as output targets
X = train.drop(['Survived'], axis=1)
X.drop(['Name'], axis=1, inplace=True)
X.drop(['Embarked'], axis=1, inplace=True)
X.drop(['PassengerId'], axis=1, inplace=True)
X.drop(['Cabin'], axis=1, inplace=True)
X.drop(['Ticket'], axis=1, inplace=True)
X.Age.fillna(X.Age.mean(), inplace=True)
X.info()
X.head()

# create and train a simple model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X, y)

# evaluate the model
model.score(X, y)

# export the model to pickle file
file = open('model.pkl', 'wb')  # write in bytes
pickle.dump(model, file)
file.close()
