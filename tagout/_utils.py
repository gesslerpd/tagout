"""Utility functions."""

from html import escape


def class_names(obj):
    """Format class attribute value.

    :param obj: class names object
    :type obj: iterable or dict

    :returns: class attribute value
    :rtype: str

    """
    try:
        class_items = obj.items()
    except AttributeError:
        class_list = obj
    else:
        class_list = (class_name for class_name, value in class_items if value)
    return ' '.join(class_name.strip() for class_name in class_list)


def escape_text(text):
    """Escape text.

    :param text: text to escape
    :type text: str

    :returns: escaped text
    :rtype: str

    """
    return escape(text, quote=True)
