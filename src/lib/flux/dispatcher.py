class Action:
    """
    Action is the basic class that all actions should inherit from
    """


class MessageSourceOptions:
    """
    Enumeration for identifying where a action originated
    """
    # The action originated from the server
    server = 0
    # The action originated from a view
    view = 1


class DispatcherMessage:
    """
    The dispatcher message class encapsulates an action with additional useful functionality
    """
    def __init__(self, source, action):
        """
        The constructor

        :param source: The action source (MessageSourceOptions)
        :param action: The action (As a class inheriting from Action)
        """
        # Check that the source is valid
        if source != MessageSourceOptions.server and source != MessageSourceOptions.view:
            # No
            raise Exception("Invalid Action source")

        # Check that the action is valid
        assert action

        # Record the parameters
        self._source = source
        self._action = action

        # The message has been matched yet
        self._matched = False

    @property
    def source(self):
        """
        Get the action source (MessageSourceOptions)

        :return: The action source
        """
        return self._source

    @property
    def action(self):
        """
        Get the action (Action)

        :return: The action
        """
        return self._action

    def first(self, cls, cb):
        """
        This function resets the matcher and then checks to see if the action class provided matches the action

        When processing messages, call this function first, followed by "next()" or "if_any_matched()"

        :param cls: The action class to check against
        :param cb: The callback to call if the action class matches the action of this message
        :return: self so that next/if_any_matched can be chained
        """
        # Reset the match
        self._matched = False

        # Check if the action in this message matches the class provided
        if type(self._action) is cls:
            # Yes it does, record that we had a message match
            self._matched = True
            # Trigger the callback with the action from this message
            cb(self._action)

        # Return self so that calls to this class can be chained
        return self

    def next(self, cls, cb):
        """
        Operates similarly to "first()", but does not reset the matcher

        Chain this call after a call to "first()"

        :param cls: The action class to check against
        :param cb: the callback to call if the action class matches the action of this message
        :return: self so that next/if_any_matched can be chained
        """
        # Check if the action in this message matches the class provided
        if type(self._action) is cls:
            # Yes it does, record that we had a message match
            self._matched = True
            # Trigger the callback with the action from this message
            cb(self._action)

        # Return self so that calls to this class can be chained
        return self

    def if_any_matched(self, cb):
        """
        If any actions were matched since a call to "first()" thin this function will trigger the callback specified

        If no action was matched, his function is a noop

        :param cb: The callback to trigger if a match has been found
        :return: Nothing
        """
        if self._matched:
            cb()


class AppDispatcher:
    """
    AppDispatcher is a class for proxying messages to various sinks, typically a sync would be a store
    """
    def __init__(self):
        # Initally create an empty array of dispatchers (message sinks)
        self._dispatchers = []

    def register(self, cb):
        """
        Registers a new dispatcher (message sink)

        :param cb: The callback to call when a message is received
        :return: Nothing
        """
        self._dispatchers.append(cb)

    def handle_view_action(self, action):
        """
        Handles dispatch of an action originating from a view

        :param action: The message to dispatch
        :return: Nothing
        """
        # Confirm that an action was provided
        assert action

        # Create the message from the action
        message = DispatcherMessage(MessageSourceOptions.view, action)

        # Iterate over the dispatchers and call each one with the provided message
        for dispatcher in self._dispatchers:
            # Call this dispatcher with the message
            dispatcher(message)

    def handle_server_action(self, action):
        """
        Handles dispatch of an action originating from the server

        :param action: The message to dispatch
        :return: Nothing
        """
        # Confirm that an action was provided
        assert action

        # Create the message from the action
        message = DispatcherMessage(MessageSourceOptions.view, action)

        # Iterate over the dispatchers and call each one with the provided message
        for dispatcher in self._dispatchers:
            # Call this dispatcher with the message
            dispatcher(message)
