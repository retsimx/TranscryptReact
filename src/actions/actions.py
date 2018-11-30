from lib.flux.dispatcher import Action


class StoreInitialisedAction(Action):
    """
    This action is dispatched when the store has completed setup, and the root app component is mounted
    """
    def __init__(self, store):
        """
        :param store: The store that is initialised
        """
        # Make sure that the store was provided
        assert store

        # Record the parameters
        self.store = store


class ButtonClickedAction(Action):
    """
    This action is dispatched when one of the buttons is clicked to indicate that the counter should be increased or
    decreased
    """
    def __init__(self, increase):
        """
        :param increase: True if the counter should be increased, otherwise false
        """

        # Record the parameters
        self.increase = increase
