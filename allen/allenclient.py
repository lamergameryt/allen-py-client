import random
import requests
from typing import Union
from allen.utils import fetch_jwt_from_otp, require_otp, validate_response
from allen.video import RecordedVideo, LiveClassDay
from allen.exceptions import AllenInvalidUsernamePassword, AllenResponseUnavailable, AllenInvalidResponse
from allen.exam import Examination
from allen.addon_classes import AddonClass
from allen.test_record import TestRecord
from typing import List

__all__ = ['AllenClient']


class AllenClient:
    """
    Base class for access to Allen's API.

    .. note::

        You do not have the enter all three init parameters.
        Either authenticate using username and password, or using JWT.
    """

    def __init__(self, username: Union[str, int] = None, password: str = None, jwt: str = None):
        """
        Initialize connection to Allen's API.

        :param username: The form number used to log into Allen's website.
        :param password: The password used to log into Allen's website.
        :param jwt: The JWT Token
        """

        # Checks to ensure code consistency.
        if username is None:
            username = ""
        if password is None:
            password = ""
        if username is int:
            username = str(username)

        if jwt is None:
            if username == "" or password == "":
                raise AllenInvalidUsernamePassword()

            self._username = username
            self._password = password
            self.__setup()
        else:
            self._jwt = jwt

        self.api_url = 'ddcapi.allenbpms.in/api'

    def get_recorded_videos(self) -> List[RecordedVideo]:
        """
        Fetch the list of recorded videos available to view.

        :return: A list of the class:`video.RecordedVideo` class
        """
        video_list_json = self.fetch_json('dc/student/recordinglist')
        video_list = list()

        for video_day in video_list_json:
            date = video_day['ClassDate']
            video_json_list = video_day['listClass']
            for video_json in video_json_list:
                video_list.append(RecordedVideo.from_json(video_json, date, self))

        return video_list

    def get_live_classes(self) -> List[LiveClassDay]:
        """
        Fetch the list of upcoming live classes.

        :return: A list of the class:`video.LiveClassDay` class
        """
        live_class_day_list_json = self.fetch_json('dc/student/livelist')
        return [LiveClassDay.from_json(live_class_day) for live_class_day in live_class_day_list_json]

    def get_test_records(self) -> List[TestRecord]:
        """
        Fetch the list of tests you've attempted.

        :return: A list of the class:`test_record.TestRecord` class
        """
        test_list = self.fetch_json('studenttestrecord').get('testList')
        return [TestRecord.from_json(test, self) for test in test_list]

    def get_exam_calendar(self) -> List[Examination]:
        """
        Fetch the list of exams on the exam calendar.

        :return: A list of the class:`exam.Examination` class
        """
        json = self.fetch_json('studentexamcalendar')
        return [Examination.from_json(exam) for exam in json]

    def get_addon_classes(self) -> List[AddonClass]:
        """
        Fetch the list of addon classes available.

        :return: A list of the class:`addon_classes.AddonClass` class
        """
        json = self.fetch_json('discussion/student/list')
        return [AddonClass.from_json(addon_class, self) for addon_class in json]

    def fetch_json(self, url_path: str, http_method: str = 'POST', secure: bool = True, headers: dict = None,
                   query_params: dict = None, post_data: dict = None) -> dict:
        """
        Fetch some JSON from Allen's API.

        :param url_path: The url to fetch the JSON from.
        :param http_method: The http method that will be used with the request.
        :param secure: Specify whether to use HTTPS (True) or HTTP (False).
        :param headers: The headers to pass through the request.
        :param query_params: The url parameters to include with the request.
        :param post_data: The post data to send with the request.

        :return: A dict containing the parsed JSON response
        :meta private:
        """
        # Specify values of method parameters explicitly
        if headers is None:
            headers = {}
        if query_params is None:
            query_params = {}
        if post_data is None:
            post_data = {}
        if secure is None:
            secure = False

        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = f'Bearer {self._jwt}'

        # Removes a leading slash if included in the url_path.
        if url_path[0] == '/':
            url_path = url_path[1:]
        url = ('https://' if secure else 'http://') + self.api_url + '/' + url_path

        # Perform the HTTP request using the provided parameters.
        response = requests.request(http_method, url, params=query_params, headers=headers, json=post_data)

        if response.status_code != 200:
            raise AllenResponseUnavailable(url, response)

        json = response.json()
        if 'data' not in json or json['data'] is None:
            raise AllenInvalidResponse(response)

        return json['data']

    def __setup(self):
        """
        Generate a JWT token from the provided username and password.

        :meta private:
        """
        username = self._username
        password = self._password
        device_id = random.randint(100000000000, 999999999999)

        response = requests.post('https://ddcapi.allenbpms.in/oauth2/astoken', json={
            'DeviceType': 'Web',
            'Devicetoken': device_id,
            'Password': password,
            'UserName': username
        })

        validate_response(response)
        otp = require_otp(response)
        json = response.json()

        if not otp:
            self._jwt = json['data']['jwt']
        else:
            student_id = json['data']['StudentID']
            self._jwt = fetch_jwt_from_otp(username, password, device_id, student_id)
