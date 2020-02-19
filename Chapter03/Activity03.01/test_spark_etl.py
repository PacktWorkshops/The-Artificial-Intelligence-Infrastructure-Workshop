from unittest import TestCase


class TestSparkETL(TestCase):

    def test_spark_etl(self):
        # arrange
        import spark_etl

        # act
        result = spark_etl.selected.collect()

        # assert
        assert len(result) == 160
        assert result[0]['rating'] == 'TV-Y'
        assert result[21]['title'] == 'Transformers Rescue Bots Academy'
        assert result[94]['count_lists'] == 2
        assert result[159]['release_year'] == '1997'
