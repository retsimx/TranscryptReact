from actions.actions import ButtonClickedAction
from lib.react.components.component import Component
from lib.react.dom import DOM as d

__pragma__('kwargs')


class Button(Component):
    """
    Example of a simple button component
    """

    class Props:
        """
        Define the props for this button component
        """

        def __init__(self, name='button', onclick=lambda x: False, key=None):
            # Record the props
            self.name = name
            self.onclick = onclick
            self.key = key

    def render(self):
        """
        Renders the button component

        :return: The react element/Component that describes our button
        """

        # Render a simple dom button
        return d.button(
            {'onClick': self.props.onclick},
            self.props.name
        )


class App(Component):
    """
    App is our root component for our application
    """

    class Props:
        """
        Define the props for our app component
        """

        def __init__(self, store, dispatcher):
            # Store and dispatcher are the only props we care about
            self.store = store
            self.dispatcher = dispatcher

    class State:
        """
        Define the state for our app component
        """

        def __init__(self, count=0):
            # A simple message state attribute to display the counter is all that is needed
            self.count = count

    def __init__(self, store, dispatcher):
        # Call the super constructor to pass in the initial props and the initial state
        super().__init__(App.Props(store, dispatcher), App.State)

    def render(self):
        """
        Renders our application

        :return: The react element/Component that represents our app component
        """
        # Check that the state is set, otherwise our component has not yet finished initialising
        if not self.state or not len(self.state):
            # Nothing left to do, return a null component
            return None

        # Render our application
        return d.div(None, [
            # Render the increase button
            Button(
                Button.Props(
                    'Decrease!',
                    # When it's clicked, trigger a button clicked action to decrease the counter
                    lambda: self.props.dispatcher.handle_view_action(ButtonClickedAction(False)),
                    0
                )
            ),
            # Render the decrease button
            Button(
                Button.Props(
                    'Increase!',
                    # When it's clicked, trigger a button clicked action to increase the counter
                    lambda: self.props.dispatcher.handle_view_action(ButtonClickedAction(True)),
                    1
                )
            ),
            # Draw a horizontal rule
            d.hr({'key': 2}),
            # Finally render a p tag with the count in it
            d.p({'key': 3}, self.state.count)
        ])

    def component_did_mount(self):
        """
        When the component mounts, register our app with the store so that we can receive updates

        :return: Nothing
        """
        self.props.store.register(self.on_change)

    def on_change(self):
        """
        Our on change callback that is triggered when the store that we are subscribed to handles a message

        :return: Nothing
        """
        # Get the new value of the counter from the store and update our state
        self.set_state(App.State(self.props.store.count))
