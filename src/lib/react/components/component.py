from lib.react.components.utils import native_component_wrapper


class Component:
    """
    React.Component is the base class for React components when they are defined using ES6 classes:

    class Greeting extends React.Component {
      render() {
        return <h1>Hello, {this.props.name}</h1>;
      }
    }

    See the React.Component API Reference for a list of methods and properties related to the base React.Component
    class.
    """
    def __init__(self, props, state=None):
        # Create the actual react element that we'll use as the proxy
        self.__react_proxy = native_component_wrapper(self, props, state)

    def render(self):
        """
        The render() method is the only required method in a class component.

        When called, it should examine this.props and this.state and return one of the following types:

        * React elements. Typically created via JSX. For example, <div /> and <MyComponent /> are React elements
            that instruct React to render a DOM node, or another user-defined component, respectively.
        * Arrays and fragments. Let you return multiple elements from render. See the documentation on fragments for
            more details.
        * Portals. Let you render children into a different DOM subtree. See the documentation on portals for more
            details.
        * String and numbers. These are rendered as text nodes in the DOM.
        * Booleans or null. Render nothing. (Mostly exists to support return test && <Child /> pattern, where test
            is boolean.)

        The render() function should be pure, meaning that it does not modify component state, it returns the same
        result each time it’s invoked, and it does not directly interact with the browser.

        If you need to interact with the browser, perform your work in componentDidMount() or the other lifecycle
        methods instead. Keeping render() pure makes components easier to think about.

        Note
            render() will not be invoked if shouldComponentUpdate() returns false.
        """
        raise Exception("Render must be implemented")

    def component_did_mount(self):
        """
        componentDidMount() is invoked immediately after a component is mounted (inserted into the tree).
        Initialization that requires DOM nodes should go here. If you need to load data from a remote endpoint,
        this is a good place to instantiate the network request.

        This method is a good place to set up any subscriptions. If you do that, don’t forget to unsubscribe in
        componentWillUnmount().

        You may call setState() immediately in componentDidMount(). It will trigger an extra rendering, but it will
        happen before the browser updates the screen. This guarantees that even though the render() will be called
        twice in this case, the user won’t see the intermediate state. Use this pattern with caution because it
        often causes performance issues. In most cases, you should be able to assign the initial state in the
        constructor() instead. It can, however, be necessary for cases like modals and tooltips when you need to
        measure a DOM node before rendering something that depends on its size or position.
        """

    def component_will_unmount(self):
        """
        componentWillUnmount() is invoked immediately before a component is unmounted and destroyed. Perform any
        necessary cleanup in this method, such as invalidating timers, canceling network requests, or cleaning up
        any subscriptions that were created in componentDidMount().

        You should not call setState() in componentWillUnmount() because the component will never be re-rendered.
        Once a component instance is unmounted, it will never be mounted again.
        """

    def should_component_update(self, next_props, next_state):
        """
        Use shouldComponentUpdate() to let React know if a component’s output is not affected by the current change
        in state or props. The default behavior is to re-render on every state change, and in the vast majority of
        cases you should rely on the default behavior.

        shouldComponentUpdate() is invoked before rendering when new props or state are being received. Defaults to
        true. This method is not called for the initial render or when forceUpdate() is used.

        This method only exists as a performance optimization. Do not rely on it to “prevent” a rendering, as this
        can lead to bugs. Consider using the built-in PureComponent instead of writing shouldComponentUpdate() by
        hand. PureComponent performs a shallow comparison of props and state, and reduces the chance that you’ll
        skip a necessary update.

        If you are confident you want to write it by hand, you may compare this.props with nextProps and this.state
        with nextState and return false to tell React the update can be skipped. Note that returning false does not
        prevent child components from re-rendering when their state changes.

        We do not recommend doing deep equality checks or using JSON.stringify() in shouldComponentUpdate(). It is
        very inefficient and will harm performance.

        Currently, if shouldComponentUpdate() returns false, then UNSAFE_componentWillUpdate(), render(), and
        componentDidUpdate() will not be invoked. In the future React may treat shouldComponentUpdate() as a hint
        rather than a strict directive, and returning false may still result in a re-rendering of the component.
        """
        return True

    def component_did_update(self, previous_props, previous_state, snapshot):
        """
        componentDidUpdate() is invoked immediately after updating occurs. This method is not called for the initial
        render.

        Use this as an opportunity to operate on the DOM when the component has been updated. This is also a good
        place to do network requests as long as you compare the current props to previous props (e.g. a network
        request may not be necessary if the props have not changed).

        componentDidUpdate(prevProps) {
          // Typical usage (don't forget to compare props):
          if (this.props.userID !== prevProps.userID) {
            this.fetchData(this.props.userID);
          }
        }

        You may call setState() immediately in componentDidUpdate() but note that it must be wrapped in a condition
        like in the example above, or you’ll cause an infinite loop. It would also cause an extra re-rendering
        which, while not visible to the user, can affect the component performance. If you’re trying to “mirror”
        some state to a prop coming from above, consider using the prop directly instead. Read more about why
        copying props into state causes bugs.

        If your component implements the getSnapshotBeforeUpdate() lifecycle (which is rare), the value it returns
        will be passed as a third “snapshot” parameter to componentDidUpdate(). Otherwise this parameter will be
        undefined.

        Note
            componentDidUpdate() will not be invoked if shouldComponentUpdate() returns false.
        """

    def get_snapshot_before_update(self, previous_props, previous_state):
        """
        getSnapshotBeforeUpdate() is invoked right before the most recently rendered output is committed to e.g.
        the DOM. It enables your component to capture some information from the DOM (e.g. scroll position) before
        it is potentially changed. Any value returned by this lifecycle will be passed as a parameter to
        componentDidUpdate().

        This use case is not common, but it may occur in UIs like a chat thread that need to handle scroll position
        in a special way.

        A snapshot value (or null) should be returned.
        """
        return None

    def component_did_catch(self, error, info):
        """
        This lifecycle is invoked after an error has been thrown by a descendant component. It receives two
        parameters:

        * error - The error that was thrown.
        * info - An object with a componentStack key containing information about which component threw the error.

        componentDidCatch() is called during the “commit” phase, so side-effects are permitted.
        """

    @property
    def state(self):
        """
        The state contains data specific to this component that may change over time. The state is user-defined,
        and it should be a plain JavaScript object.

        If some value isn’t used for rendering or data flow (for example, a timer ID), you don’t have to put it in
        the state. Such values can be defined as fields on the component instance.

        See State and Lifecycle for more information about the state.

        Never mutate this.state directly, as calling setState() afterwards may replace the mutation you made. Treat
        this.state as if it were immutable.
        """
        return self.__react_proxy.component_instance.state or {}

    @property
    def props(self):
        """
        this.props contains the props that were defined by the caller of this component. See Components and Props
        for an introduction to props.

        In particular, this.props.children is a special prop, typically defined by the child tags in the JSX
        expression rather than in the tag itself.
        """
        return self.__react_proxy.component_instance.props or {}

    @property
    def children(self):
        """
        Returns any children this instance has as an array
        """
        # Check if there are actually any children
        if self.props and self.props.children:
            # Is the children already in an array?
            if type(self.props.children) is list:
                # Yes, return the children array
                return self.props.children
            else:
                # No, convert the children (probably a single element or string etc) to an array with one item and
                # return it
                return [self.props.children]

        # There are no children, return an empty array
        return []

    @property
    def component(self):
        """
        Used to return the actual react component instance (that acts as a proxy for this instance), for rendering
        as a child element
        """
        return self.__react_proxy._reactElement

    def set_state(self, state, cb=None):
        """
        setState() enqueues changes to the component state and tells React that this component and its children
        need to be re-rendered with the updated state. This is the primary method you use to update the user
        interface in response to event handlers and server responses.

        Think of setState() as a request rather than an immediate command to update the component. For better
        perceived performance, React may delay it, and then update several components in a single pass. React does
        not guarantee that the state changes are applied immediately.

        setState() does not always immediately update the component. It may batch or defer the update until later.
        This makes reading this.state right after calling setState() a potential pitfall. Instead, use
        componentDidUpdate or a setState callback (setState(updater, callback)), either of which are guaranteed to
        fire after the update has been applied. If you need to set the state based on the previous state, read
        about the updater argument below.

        setState() will always lead to a re-render unless shouldComponentUpdate() returns false. If mutable objects
        are being used and conditional rendering logic cannot be implemented in shouldComponentUpdate(), calling
        setState() only when the new state differs from the previous state will avoid unnecessary re-renders.

        The first argument is an updater function with the signature:

        (state, props) => stateChange

        state is a reference to the component state at the time the change is being applied. It should not be
        directly mutated. Instead, changes should be represented by building a new object based on the input from
        state and props. For instance, suppose we wanted to increment a value in state by props.step:

        this.setState((state, props) => {
          return {counter: state.counter + props.step};
        });

        Both state and props received by the updater function are guaranteed to be up-to-date. The output of the
        updater is shallowly merged with state.

        The second parameter to setState() is an optional callback function that will be executed once setState is
        completed and the component is re-rendered. Generally we recommend using componentDidUpdate() for such
        logic instead.

        You may optionally pass an object as the first argument to setState() instead of a function:

        setState(stateChange[, callback])

        This performs a shallow merge of stateChange into the new state, e.g., to adjust a shopping cart item
        quantity:

        this.setState({quantity: 2})

        This form of setState() is also asynchronous, and multiple calls during the same cycle may be batched
        together. For example, if you attempt to increment an item quantity more than once in the same cycle,
        that will result in the equivalent of:

        Object.assign(
          previousState,
          {quantity: state.quantity + 1},
          {quantity: state.quantity + 1},
          ...
        )

        Subsequent calls will override values from previous calls in the same cycle, so the quantity will only be
        incremented once. If the next state depends on the current state, we recommend using the updater function
        form, instead:

        this.setState((state) => {
          return {quantity: state.quantity + 1};
        });
        """
        self.__react_proxy.component_instance.setState(state, cb)

    def force_update(self, cb):
        """
        By default, when your component’s state or props change, your component will re-render. If your render()
        method depends on some other data, you can tell React that the component needs re-rendering by calling
        forceUpdate().

        Calling forceUpdate() will cause render() to be called on the component, skipping shouldComponentUpdate().
        This will trigger the normal lifecycle methods for child components, including the shouldComponentUpdate()
        method of each child. React will still only update the DOM if the markup changes.

        Normally you should try to avoid all uses of forceUpdate() and only read from this.props and this.state in
        render().
        """
        self.__react_proxy.component_instance.forceUpdate(cb)
