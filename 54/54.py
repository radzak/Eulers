from collections import Counter
import re


class PokerHand:
    HANDS = {
        ((1, 1, 1, 1, 1), 'straight', 'colour'): 'STRAIGHT FLUSH',
        ((4, 1), 'no_straight', 'no_colour'): 'FOUR OF A KIND',
        ((3, 2), 'no_straight', 'no_colour'): 'FULL HOUSE',
        ((1, 1, 1, 1, 1), 'no_straight', 'colour'): 'FLUSH',
        ((1, 1, 1, 1, 1), 'straight', 'no_colour'): 'STRAIGHT',
        ((3, 1, 1), 'no_straight', 'no_colour'): 'THREE OF A KIND',
        ((2, 2, 1), 'no_straight', 'no_colour'): 'TWO PAIR',
        ((2, 1, 1, 1), 'no_straight', 'no_colour'): 'PAIR',
        ((1, 1, 1, 1, 1), 'no_straight', 'no_colour'): 'HIGH CARD'
    }

    STRENGTH = {
        'STRAIGHT FLUSH': 9,
        'FOUR OF A KIND': 8,
        'FULL HOUSE': 7,
        'FLUSH': 6,
        'STRAIGHT': 5,
        'THREE OF A KIND': 4,
        'TWO PAIR': 3,
        'PAIR': 2,
        'HIGH CARD': 1
    }

    def __init__(self, hand):
        self.cards = self.parse_hand(hand)
        self.cards_count = {}
        self.hand = None
        self.strength = 0

        self.count_hand()
        self.sort_cards()  # sort cards considering poker hand ex. 3-2, 4-1, 2-2-1
        self.evaluate_hand()

    @staticmethod
    def parse_hand(hand):
        return [Card(card) for card in hand]

    def count_hand(self):
        card_values = [card.value for card in self.cards]
        self.cards_count = Counter(card_values)

        # My own Counter
        # c = 1
        # counts_list = {}
        # for a, b in zip(sorted_cards, sorted_cards[1:]+['']):
        #     if a != b:
        #         counts_list[a] = c
        #         c = 1
        #     else:
        #         c += 1

    def is_colour(self):
        flag = all(card.suit == self.cards[0].suit for card in self.cards)
        return ['no_colour', 'colour'][flag]

    def is_straight(self):
        sorted_card_values = [card.value for card in self.cards]

        # checking if ACE should have value 0 in this hand
        if sorted_card_values == [13, 4, 3, 2, 1]:
            self.cards[0].value = 0
            self.sort_cards()

        for card1, card2 in zip(self.cards, self.cards[1:]):
            if card2.value != card1.value - 1:
                return 'no_straight'
        else:
            return 'straight'

    def evaluate_hand(self):
        rank_counters = tuple(sorted(self.cards_count.values(), reverse=True))
        colour = self.is_colour()
        straight = self.is_straight()

        self.hand = self.HANDS.get((rank_counters, straight, colour))
        self.strength = self.STRENGTH.get(self.hand)

    def sort_cards(self):
        self.cards.sort(key=lambda x: (self.cards_count[x.value], x.value), reverse=True)

    def __lt__(self, other):
        if self.strength != other.strength:
            return self.strength < other.strength
        else:
            return self.cards < other.cards

    def __eq__(self, other):
        return self.strength == other.strength and self.cards == other.cards


class Card:
    SUITS = {
        'H': 'Hearts',
        'S': 'Spades',
        'D': 'Diamonds',
        'C': 'Clubs',
    }
    RANKS = '23456789TJQKA'

    def __init__(self, symbol):
        self.suit = ''
        self.rank = 0
        self.value = 0
        self.symbol = symbol
        self.parse_card(symbol)

    def parse_card(self, symbol):
        r = re.compile(r'(\d+|[TJQKA])([HSDC])')
        match = r.match(symbol)

        self.suit = self.SUITS[match.group(2)]
        self.rank = match.group(1)
        self.value = self.RANKS.index(self.rank) + 1

    def __repr__(self):
        old_repr = super(Card, self).__repr__()
        return '{} - {} of {}'.format(old_repr[-11:], self.rank, self.suit)

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value


def main():
    ans = 0
    with open('p054_poker.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            cards = line.split()
            hand1, hand2 = PokerHand(cards[:5]), PokerHand(cards[5:])
            ans += hand1 > hand2
    print(ans)


if __name__ == '__main__':
    main()
