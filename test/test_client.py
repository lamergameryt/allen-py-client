import unittest
from allen import AllenClient, AllenInvalidUsernamePassword
import os
import re


class VideosTestCase(unittest.TestCase):
    """
    Tests for the AllenClient module. The tests are performed only by one account.
    """

    @classmethod
    def setUpClass(cls) -> None:
        env = os.environ
        if 'jwt' in env:
            cls._client = AllenClient(jwt=env['jwt'])
        elif 'username' in env and 'password' in env:
            cls._client = AllenClient(username=env['username'], password=env['password'])
        else:
            raise AllenInvalidUsernamePassword()
        cls._regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def test_recorded_video_links(self):
        videos = self._client.get_recorded_videos()
        for video in videos:
            link = video.get_link()
            self.assertTrue(re.match(self._regex, link) is not None, msg='The url received from the server was '
                                                                         'invalid.')

    def test_live_class(self):
        video_days = self._client.get_live_classes()
        for video_day in video_days:
            for live_class in video_day.live_classes:
                self.assertGreaterEqual(live_class.remaining_time, 0, msg='The live class time remaining '
                                                                          'cannot be less than zero.')

    def test_test_records(self):
        test_records = self._client.get_test_records()
        for test_record in test_records:
            self.assertGreaterEqual(test_record.percentage, 0.0, msg='The percentage of marks received cannot be less'
                                                                     'than zero.')
