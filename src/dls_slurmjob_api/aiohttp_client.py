import asyncio
import copy
import json
import logging
import socket
from urllib.parse import urlparse

import aiohttp
from aiohttp.hdrs import METH_GET, METH_POST

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.explain import explain2
from dls_utilpack.require import require

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------
class AiohttpClient:
    """
    Object representing a client to an aiohttp server.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, aiohttp_specification):
        self.__aiohttp_specification = copy.deepcopy(aiohttp_specification)

        self.__endpoint = require(
            f"{callsign(self)} aiohttp specification",
            self.__aiohttp_specification,
            "client",
        )

        url_parts = urlparse(self.__aiohttp_specification["client"])
        self.__host = url_parts.hostname
        self.__port = url_parts.port
        self.__path = url_parts.path
        self.__host_colon_port = f"{url_parts.hostname}:{url_parts.port}"

        self.__api_version = require(
            f"{callsign(self)} aiohttp specification",
            self.__aiohttp_specification,
            "api_version",
        )

        authorization = require(
            f"{callsign(self)} aiohttp specification",
            self.__aiohttp_specification,
            "authorization",
        )

        authorization_type = require(
            f"{callsign(self)} aiohttp authorization",
            authorization,
            "type",
        )

        if authorization_type != "slurm_jwt_token":
            raise RuntimeError(
                f"{callsign(self)} aiohttp authorization type {authorization_type} not recognized"
            )

        self.__user = require(
            f"{callsign(self)} aiohttp authorization",
            authorization,
            "user",
        )
        self.__jwt_token = require(
            f"{callsign(self)} aiohttp authorization",
            authorization,
            "jwt_token",
        )

        self._client_session = None

        # Set log level default to avoid unwanted messages.
        logging.getLogger("aiohttp").setLevel(
            aiohttp_specification.get("log_level", "WARNING")
        )

    # ----------------------------------------------------------------------------------------
    def callsign(self):
        """"""
        return self.__aiohttp_specification["client"]

    # ----------------------------------------------------------------------------------------
    async def is_client_connection_possible(self):
        """"""

        if self.__endpoint.startswith("http"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.__host, self.__port))
            sock.close()
            # logger.debug(
            #     f"sock.connect_ex(({parts.hostname}, {parts.port})) result is {result}"
            # )
            return result == 0
        else:
            # TODO: Do proper check if client connection possible for unix pipe.
            await asyncio.sleep(0.100)
            return True

    # ----------------------------------------------------------------------------------------
    async def _establish_client_session(self):
        """"""

        if self._client_session is None:
            if self.__endpoint.startswith("http"):
                connector = None
                self.__client_netloc = self.__endpoint
            else:
                connector = aiohttp.UnixConnector(path=self.__path)
                self.__client_netloc = "http://unixconnector"

            self._client_session = aiohttp.ClientSession(connector=connector)

    # ----------------------------------------------------------------------------------------
    async def client_get(self, url, **kwargs):
        """"""

        return await self.client_request(METH_GET, url, **kwargs)

    # ----------------------------------------------------------------------------------------
    async def client_post(self, url, **kwargs):
        """"""

        return await self.client_request(METH_POST, url, **kwargs)

    # ----------------------------------------------------------------------------------------
    async def client_request(self, method, url, **kwargs):
        """"""
        await self._establish_client_session()

        if url.startswith("/"):
            url = url[1:]
        url = f"{self.__client_netloc}/slurm/{self.__api_version}/{url}"

        headers = kwargs.get("headers", {})
        headers = copy.deepcopy(headers)
        headers["Accept"] = "*/*"

        headers["Host"] = self.__host_colon_port
        headers["Content-Type"] = "application/json"
        headers["Connection"] = "close"

        headers["X-SLURM-USER-NAME"] = self.__user
        headers["X-SLURM-USER-TOKEN"] = self.__jwt_token

        kwargs["headers"] = headers

        async with self._client_session.request(
            method,
            url,
            **kwargs,
        ) as response:
            content_text = await response.text()

            try:
                content_json = json.loads(content_text)
                return content_json

            except Exception:
                pass

            raise RuntimeError(
                f"{url} error {response.status}: {response.reason}\n{content_text}"
            )

    # ----------------------------------------------------------------------------------------
    async def client_report_health(self):
        """"""
        await self._establish_client_session()

        try:
            response = await self.client_get("report_health")
        except Exception as exception:
            logger.error(
                explain2(exception, "[BADHEALTH] contacting server"), exc_info=exception
            )
            response = {"exception": str(exception)}

        return response

    # ----------------------------------------------------------------------------------------
    async def open_client_session(self):
        """"""

        await self._establish_client_session()

    # ----------------------------------------------------------------------------------------
    async def close_client_session(self):
        """"""

        if self._client_session is not None:
            # logger.debug("closing client session")

            await self._client_session.close()
            self._client_session = None
