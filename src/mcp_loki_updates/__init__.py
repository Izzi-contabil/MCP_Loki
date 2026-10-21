"""Declarative instruction snapshots for the existing Loki host.

This package has no server, credentials, network, database, or user cache. The
host authenticates and authorizes every call using the returned requirements.
Input files come from a reviewed Git release; integrity checks are not a
malicious-content scanner and cannot replace that review.
"""

from .provider import InstructionsProvider, InstructionsUnavailable, InvalidDomain

__version__ = "0.1.3"
__all__ = ["InstructionsProvider", "InstructionsUnavailable", "InvalidDomain", "__version__"]
