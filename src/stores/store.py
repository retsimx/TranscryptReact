from actions.actions import StoreInitialisedAction, ButtonClickedAction
from lib.flux.store import Store


class MyStore(Store):
    """
    A simple store to track a single counter for our application
    """

    def __init__(self, dispatcher):
        """
        Initialises our store

        :param dispatcher: The dispatcher that we should register with to handle messages
        """
        # Call the super constructor to handle the boilerplate
        super().__init__(dispatcher)

        # Set the initial value of our counter to 100
        self.count = 100

    def handle_message(self, message):
        """
        This function is called from the dispatcher when it receives a message

        :param message: The message
        :return: Nothing
        """
        # Call first to reset the message matcher
        message.first(
            # Check if this message is for a StoreInitialisedAction
            StoreInitialisedAction,
            # If so, no action required
            lambda x: x

            # Call next to see if the next message matches
        ).next(
            # Check if this message is for a ButtonClickedAction
            ButtonClickedAction,
            # If it is, call the handle_button_press function
            self.handle_button_press

            # Were any messages matched?
        ).if_any_matched(
            # If we handled any message, call the on_change callback
            self.on_change
        )

    def handle_button_press(self, action):
        """
        Handle the button press
        :param action: The action that was sent
        :return: Nothing
        """
        if action.increase:
            self.count += 1
        else:
            self.count -= 1
