"""Module with the logic regarding the IGDB interaction."""

import time
from abc import ABC
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Self, TypeAlias

import requests
from django.conf import settings
from requests_futures.sessions import FuturesSession

IGDB_OBJECT: TypeAlias = "IGDBPlatformResponse | IGDBGenreResponse | IGDBCompanyResponse | IGDBGameResponse"
IGDB_API_RESPONSE: TypeAlias = list[IGDB_OBJECT]


class IGDBEndpoints(StrEnum):
    """IGDB endpoints used in the application."""

    GENRES = "genres"
    PLATFORMS = "platforms"
    GAMES = "games"
    COMPANIES = "companies"


@dataclass
class IGDBAuthenticationResponse:
    """Class representing the data structure for IGDB authentication success response."""

    access_token: str
    """The access token for IGDB."""
    expires_in: int
    """The number of seconds before the access token expires."""
    token_type: str
    """The type of the access token."""


@dataclass
class BaseIGDBResponse(ABC):
    """Class representing the base data structure for IGDB responses."""

    id: int
    """The ID of the object in IGDB."""


@dataclass
class IGDBImageResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB image response."""

    image_id: str
    """The ID of the image used to construct an IGDB image link."""


@dataclass
class IGDBPlatformResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB platform response."""

    name: str
    """The name of the platform."""
    abbreviation: str = ""
    """An abbreviation of the platform name."""


@dataclass
class IGDBGenreResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB genre response."""

    name: str
    """The name of the genre."""


@dataclass
class IGDBCompanyResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB company response."""

    name: str
    """The name of the company."""
    logo: IGDBImageResponse | None = None
    """The company's logo."""

    def __post_init__(self: Self) -> None:
        """Post initializer."""
        if self.logo and isinstance(self.logo, dict):
            self.logo = IGDBImageResponse(**self.logo)


