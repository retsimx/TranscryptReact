class Store:
    """
    The store is a basic class that tracks the state of the application or some component

    This class should be inherited from, as it is just a utility class to handle some boilerplate
    """
    def __init__(self, dispatcher):
        """
        Creates the store and registers it with the provided dispatcher

        :param dispatcher: The dispatcher to register this store with
        """
        # Confirm that a dispatcher was actually provided
        assert dispatcher

        # Record the dispatcher for user in inherited classes
        self._dispatcher = dispatcher

        # Register our message handler with the dispatcher
        self._dispatcher.register(self.handle_message)

        # Create an empty array to track components that should update when we have consumed a message
        self._change_receiver = []

    def handle_message(self, message):
        """
        Called by the dispatcher to handle a message

        :param message: The message to handle
        :return: Nothing
        """
        raise Exception("handle_message must be implemented")

    def register(self, cb):
        """
        This function registers a callback to be triggered if we consume a message

        :param cb: The callback to trigger
        :return: Nothing
        """
        # Add the callback to the list of receivers
        self._change_receiver.append(cb)

    def unregister(self, cb):
        """
        Called to remove a callback from tthe list of change receivers

        :param cb: The callback to remove
        :return: Nothing
        """
        # Remove the callback
        self._change_receiver.remove(cb)

    def on_change(self):
        """
        Utility function that is used to call any change receivers if any messages were consumed by this store

        This function should be passed to if_any_matched from the message passed to handle_massage

        :return: Nothing
        """
        # Iterate over the change receivers and trigger each callback
        for cb in self._change_receiver:
            # Trigger the callback
            cb()

    @property
    def dispatcher(self):
        """
        Returns the dispatcher that this store is registered with
        """
        return self._dispatcher
