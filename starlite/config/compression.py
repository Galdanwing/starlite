from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from starlite.exceptions import ImproperlyConfiguredException
from starlite.middleware.compression import CompressionMiddleware

__all__ = ("CompressionConfig",)


@dataclass
class CompressionConfig:
    """Configuration for response compression.

    To enable response compression, pass an instance of this class to the :class:`Starlite <.app.Starlite>` constructor
    using the ``compression_config`` key.
    """

    backend: Literal["gzip", "brotli"]
    """Literal of "gzip" or "brotli"."""
    minimum_size: int = field(default=500)
    """Minimum response size (bytes) to enable compression, affects all backends."""
    gzip_compress_level: int = field(default=9)
    """Range ``[0-9]``, see :doc:`python:library/gzip`."""
    brotli_quality: int = field(default=5)
    """Range ``[0-11]``, Controls the compression-speed vs compression-density tradeoff.

    The higher the quality, the slower the compression.
    """
    brotli_mode: Literal["generic", "text", "font"] = "text"
    """``MODE_GENERIC``, ``MODE_TEXT`` (for UTF-8 format text input, default) or ``MODE_FONT`` (for WOFF 2.0)."""
    brotli_lgwin: int = field(default=22)
    """Base 2 logarithm of size.

    Range is 10 to 24. Defaults to 22.
    """
    brotli_lgblock: Literal[0, 16, 17, 18, 19, 20, 21, 22, 23, 24] = 0
    """Base 2 logarithm of the maximum input block size.

    Range is ``16`` to ``24``. If set to ``0``, the value will be set based on the quality. Defaults to ``0``.
    """
    brotli_gzip_fallback: bool = True
    """Use GZIP if Brotli is not supported."""
    middleware_class: type[CompressionMiddleware] = CompressionMiddleware
    """Middleware class to use, should be a subclass of :class:`CompressionMiddleware`."""
    exclude: str | list[str] | None = None
    """A pattern or list of patterns to skip in the compression middleware."""
    exclude_opt_key: str | None = None
    """An identifier to use on routes to disable compression for a particular route."""

    def __post_init__(self) -> None:
        if self.minimum_size <= 0:
            raise ImproperlyConfiguredException("minimum_size must be greater than 0")

        if self.gzip_compress_level < 0 or self.gzip_compress_level > 9:
            raise ImproperlyConfiguredException("gzip_compress_level must be a value between 0 and 9")

        if self.brotli_quality < 0 or self.brotli_quality > 11:
            raise ImproperlyConfiguredException("brotli_quality must be a value between 0 and 11")

        if self.brotli_lgwin < 10 or self.brotli_lgwin > 24:
            raise ImproperlyConfiguredException("brotli_lgwin must be a value between 10 and 24")
