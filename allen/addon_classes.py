from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, order=True)
class AddonVideo:
    unique_code: str
    '''The unique code for the addon video'''

    module_no: str
    '''The module of the addon video'''

    @classmethod
    def from_json(cls, json_obj: dict, client):
        """
        Deserialize the video json dict to a AddonVideo object.

        :param json_obj: The json dictionary to deserialize.
        :param client: The allen client.
        :meta private:
        """
        unique_code = json_obj.get('UniqueCode')
        module_no = json_obj.get('ModuleNo')
        cls.client = client

        return AddonVideo(unique_code, module_no)

    def get_link(self) -> str:
        """
        Retrieve the link of the addon video.

        :return: The link of the video.
        """
        json = self.client.fetch_json('discussion/student/player', post_data={'UniqueCode': self.unique_code})
        return json['ClassURL']


@dataclass(frozen=True, order=True)
class AddonChapter:
    chapter_name: str
    '''The name of the chapter of the addon chapter'''

    videos: List[AddonVideo]
    '''The list of videos present in the addon chapter'''

    @classmethod
    def from_json(cls, json_obj: dict, client):
        """
        Deserialize the addon chapter json dict to a AddonChapter object.

        :param json_obj: The json dictionary to deserialize.
        :param client: The allen client.
        :meta private:
        """
        chapter_name = json_obj['ChapterName']
        videos = [AddonVideo.from_json(video, client) for video in json_obj['listClass']]

        return AddonChapter(chapter_name, videos)


@dataclass(frozen=True, order=True)
class AddonClass:
    subject_name: str
    '''The name of the subject of the addon class'''

    chapters: List[AddonChapter]
    '''The list of chapters present in the addon class'''

    @classmethod
    def from_json(cls, json_obj: dict, client):
        """
        Deserialize the addon class dict to a AddonClass object.

        :param json_obj: The json dictionary to deserialize.
        :param client: The allen client.
        :meta private:
        """
        subject_name = json_obj['SubjectName']
        chapters = [AddonChapter.from_json(chapter, client) for chapter in json_obj['listChapter']]

        return AddonClass(subject_name, chapters)
