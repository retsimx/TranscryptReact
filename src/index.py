from actions.actions import StoreInitialisedAction
from components.app import App
from lib.flux.dispatcher import AppDispatcher
from lib.react.react import React
from stores.store import MyStore

# Create a dispatcher to route messages
dispatcher = AppDispatcher()

# Create a store to track the state of our application
store = MyStore(dispatcher)

# Create our app and mount it in the dom
React.render(
    # Create our application component specifying the store and the dispatcher
    App(store, dispatcher),
    # Get the dom element to mount our application to
    document.getElementById('container')
)

# Now that our application is mounted, tell it that we have initialised the store
dispatcher.handle_view_action(StoreInitialisedAction(store))
