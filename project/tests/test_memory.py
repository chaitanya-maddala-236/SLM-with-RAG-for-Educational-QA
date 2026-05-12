import unittest

from project.app.memory.conversation_memory import ConversationMemory


class TestConversationMemory(unittest.TestCase):
    def test_decay_and_prune(self):
        memory = ConversationMemory(short_term_limit=2, decay_rate=0.25)
        memory.add_turn("q1", "a1", "bio")
        memory.add_turn("q2", "a2", "chem")
        memory.add_turn("q3", "a3", "bio")
        self.assertEqual(len(memory.turns), 2)
        self.assertTrue(isinstance(memory.summary, str))


if __name__ == "__main__":
    unittest.main()
