"""
ZeroMQ signal transmission module for AdaptiveFX.

Publishes structured trading signals over a ZeroMQ PUB socket so that the
MetaTrader 5 Expert Advisor (subscribed on the other end) can receive and
execute them in near real-time.
"""

from __future__ import annotations

import json

from loguru import logger

from config.settings import settings


class SignalTransmitter:
    """Publishes trading signals via ZeroMQ PUB/SUB.

    Attributes:
        context: ZeroMQ Context instance.
        socket: ZeroMQ PUB socket.
        port: Port number on which the socket is bound.
        topic: ZeroMQ topic prefix prepended to every message.
    """

    def __init__(self) -> None:
        self.context = None
        self.socket = None
        self.port: int = settings.ZMQ_PUB_PORT
        self.topic: str = settings.ZMQ_TOPIC

    # ------------------------------------------------------------------
    def connect(self, port: int | None = None) -> None:
        """Set up and bind the ZeroMQ PUB socket.

        Args:
            port: TCP port to bind to.  Defaults to ``settings.ZMQ_PUB_PORT``.
        """
        # TODO: Initialise ZeroMQ context and bind PUB socket
        # import zmq
        # self.port = port or self.port
        # self.context = zmq.Context()
        # self.socket  = self.context.socket(zmq.PUB)
        # self.socket.bind(f"tcp://*:{self.port}")
        # logger.info(f"ZeroMQ PUB socket bound on port {self.port}.")
        logger.warning("connect() not yet implemented.")

    # ------------------------------------------------------------------
    def send(self, signal: dict) -> None:
        """Serialise and publish a signal dictionary.

        The message format is: ``"<TOPIC> <JSON_payload>\\n"``

        Args:
            signal: Signal dictionary as produced by
                :class:`signal.generator.SignalGenerator`.
        """
        # TODO: Serialise signal to JSON and send via PUB socket
        # if self.socket is None:
        #     logger.error("Socket not connected. Call connect() first.")
        #     return
        # payload = json.dumps(signal)
        # message = f"{self.topic} {payload}"
        # self.socket.send_string(message)
        # logger.debug(f"Signal sent → {message}")
        logger.warning(f"send() not yet implemented. Signal: {signal}")

    # ------------------------------------------------------------------
    def disconnect(self) -> None:
        """Close the ZeroMQ socket and terminate the context."""
        # TODO: Clean up ZeroMQ resources
        # if self.socket:
        #     self.socket.close()
        # if self.context:
        #     self.context.term()
        # logger.info("ZeroMQ PUB socket disconnected.")
        logger.warning("disconnect() not yet implemented.")
