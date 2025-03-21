import pandas as pd
import json
import requests
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

log_path = os.path.join(os.getcwd(), "logs_platform")
if not os.path.exists(log_path):
    os.mkdir(log_path)
else:
    for file in os.listdir(log_path):
        file_path = os.path.join(log_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

filename = 'api_test_logs_' + datetime.now().strftime('%Y-%m-%d') + '.log'
log_file_path = os.path.join(log_path, filename)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

log_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(console_handler)


def global_function(url, payload, method, headers, token):
    print("URL:", url)
    print("Payload:", payload)
    print("Method:", method)

    if "id" in payload:
        payload["id"] = int(payload["id"])

    if isinstance(payload, dict):
        payload = json.dumps(payload)

    if token:
        headers['Authorization'] = f'Bearer {token}'

    response = requests.request(method, url, headers=headers, data=payload)

    try:
        res = response.json()
    except json.JSONDecodeError:
        res = response.text
    print("Response:", res)
    return res


data = [

    {"login": {"url": "https://platform.test.pinacagroup.internal/api/auth/login",
               "headers": {
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'},

               "payload": {"payload1": {"username": "Testadmin", "password": "Test@1234"}
                   ,
                           "payload2": {"username": "TestAdmin", "password": "Abc@1234"}
                           }, "method": ["POST", "GET"]}}]

api_results = []


def global_function(url, payload, method, headers, token, params):
    """Make API requests and return the actual status code dynamically."""
    final_url = None
    if params == None:

        try:
            if token:
                headers["Authorization"] = f"Bearer {token}"

            if method == "POST":
                response = requests.post(url, json=payload, headers=headers, verify=False)
            elif method == "PUT":
                response = requests.put(url, json=payload, headers=headers, verify=False)
            elif method == "GET":
                response = requests.get(url, headers=headers, verify=False)
                print(response)
            else:
                logger.error(f"Invalid method: {method}")
                return None
            return response.status_code, response.json()

        except Exception as e:
            logger.error(f"Request failed: {e}")
            return 500, str(e)
    else:
        final_url = url
        print(params)

        query_string = "?"
        for idx, (key, value) in enumerate(params.items()):

            query_string += f"{key}={str(value)}"
            if idx < len(params) - 1:
                query_string += "&"

        final_url += query_string
        url = final_url

        print(" final jxbcjdbvhjd", final_url)
        try:
            if token:
                headers["Authorization"] = f"Bearer {token}"

            if method == "POST":
                response = requests.post(url, json=payload, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=payload, headers=headers)
            elif method == "GET":
                response = requests.get(url, headers=headers)
                print(response)
            else:
                logger.error(f"Invalid method: {method}")
                return None

            return response.status_code, response.json()

        except Exception as e:
            logger.error(f"Request failed: {e}")
            return 500, str(e)


token = None


def validate_payload(payload):
    """Validates payload fields and converts to correct data types if possible."""
    try:
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")

        if "id" in payload:
            if isinstance(payload["id"], str) and payload["id"].isdigit():
                payload["id"] = int(payload["id"])
            elif not isinstance(payload["id"], int):
                raise ValueError(f"Invalid ID format: {payload['id']}")

        if "roleId" in payload:
            if isinstance(payload["roleId"], str) and payload["roleId"].isdigit():
                payload["roleId"] = int(payload["roleId"])
            elif not isinstance(payload["roleId"], int):
                raise ValueError(f"Invalid roleId format: {payload['roleId']}")

        if "timeoutValue" in payload:
            if isinstance(payload["timeoutValue"], str) and payload["timeoutValue"].isdigit():
                payload["timeoutValue"] = int(payload["timeoutValue"])
            elif not isinstance(payload["timeoutValue"], int):
                raise ValueError(f"Invalid timeoutValue format: {payload['timeoutValue']}")

    except ValueError as e:
        logger.error(f"Payload validation failed: {e}")
        return None
    return payload


for each_endpoint in data:
    for each_url in each_endpoint:
        url = each_endpoint[each_url].get("url")
        headers = each_endpoint[each_url].get("headers", {})
        params = each_endpoint[each_url].get("params", {})
        if params:
            print(params)
            for each_params in params:
                logger.info(f"Processing URL: {url}")

                for each_payload_key, each_payload in each_endpoint[each_url].get("payload", {}).items():
                    validated_payload = validate_payload(each_payload)
                    if validated_payload is None:
                        logger.error(f"Skipping request due to invalid payload: {each_payload_key}")
                        continue

                    for each_method in each_endpoint[each_url].get("method", []):
                        # try:

                        # Make the API request
                        status_code, response_body = global_function(url, validated_payload, each_method, headers,
                                                                     token, params[each_params])
                        logger.info(f"Url Name:{each_url}")
                        logger.info(f"payload name  : {each_payload_key}")
                        logger.info(f"Request Method: {each_method} | URL: {url} | Payload: {validated_payload}")
                        logger.info(f"Actual Status Code: {status_code}")
                        logger.info(f"Response Body: {response_body}")

                        # Save token if logging in
                        if each_url == "login" and "accessToken" in response_body:
                            token = response_body["accessToken"]
                            logger.info("Access Token retrieved successfully.")

                        logger.info("\n-----------------------------------------------------------------")

        else:
            logger.info(f"Processing URL: {url}")

            for each_payload_key, each_payload in each_endpoint[each_url].get("payload", {}).items():
                validated_payload = validate_payload(each_payload)
                if validated_payload is None:
                    logger.error(f"Skipping request due to invalid payload: {each_payload_key}")
                    continue

                for each_url, endpoint_data in each_endpoint.items():
                    for each_method in endpoint_data.get("method", []):
                        try:
                            # Call API function
                            status_code, response_body = global_function(url, validated_payload, each_method, headers,
                                                                         token, None)

                            # Logging request and response details
                            logger.info(f"Url Name: {each_url}")
                            logger.info(f"Payload Name: {each_payload_key}")
                            logger.info(f"Request Method: {each_method} | URL: {url} | Payload: {validated_payload}")
                            logger.info(f"Actual Status Code: {status_code}")
                            logger.info(f"Response Body: {response_body}")

                            # Save token if logging in
                            if each_url == "login" and "accessToken" in response_body:
                                token = response_body["accessToken"]
                                logger.info("Access Token retrieved successfully.")

                            # Append data to list
                            api_results.append({
                                "URL": each_url,
                                "Method": each_method,
                                "Payload": validated_payload,
                                "Status Code": status_code,
                                "Response Body": response_body
                            })

                        except Exception as e:
                            logger.error(f"Error processing {each_url} | Method: {each_method} | Error: {e}")
                            api_results.append({
                                "URL": each_url,
                                "Method": each_method,
                                "Payload": validated_payload,
                                "Status Code": "Error",
                                "Response Body": str(e)
                            })
                    df = pd.DataFrame(api_results)

                    # Save to an ODS file
                    df.to_excel("API_Test_Results.ods", engine="odf", index=False)

                    logger.info("✅ API results saved successfully in 'API_Test_Results.ods'")