import unittest

from project.app.evaluation.metrics import ndcg_at_k, precision_at_k, recall_at_k
from project.app.rag.fallback import FallbackLevel, select_fallback_level


class TestFallbackAndMetrics(unittest.TestCase):
    def test_fallback_levels(self):
        self.assertEqual(select_fallback_level(0.7, 0.6, 0.3), FallbackLevel.full_rag)
        self.assertEqual(select_fallback_level(0.4, 0.6, 0.3), FallbackLevel.partial_rag)
        self.assertEqual(select_fallback_level(0.2, 0.6, 0.3), FallbackLevel.llm_fallback)

    def test_retrieval_metrics(self):
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d2", "d4"}
        self.assertGreaterEqual(precision_at_k(retrieved, relevant, 2), 0)
        self.assertGreaterEqual(recall_at_k(retrieved, relevant, 3), 0)
        self.assertGreaterEqual(ndcg_at_k(retrieved, relevant, 3), 0)


if __name__ == "__main__":
    unittest.main()
