"""rust-python-template: a Rust-core + PyO3 + Python-wrapper library template.

The public symbols here are re-exported from the compiled ``._core`` module,
which is built from the ``-ffi`` crate. Importing this package requires that
extension to have been built — run ``just develop`` or ``just bootstrap``.

Examples:
    >>> from rust_python_template import add
    >>> add(2, 3)
    5
    >>> add(-5, -7)
    -12
"""

from importlib.metadata import version as _version

from rust_python_template._core import add

__version__ = _version("rust-python-template")
__all__ = ["__version__", "add"]
