"""
Implements the observer pattern and simulates a simple auction.
"""
import random
import names
import self as self


class Auctioneer:
    """
    The auctioneer acts as the "core". This class is responsible for
    tracking the highest bid and notifying the bidders if it changes.
    """

    def __init__(self):
        # This is the list of observers
        self.bidders = []
        self._highest_bid = 0
        self._highest_bidder = None

    @property
    def highest_bid(self):
        return self._highest_bid

    @highest_bid.setter
    def highest_bid(self, amt):
        self._highest_bid = amt

    @property
    def highest_bidder(self):
        return self._highest_bidder

    def register_bidder(self, bidder):
        """
        Adds a bidder to the list of tracked bidders.
        :param bidder: object with __call__(auctioneer) interface.
        """
        self.bidders.append(bidder)

    def reset_auctioneer(self):
        """
        Resets the auctioneer. Removes all the bidders and resets the
        highest bid to 0.
        """
        self.bidders.clear()
        self._highest_bid = 0

    def _notify_bidders(self):
        """
        Executes all the bidder callbacks. Should only be called if the
        highest bid has changed.
        """
        # when there is a new bid we have to notify all the bidders. so we use the bidder list to see
        # who has bid then we notify them and set the new highest bid. then we iterate thru them to see who
        # wants to bid more. if the call back is empty (?) we then accept the bid. we also clear the list again
        # so we can bid the next item in the prompt, while loop that i guess (?)

        for o in self.bidders:
            # let the bidder know someone bid, run the prob if they will be bidding again. keep repeating using callback
            # object until we reach the end watch for overflow? use yield
            if o != self._highest_bidder:
                o(self)

    def accept_bid(self, bid, bidder):
        """
        Accepts a new bid and updates the highest bid. This notifies all
        the bidders via their callbacks.
        :param bid: a float.
        :precondition bid: should be higher than the existing bid.
        :param bidder: The object with __call__(auctioneer) that placed
        the bid.
        """
        if self._highest_bid < bid:
            self._highest_bid = bid
            self._highest_bidder = bidder
            self._notify_bidders()


class Bidder:

    def __init__(self, name, budget=100.00, bid_probability=0.35, bid_increase_perc=1.1):
        self.name = name
        self.bid_probability = bid_probability
        self.budget = budget
        self.bid_increase_perc = bid_increase_perc
        self.highest_bid = 0

    def __call__(self, auctioneer: Auctioneer):
        my_bid = (self.bid_increase_perc * auctioneer.highest_bid)
        self.budget = (self.budget - my_bid)
        if auctioneer.highest_bidder != self and my_bid <= self.budget and random.random() < self.bid_probability:
            this_current_object = auctioneer.highest_bidder
            self.highest_bid = my_bid

            if this_current_object is None:
                print(
                    f"{self.name} bidded ${self.highest_bid} in response to the starting "
                    f"price of ${auctioneer.highest_bid}!")
            else:
                print(
                    f"{self.name} bidded ${self.highest_bid} in response to {this_current_object.name}'s bid of "
                    f"${this_current_object.highest_bid}!")

            auctioneer.accept_bid(my_bid, self)

    def __str__(self):
        return f"{self.name} at ${self.highest_bid}"

    def __repr__(self):
        return f"{self.name}\t {self.bid_probability}\t ${self.budget}\t {self.bid_increase_perc}\t${self.highest_bid}"


class Auction:
    """
    Simulates an auction. Is responsible for driving the auctioneer and
    the bidders.
    """

    def __init__(self, bidders):
        """
        Initialize an auction. Requires a list of bidders that are
        attending the auction and can bid.
        :param bidders: sequence type of objects of type Bidder
        """
        self._bidder_list = bidders
        self._auctioneer = Auctioneer()

    def simulate_auction(self, item, start_price):
        """
        Starts the auction for the given item at the given starting
        price. Drives the auction till completion and prints the results.
        :param item: string, name of item.
        :param start_price: float
        """
        self._auctioneer.highest_bid = start_price
        print(f"Auctioning {item} starting at ${start_price}")

        for bid_placer in self._bidder_list:
            bid_placer(self._auctioneer)
        if self._auctioneer.highest_bidder is None:
            print("There is no winners of the auction.")
        else:
            print(
                f"\nThe winner of the auction is: {self._auctioneer.highest_bidder}\n")
            # using dictionary comprehension to check if someone actually bid, if not,
            # do not display the bid in the summary
        summary = {bidder.name: bidder.highest_bid for bidder in self._bidder_list if bidder.highest_bid > 0}
        for name, high in summary.items():
            print(f"Bidder: {name}\t Highest Bid: ${high}")


def main():
    bidders = []
    create_user = True

    # Hardcoding the bidders.
    bidders.append(Bidder("Jojo", 3000, random.random(), 1.2))
    bidders.append(Bidder("Melissa", 7000, random.random(), 1.5))
    bidders.append(Bidder("Priya", 15000, random.random(), 1.1))
    bidders.append(Bidder("Kewei", 800, random.random(), 1.9))
    bidders.append(Bidder("Scott", 4000, random.random(), 2))

    item = input("What is the item that is being auctioned?")
    price = input("What is the starting price?")
    #
    # default = input("Do you want default bidders or to create your own? (y/n)")
    #
    # if default == 'y':
    #     bidders.append(Bidder("Jojo", 3000, random.random(), 1.2))
    #     bidders.append(Bidder("Melissa", 7000, random.random(), 1.5))
    #     bidders.append(Bidder("Priya", 15000, random.random(), 1.1))
    #     bidders.append(Bidder("Kewei", 800, random.random(), 1.9))
    #     bidders.append(Bidder("Scott", 4000, random.random(), 2))
    #     create_user = False
    # elif default == 'n':
    # create_user = True
    #
    while create_user:
        name = input("What is the bidders name?")
        budget = input("What is the bidders budget?")
        incr = input("How much will the bidder increase the previous bid by?")
        bidders.append(Bidder(name, float(budget), random.random(), float(incr)))
        create_user = False
        choice = input("Do you want to create another user? (y/n)")
        if choice.__contains__('y'):
            create_user = True
        elif choice.__contains__('n'):
            create_user = False
        else:
            print("Invalid entry, please enter y/n")

    #
    #
    #
    # for b in bidders:
    #     print(b.__repr__())
    print("\n\nStarting Auction!!")
    print("------------------")
    my_auction = Auction(bidders)
    my_auction.simulate_auction(item, float(price))


if __name__ == '__main__':
    main()