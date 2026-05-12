import unittest

from project.app.retrieval.query_processing import preprocess_query


class TestQueryProcessing(unittest.TestCase):
    def test_preprocess_expands_and_corrects(self):
        out = preprocess_query("bio photosynthsis")
        self.assertEqual(out, "biology photosynthesis")


if __name__ == "__main__":
    unittest.main()
