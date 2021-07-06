from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, order=True)
class RecordedVideo:
    unique_code: str
    '''The unique code for the recorded video'''

    subject_name: str
    '''The name of the subject taught in the recorded video'''

    _date: str
    '''The date the video was recorded'''

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
        json = self.client.fetch_json('dc/student/recordingplayer', post_data={'UniqueCode': self.unique_code})
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


@dataclass(frozen=True, order=True)
class LiveClass:
    class_start_time: str
    '''The time the class starts in ``12:00PM`` format'''

    class_end_time: str
    '''The time the class ends in ``12:00PM`` format'''

    unique_code: str
    '''The unique code for the live video'''

    subject_name: str
    '''The name of the subject which will be taught in the live video'''

    remaining_time: int
    '''The time remaining for the class to start in seconds'''

    @classmethod
    def from_json(cls, json_obj: dict):
        """
        Deserialize the live class json dict to a LiveClass object.

        :param json_obj: The json dictionary to deserialize.
        :meta private:
        """
        class_start_time = json_obj.get('ClassStart')
        class_end_time = json_obj.get('ClassEnd')
        unique_code = json_obj.get('UniqueCode')
        subject_name = json_obj.get('SubjectName')
        remaining_time = json_obj.get('RemainingTime')

        return LiveClass(class_start_time, class_end_time, unique_code, subject_name, remaining_time)


@dataclass(frozen=True, order=True)
class LiveClassDay:
    class_day: str
    '''The day of the live class, for example ``Wednesday``'''

    _date: str
    '''The date of the live class'''

    live_classes: list[LiveClass]
    '''The list of live classes on this day'''

    @classmethod
    def from_json(cls, json_obj: dict):
        """
        Deserialize the live class day json dict to a LiveClassDay object.

        :param json_obj: The json dictionary to deserialize.
        :meta private:
        """
        class_day = json_obj.get('ClassDay')
        _date = json_obj.get('ClassDate')
        live_classes = [LiveClass.from_json(live_class) for live_class in json_obj.get('listClass')]

        return LiveClassDay(class_day, _date, live_classes)

    def get_live_class_date(self) -> str:
        """
        Returns the date of the live classes in ``Thursday : 01 January 1970`` format.

        :return: The date if a valid date is present, else None.
        """
        try:
            return datetime.fromisoformat(self._date).strftime('%A : %d %B %Y')
        except ValueError:
            return None
