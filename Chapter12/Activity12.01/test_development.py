from unittest import TestCase
import development


class TestModelDevelopment(TestCase):

    def test_model(self):
        # arrange
        train = development.train
        test = development.test
        X = development.X
        y = development.y

        # act
        file = open('model.pkl', 'rb')
        file.close()

        # assert
        assert len(train) == 891
        assert len(test) == 418
        assert len(X.columns) == 6
        assert len(y) == 891
        assert file
