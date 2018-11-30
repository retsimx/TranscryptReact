from lib.react.native import _react
from lib.react.react import React

_react_component_classes = {}


def native_component_wrapper(parent, props, cls_state=None, children=None):
    """
    Creates a new react class for the parent component if one does not exist, then instantiates it. The class wraps a
    proxy Component class that is responsible for calling various functions from the parent component, and also handles
    the parent component calling various element functions like setState etc
    """
    # Create a scoped variable to store the component instance
    component_instance = None

    # noinspection PyUnresolvedReferences,PyPep8Naming
    class _Component(object, _react.Component.prototype):
        """
        The proxy Component class
        """

        def __init__(self):
            """
            Checks to see if a react class exists yet for the specified parent component, if not it creates a new react
            class that is then reused for all instances of the parent class. It then instantiates the class and returns
            the instantiated class
            """
            # Get the type of the parent
            current_type = type(parent)
            # Construct the type "name" for the class
            current_type = current_type.__module__ + '.' + current_type.__name__

            # Check if the react class for the parent exists yet
            if current_type in _react_component_classes:
                # Yes, get the existing react class and re-use it
                react_component_class = _react_component_classes[current_type]
            else:
                # No, create the react class for the parent
                react_component_class = _create_class(self, current_type)
                # Record the class for reuse later
                _react_component_classes[current_type] = react_component_class

            # Create the initial arguments to instantiate the react class
            create_elems_args = [react_component_class, props]

            # Check if there are any children
            if children:
                # Convert the children to an element array and add it to the creation parameters
                create_elems_args.append(React.to_element_array(children))

            # Instantiate the react element
            self._reactElement = _react.createElement.apply(None, create_elems_args)

        @staticmethod
        def constructorStateInitialiser():
            """
            Called whenever the react class is instantiated to get the default state if one was provided
            """
            return cls_state() if cls_state else {}

        @staticmethod
        def render():
            """
            React render proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            return parent.render()

        @staticmethod
        def componentDidMount():
            """
            React componentDidMount proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            parent.component_did_mount()

        @staticmethod
        def componentWillUnmount():
            """
            React componentWillUnmount proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            parent.component_will_unmount()

        @staticmethod
        def shouldComponentUpdate(next_props, next_state):
            """
            React shouldComponentUpdate proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            return parent.should_component_update(next_props, next_state)

        @staticmethod
        def componentDidUpdate(previous_props, previous_state, snapshot):
            """
            React componentDidUpdate proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            parent.component_did_update(previous_props, previous_state, snapshot)

        @staticmethod
        def getSnapshotBeforeUpdate(previous_props, previous_state):
            """
            React getSnapshotBeforeUpdate proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            return parent.get_snapshot_before_update(previous_props, previous_state)

        @staticmethod
        def componentDidCatch(error, info):
            """
            React componentDidCatch proxy function
            """
            # Remember the component instance
            component_instance.component_instance = this
            # Call the original function
            parent.component_did_catch(error, info)

    # Create the component instance and return the proxy class
    component_instance = _Component()
    return component_instance


# noinspection PyUnresolvedReferences
def _create_class(proxy, display_name):
    """
    Utility function for creating a react class for the specified proxy class with the specified name
    """
    assert proxy
    assert display_name

    # Magic javascript for generating a class that inherits from both React.Component and the proxy class
    __pragma__(
        'js',
        '''
        function react_component_class_creator_utils_create_class(template, displayName) {{
            function getOwnPropertyDescriptors(obj) {{ // IE11 doesn't support Object.getOwnPropertyDescriptors so use this
                var result = {{}};
                var arrPropertyNames = Object.getOwnPropertyNames(obj); // IE11 doesn't support "var key of Reflect.ownKeys(obj)" but this approach should suffice for Bridge classes
                for (var i = 0; i < arrPropertyNames.length; i++) {{
                    var key = arrPropertyNames[i];
                    result[key] = Object.getOwnPropertyDescriptor(obj, key);
                }}
                return result;
            }}

            let reactComponentClass = null;

            // Use the displayName to name the component class function (React DevTools will use this)
            eval("reactComponentClass = function " + displayName + "(props) {{ window.react_component_class_creator_utils_initialise_component_state(this, template, props); }}");

            // Set the React.Component base class
            reactComponentClass.prototype = Object.create(
                _react.Component && _react.Component.prototype,
            );
            if (Object.setPrototypeOf) {{
                Object.setPrototypeOf(reactComponentClass, _react.Component);
            }}
            else {{
                reactComponentClass.__proto__ = _react.Component;
            }}
            // Attach the members
            var protoStack = [];
            var o = template.__proto__;
            while (o) {{
                protoStack.push(o);
                o = o.__proto__;
            }}
            for (var i = protoStack.length - 1; i >= 0; i--) {{
                o = protoStack[i];
                var descriptors = getOwnPropertyDescriptors(o);
                for (var name in descriptors) {{
                    var descriptor = descriptors[name];
                    if (descriptor instanceof Object)
                        Object.defineProperty(reactComponentClass.prototype, name, descriptor);
                }}
            }}

            return reactComponentClass;
        }}

        function react_component_class_creator_utils_initialise_component_state(instance, template, props) {{
            var getInitialState = template.constructorStateInitialiser;
            if ((typeof(getInitialState) !== "function") || (getInitialState.length !== 0)) {{
                return;
            }}
            instance.props = props;

            var state = getInitialState.call(instance);
            if (state) {{
                instance.state = state;
            }}
        }}

        window.react_component_class_creator_utils_initialise_component_state = 
        react_component_class_creator_utils_initialise_component_state;
        '''
    )

    # Create the react class and return it
    return react_component_class_creator_utils_create_class(proxy, display_name.replace('.', '_'))
