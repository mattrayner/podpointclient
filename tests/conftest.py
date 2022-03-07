"""Global fixtures for podpointclient."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch

import pytest

# import podpointclient.endpoints

# # This fixture, when used, will result in the base API being changed to HTTP not HTTPS
# @pytest.fixture(autouse=True)
# def set_to_http(monkeypatch):
#     """Patch HTTPS api to HTTP."""
#     monkeypatch.setattr(podpointclient.endpoints, 'API_BASE_URL', 'http://api.pod-point.com/v4')


# # In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# # for exception handling.
# @pytest.fixture(name="error_on_get_data")
# def error_get_data_fixture():
#     """Simulate error when retrieving data from API."""
#     with patch(
#         "custom_components.pod_point.PodPointApiClient.async_get_pods",
#         side_effect=Exception,
#     ):
#         yield
