from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, order=True)
class RecordedVideo:
    unique_code: str
    '''The unique code for the recorded video'''

    subject_name: str
    '''The name of the subject taught in the recorded video'''

    _date: str

    @classmethod
    def from_json(cls, json_obj: dict, date: str, client):
        """
        Deserialize the video json dict to a RecordedVideo object.

        :param json_obj: The json dictionary to deserialize.
        :param date: The date the lecture was recorded at.
        :param client: The allen client.
        :meta private:
        """
        unique_code = json_obj.get('UniqueCode')
        subject_name = json_obj.get('SubjectName')
        cls.client = client

        return RecordedVideo(unique_code, subject_name, date)

    def get_link(self) -> str:
        """
        Retrieve the link of the recorded video.

        :return: The link of the video.
        """
        json = self.client.fetch_json('dc/student/recordingplayer', post_data={'UniqueCode': self.unique_code})['data']
        return json['ClassURL']

    def get_recording_date(self) -> str:
        """
        Returns the date of the recording in ``Thursday : 01 January 1970`` format.

        :return: The date if a valid date is present, else None.
        """
        try:
            return datetime.fromisoformat(self._date).strftime('%A : %d %B %Y')
        except ValueError:
            return None
