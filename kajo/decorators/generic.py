# -*- coding: utf-8 -*-

from kajo.utils import RecordDict


def objectify(method):
    """Decorator that converts <dict> to instance of <RecordDict>."""
    def objectify_wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        if isinstance(result, dict):
            result = RecordDict(**result)
        elif isinstance(result, (list, tuple)):
            type_ = type(result)
            result = type_(RecordDict(**elm) for elm in result)

        return result
    return objectify_wrapper
