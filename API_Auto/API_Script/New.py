import requests
import pytest
import allure

BASE_URL = "https://platform.test.pinacagroup.internal"
LOGIN_ENDPOINT = "/api/auth/login"
UPDATE_USER_ENDPOINT = "/api/users/update"


USERNAME = "Bhuvanes_Admin"
PASSWORD = "Test@123"

USER_ID = 123

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

@pytest.fixture(scope="session")
def get_access_token():
    """Fixture to get access token before running test cases"""
    url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    payload = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    response_data = response.json()
    access_token = response_data.get("accessToken")
    assert access_token is not None, "Access token was not returned in response"

    return access_token  # Return token for tests

@allure.feature("User Management")
@allure.story("Update User")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.update_user
def test_update_user(get_access_token):
    """Test updating user details"""

    url = f"{BASE_URL}{UPDATE_USER_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {get_access_token}",  # Using the fixture token
        "Content-Type": "application/json"
    }

    with allure.step("Sending update user request"):
        response = requests.put(url, json=UPDATE_PAYLOAD, headers=headers, verify=False)

    with allure.step("Validating response"):
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    print(f"Update Response: {response.text}")
#
#
# import requests
# import allure
# import pytest
#
# BASE_URL = "https://your-api-url.com"  # Update with your actual base URL
# USER_ID = 123  # Replace with a valid user ID
# TOKEN = "your_existing_token"  # Use the same token from the previous test
#
#
# @allure.feature("User Management")
# @allure.story("Mark User as Inactive")
# @allure.severity(allure.severity_level.CRITICAL)
# @pytest.mark.mark_as_inactive
# def test_mark_user_inactive():
#     """Test marking a user as inactive"""
#
#     url = f"{BASE_URL}/users/markAsInactive/{USER_ID}"
#
#     headers = {
#         "Authorization": f"Bearer {TOKEN}",
#         "Content-Type": "application/json"
#     }
#
#     payload = {
#         "inputStatus": "Inactive"
#     }
#
#     with allure.step("Sending mark as inactive request"):
#         response = requests.put(url, json=payload, headers=headers, verify=False)
#
#     with allure.step("Validating response"):
#         allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
#         print("Status Code:", response.status_code)
#         print("Response Text:", response.text)
#         assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
#