@dataclass
class IGDBInvolvedCompanyResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB involved company response."""

    company: int
    """Reference ID for Company object."""
    developer: bool
    """If it is a developer."""
    publisher: bool
    """If it is a publisher."""


@dataclass
class IGDBGameResponse(BaseIGDBResponse):
    """Class representing the data structure for IGDB game response."""

    name: str
    """The name of the game."""
    cover: IGDBImageResponse | None = None
    """The cover of this game."""
    first_release_date: int | None = None
    """The first release date for this game."""
    genres: list[int] | None = None
    """The list of the genres IDs for this game."""
    involved_companies: list[IGDBInvolvedCompanyResponse] | None = None
    """The list of involved companies for this game."""
    platforms: list[int] | None = None
    """The list of platforms IDs for this game."""
    summary: str = ""
    """A description of the game."""

    def __post_init__(self: Self) -> None:
        """Post initializer."""
        if self.cover and isinstance(self.cover, dict):
            self.cover = IGDBImageResponse(**self.cover)

        if self.involved_companies and isinstance(self.involved_companies, list):
            self.involved_companies = [
                IGDBInvolvedCompanyResponse(
                    **company,
                )
                for company in self.involved_companies
                if isinstance(company, dict)
            ]


class IGDBInteractionError(Exception):
    """IGDB interaction error."""


class IGDBWrapper:
    """IGDB wrapper class."""

    IGDB_AUTHENTICATION_URL = (
        "https://id.twitch.tv/oauth2/token"
        f"?client_id={settings.IGDB_CLIENT_ID}&client_secret={settings.IGDB_CLIENT_SECRET}&grant_type=client_credentials"
    )
    IGDB_BASE_URL = "https://api.igdb.com/v4/"
    QUERY_ITEM_LIMIT = 500
    MAX_REQUESTS_TO_IGDB = 4

    def __init__(self: Self) -> None:
        """Initialize the IGDB wrapper."""
        _access_token = self.get_igdb_access_token()
        self._basic_auth_headers = {
            "Client-ID": settings.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {_access_token}",
        }

    @property
    def basic_auth_headers(self: Self) -> dict[str, str]:
        """The headers for the IGDB API request."""
        return self._basic_auth_headers

    def get_igdb_access_token(self: Self) -> str:
        """Get the IGDB access token."""
        try:
            response = requests.post(self.IGDB_AUTHENTICATION_URL, timeout=10)
            response.raise_for_status()
            return IGDBAuthenticationResponse(**response.json()).access_token
        except requests.HTTPError as e:
            error_message = f"Unable to get the access_token for IGDB. Error: {e}"
            raise IGDBInteractionError(error_message) from e

    def _cast_response(self: Self, endpoint: IGDBEndpoints, response_json: list[dict[str, Any]]) -> IGDB_API_RESPONSE:
        """Cast the response to the correct type for the endpoint."""
        response_map = {
            IGDBEndpoints.PLATFORMS.value: IGDBPlatformResponse,
            IGDBEndpoints.GENRES.value: IGDBGenreResponse,
            IGDBEndpoints.COMPANIES.value: IGDBCompanyResponse,
            IGDBEndpoints.GAMES.value: IGDBGameResponse,
        }

        response_type = response_map.get(endpoint.value)
        if not response_type:
            error_message = f"Unknown endpoint: {endpoint.value}."
            raise IGDBInteractionError(error_message)

        return [response_type(**response) for response in response_json]

    def api_request(self: Self, endpoint: IGDBEndpoints, query: str) -> IGDB_API_RESPONSE:
        """Run request to the IGDB API.

        Args:
            endpoint (IGDBEndpoints): The name of the endpoint.
            query (str): The query for the endpoint.
        """
        if not query:
            error_message = "No query provided."
            raise IGDBInteractionError(error_message)
        try:
            response = requests.post(
                f"{self.IGDB_BASE_URL}{endpoint.value}",
                data=query,
                headers=self.basic_auth_headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            error_message = f"Unable to get the {endpoint.value}. Error: {e}"
            raise IGDBInteractionError(error_message) from e

        return self._cast_response(endpoint, response.json())

    def get_all_objects(self: Self, endpoint: IGDBEndpoints, query: str) -> IGDB_API_RESPONSE:
        """Get all objects from the IGDB database.

        Args:
            endpoint (IGDBEndpoints): The name of the endpoint.
            query (str): The query for the endpoint.
        """
        result: IGDB_API_RESPONSE = []
        offset = 0
        query = f"{query}limit {self.QUERY_ITEM_LIMIT};sort id;"
        while True:
            items_in_response = 0
            for response in self.api_multi_request(endpoint, query, offset):
                response_cast = self._cast_response(endpoint, response.json())
                items_in_response += len(response_cast)
                result.extend(response_cast)
            if items_in_response != self.MAX_REQUESTS_TO_IGDB * self.QUERY_ITEM_LIMIT:
                break
            offset += self.QUERY_ITEM_LIMIT
            # IGDB API has a limit of 4 requests per second
            time.sleep(1)
        return result

    def api_multi_request(self: Self, endpoint: IGDBEndpoints, query: str, offset: int = 0) -> list[requests.Response]:
        """
        Run up to `MAX_REQUESTS_TO_IGDB` request at the same time to the IGDB API.

        Args:
            endpoint (IGDBEndpoints): The name of the endpoint.
            query (str): The query for the endpoint.
            offset (int): The offset to start from.

        Returns:
            list[requests.Response]: A list of the responses.
        """
        if not query:
            error_message = "No query provided."
            raise IGDBInteractionError(error_message)
        session = FuturesSession(max_workers=self.MAX_REQUESTS_TO_IGDB)
        requests = [
            session.post(
                url=f"{self.IGDB_BASE_URL}{endpoint.value}",
                data=f"{query}offset {new_offset};sort id;",
                headers=self.basic_auth_headers,
                timeout=10,
            )
            for new_offset in range(
                offset,
                offset + (self.MAX_REQUESTS_TO_IGDB * self.QUERY_ITEM_LIMIT),
                self.QUERY_ITEM_LIMIT,
            )
        ]
        return [req.result() for req in requests]


if __name__ == "__main__":
    wrapper = IGDBWrapper()
