#!/usr/bin/env python3

"""
** Allows a 'Printer' to behave like a decorator. **
----------------------------------------------------

Thus, it is possible to make a function call verbose, and in particular to time it.
"""

import inspect
import os

from context_printer.printer import Printer


def decorate(func):
    """
    ** Makes a function verbose. **

    Parameters
    ----------
    func : callable
        The function that we want to decorate.

    Returns
    -------
    callable
        The decorating function.

    Examples
    --------
    >>> from context_printer.memory import reset_lifo
    >>> reset_lifo()
    >>> from context_printer.decorator import decorate
    >>>
    >>> @decorate
    ... def f(x, y): pass
    ...
    >>> f(0, 0) # doctest: +SKIP
    Call f(0, 0)
    █ done, total elapsed time: 3.34 us
    >>> f(0, y=1) # doctest: +SKIP
    Call f(0, y=1)
    █ done, total elapsed time: 1.43 us
    >>> f(x=1, y=1) # doctest: +SKIP
    Call f(x=1, y=1)
    █ done, total elapsed time: 1.19 us
    >>>
    """
    file = inspect.getfile(func)
    if not os.path.exists(file):
        file = None
    try:
        lineno = inspect.currentframe().f_back.f_back.f_lineno
    except AttributeError:
        lineno = None
    name = func.__name__

    def decorated(*args, **kwargs):
        signature_kwargs = ', '.join(f'{k}={repr(kwargs[k])}' for k in sorted(kwargs))
        signature = ', '.join(repr(arg) for arg in args)
        if signature_kwargs:
            if signature:
                signature += ', '
            signature += signature_kwargs
        message = f'Call {name}({signature})'
        if file is not None:
            message += f' from {file}'
        if lineno is not None and file is not None:
            message += f' l{lineno}'

        with Printer(message) as ctp:
            res = func(*args, **kwargs)
            ctp.print(f'done, total elapsed time: {ctp.elapsed_time()}')
            return res

    return decorated
