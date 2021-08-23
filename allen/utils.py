import requests
from json import JSONDecodeError
from allen.exceptions import AllenInvalidResponse, AllenInvalidUsernamePassword
from typing import Union

__all__ = ['fetch_jwt_from_otp', 'validate_response', 'require_otp']


def validate_response(response: requests.Response):
    """
    Checks if a response is valid or not based on the checks entered in checklist.

    :param response: The response to validate.
    :meta private:
    """
    checks = ['StudentID', 'UserID']

    try:
        json = response.json()
    except (TypeError, JSONDecodeError):
        raise AllenInvalidResponse(response)

    if 'data' not in json:
        raise AllenInvalidResponse(response)

    json = json['data']
    for check in checks:
        if check not in json:
            raise AllenInvalidResponse(response)

        if json[check] == 0:
            raise AllenInvalidUsernamePassword()


def require_otp(response: requests.Response) -> Union[int, bool]:
    """
    Checks if an OTP is required to retrieve the JWT token.

    :param response: The response to check.
    :return: False if OTP is not required, else the actual otp is returned.
    :meta private:
    """
    json = response.json()
    checks = ['error', 'data']

    for check in checks:
        if check not in json:
            raise AllenInvalidResponse(response)

    error = str(json['error'])
    json = json['data']
    if 'OTP' not in json:
        raise AllenInvalidResponse(response)

    otp = json['OTP']
    if otp is not None and error == 'True':
        return otp
    else:
        return False


def fetch_jwt_from_otp(username: str, password: str, device_id: int, student_id: int):
    """
    Fetch the JWT token based on the OTP generated.

    :param username: The form number used to log into Allen's website.
    :param password: The password used to log into Allen's website.
    :param device_id: A random generated id unique to the device.
    :param student_id: The id of the student in Allen's database.
    :return: The JWT token based on the username and password.
    :meta private:
    """
    response = requests.post('https://ddcapi.allenbpms.in/oauth2/verifyotp', json={
        'DeviceType': 'Web',
        'Devicetoken': device_id,
        'Password': password,
        'UserName': username,
        'g-recaptcha-response': 'otp',
        'StudentID': student_id
    })
    json = response.json()

    if 'data' not in json:
        raise AllenInvalidResponse(response)

    json = json['data']
    if 'jwt' not in json:
        raise AllenInvalidResponse(response)

    return json['jwt']
