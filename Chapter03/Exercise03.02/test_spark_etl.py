from unittest import TestCase


class TestSparkETL(TestCase):

    def test_spark_etl(self):
        # arrange
        import spark_etl

        # act
        result = spark_etl.selected.collect()

        # assert
        assert len(result) == 338
        assert result[0]['rating'] == 'TV-G'
        assert result[122]['count_cast'] == 10
        assert result[281]['director'] is None
        assert result[334]['release_year'] == '2019'
