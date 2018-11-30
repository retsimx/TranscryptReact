# Full list of HTML5 tags
from lib.react.react import React

_tags = ["a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "b", "base", "basefont",
         "bdi", "bdo", "big", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code",
         "col", "colgroup", "datalist", "dd", "del", "details", "dfn", "dir", "div", "dl", "dt", "em", "embed",
         "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4",
         "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "keygen",
         "label", "legend", "li", "link", "map", "mark", "menu", "meta", "meter", "nav", "noframes", "noscript",
         "object", "ol", "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rp", "rt", "ruby", "s",
         "samp", "script", "section", "select", "small", "source", "span", "strike", "strong", "style", "sub",
         "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "tt", "u",
         "ul", "var", "video", "wbr"]


# Create a DOM class
class DOM:
    pass


# Iterate over tags and add functions to generate tags
for tag in _tags:
    # Create a new function scope so that the tag name is not lost
    def fn(_tag):
        # Add the tag to the DOM class
        setattr(DOM, _tag, lambda props, children: React.create_element(_tag, props, React.to_element_array(children)))


    # Call the scope breaking function
    fn(tag)
