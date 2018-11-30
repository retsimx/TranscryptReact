from lib.react.native import _react, _react_dom


class React:
    """
    React is the entry point to the React library. If you load React from a <script> tag, these top-level APIs are
    available on the React global. If you use ES6 with npm, you can write import React from 'react'. If you use ES5
    with npm, you can write var React = require('react').
    """

    @staticmethod
    def to_element_array(elements):
        """
        Takes an individual, or array of, [components, or elements, or strings etc], and converts that to a compatible
        react element array.

        This function takes care of the conversion of Component to Element
        """
        return [c.component if c.component else c for c in elements] if type(elements) is list else \
            elements.component if elements and elements.component else elements

    @staticmethod
    def create_element(_type, props, children):
        """
        React.createElement(
          type,
          [props],
          [...children]
        )

        Create and return a new React element of the given type. The type argument can be either a tag name string
        (such as 'div' or 'span'), a React component type (a class or a function), or a React fragment type.

        Code written with JSX will be converted to use React.createElement(). You will not typically invoke
        React.createElement() directly if you are using JSX. See React Without JSX to learn more.
        """
        return _react.createElement(
            _type, props,
            React.to_element_array(children)
        )

    @staticmethod
    def clone_element(element, props, children):
        """
        React.cloneElement(
          element,
          [props],
          [...children]
        )
        Clone and return a new React element using element as the starting point. The resulting element will have the
        original element’s props with the new props merged in shallowly. New children will replace existing children.
        key and ref from the original element will be preserved.

        React.cloneElement() is almost equivalent to:

        <element.type {...element.props} {...props}>{children}</element.type>

        However, it also preserves refs. This means that if you get a child with a ref on it, you won’t accidentally
        steal it from your ancestor. You will get the same ref attached to your new element.

        This API was introduced as a replacement of the deprecated React.addons.cloneWithProps().
        """
        return _react.cloneElement(element, props, children)

    @staticmethod
    def is_valid_element(o):
        """
        Verifies the object is a React element. Returns true or false.
        """
        return _react.isValidElement(o)

    @staticmethod
    def render(element, container):
        """
        Render a React element into the DOM in the supplied container and return a reference to the component (or
        returns null for stateless components).

        If the React element was previously rendered into container, this will perform an update on it and only mutate
        the DOM as necessary to reflect the latest React element.

        If the optional callback is provided, it will be executed after the component is rendered or updated.

        Note:

        ReactDOM.render() controls the contents of the container node you pass in. Any existing DOM elements inside are
        replaced when first called. Later calls use React’s DOM diffing algorithm for efficient updates.

        ReactDOM.render() does not modify the container node (only modifies the children of the container). It may be
        possible to insert a component to an existing DOM node without overwriting the existing children.

        ReactDOM.render() currently returns a reference to the root ReactComponent instance. However, using this return
        value is legacy and should be avoided because future versions of React may render components asynchronously in
        some cases. If you need a reference to the root ReactComponent instance, the preferred solution is to attach a
        callback ref to the root element.

        Using ReactDOM.render() to hydrate a server-rendered container is deprecated and will be removed in React 17.
        Use hydrate() instead.
        """
        return _react_dom.render(React.to_element_array(element), container)
