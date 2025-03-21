#
# BASE_URL = "https://platform.test.pinacagroup.internal"
# LOGIN_ENDPOINT = "/api/auth/login"
#
# USERNAME = "Testadmin"
# PASSWORD = "Test@1234"
#
#
# @allure.feature("Authentication")
# @allure.story("Login Test")
# @allure.severity(allure.severity_level.CRITICAL)
# @pytest.mark.login
# def test_login():
#     """Test login functionality and validate response"""
#     url = f"{BASE_URL}{LOGIN_ENDPOINT}"
#     payload = {"username": USERNAME, "password": PASSWORD}
#     headers = {"Content-Type": "application/json"}
#
#     with allure.step("Sending login request"):
#         response = requests.post(url, json=payload, headers=headers, verify=False)
#
#     with allure.step("Validating response"):
#         allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
#         assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
#
#     print(f"Status Code: {response.status_code}")
#     print("Response:", response.text)

import requests
import pytest
import allure

BASE_URL = "https://platform.test.pinacagroup.internal"
LOGIN_ENDPOINT = "/api/auth/login"
UPDATE_USER_ENDPOINT = "/users/update"

USERNAME = "Bhuvanes_Admin"
PASSWORD = "Test@123"

# Global variable to store access token
ACCESS_TOKEN = None



# Example user update payload
UPDATE_PAYLOAD = {
  "id": 778,
  "firstName": "Bhuvanes",
  "lastName": "Muniyappan",
  "roleId": 3,
  "organizationId": 1,
  "timeoutValue": 10,
  "timeoutUnit": "minutes"
}

@allure.feature("Authentication")
@allure.story("Login Test")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.login
def test_login():
    """Test login functionality and validate response"""
    global ACCESS_TOKEN  # Declare global to store the token

    url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}

    with allure.step("Sending login request"):
        response = requests.post(url, json=payload, headers=headers, verify=False)

    with allure.step("Validating response"):
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    # Extract access token from response
    response_data = response.json()
    ACCESS_TOKEN = response_data.get("accessToken")  # Store token globally

    print(f"Access Token: {ACCESS_TOKEN}")

    assert ACCESS_TOKEN is not None, "Access token was not returned in response"


@allure.feature("User Management")
@allure.story("Update User")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.update_user
def test_update_user():
    """Test updating user details"""

    global ACCESS_TOKEN  # Ensure the access token is available

    assert ACCESS_TOKEN is not None, "No access token available, login test must run first."

    url = f"{BASE_URL}{UPDATE_USER_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    with allure.step("Sending update user request"):
        response = requests.put(url, json=UPDATE_PAYLOAD, headers=headers, verify=False)

    with allure.step("Validating response"):
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    print(f"Update Response: {response.text}")
