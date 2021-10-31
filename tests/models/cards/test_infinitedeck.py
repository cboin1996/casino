import unittest
from casino.models.cards.infinitedeck import InfiniteDeck
from casino.models.cards.color import Color

class TestInfiniteDeck(unittest.TestCase):
    def setUp(self):
        self.pb = 0.3333
        self.deck = InfiniteDeck(0,10, self.pb)
        self.tolerance = 0.05

    def test_draw(self):
        num_count = {}
        color_count = {}
        for _ in range(100):
            card = self.deck.draw()
            if card.color.name in num_count:
                if card.number in num_count[card.color.name]:
                    num_count[card.color.name][card.number] += 1
                else:
                    num_count[card.color.name][card.number] = 1

            else:
                num_count[card.color.name] = {}

            if card.color.name in color_count:
                color_count[card.color.name] += 1
            else:
                color_count[card.color.name] = 1

        print(color_count)
        print(num_count)
        msg = f"Expecting number of red cards to be within [{self.tolerance}] of [{self.pb}] for the drawn cards!"
        self.assertAlmostEqual(color_count[Color.RED.name]/color_count[Color.BLACK.name], 0.33, delta=self.tolerance, msg=msg)

if __name__ == "__main__":
    unittest.main()

