"""Tests for my_game_list app urls."""

import importlib

from django.test import override_settings

import my_game_list.my_game_list.urls as my_game_list_urls


def test_rosetta_in_urls() -> None:
    """Test if rosetta urls are added correctly after adding rosetta to the INSTALLED_APPS."""
    with override_settings(INSTALLED_APPS=["test", "rosetta"]):
        importlib.reload(my_game_list_urls)

        assert any("rosetta" in str(urlpattern) for urlpattern in my_game_list_urls.urlpatterns)


def test_rosetta_not_in_urls() -> None:
    """Test if rosetta urls are not present in the application urls."""
    with override_settings(INSTALLED_APPS=["test"]):
        importlib.reload(my_game_list_urls)

        assert all("rosetta" not in str(urlpattern) for urlpattern in my_game_list_urls.urlpatterns)
