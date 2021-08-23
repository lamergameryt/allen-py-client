from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True, order=True)
class Examination:
    marking_scheme: str
    '''The marking scheme of the examination, for example ``JEE MAIN. PATTERN``'''

    syllabus: str
    '''The syllabus of the examination'''

    test_centre: str
    '''The centre in which the examination will be held'''

    test_day: str
    '''The day the examination will be held, for example ``Wednesday``'''

    test_name: str
    '''The name of the examination'''

    time_detail: str
    '''The time the examination was or will be held'''

    _test_date: str
    '''The date the examination was or will be held'''

    @classmethod
    def from_json(cls, json_obj: dict):
        """
        Deserialize the exam json dict to an Examination object.

        :param json_obj: The json dictionary to deserialize.
        :meta private:
        """
        marking_scheme = json_obj.get('MarkingScheme')
        syllabus = json_obj.get('Syllabus')
        test_centre = json_obj.get('TestCentre')
        test_day = json_obj.get('TestDay')
        test_name = json_obj.get('TestName')
        time_detail = json_obj.get('TimeDetail')
        test_date = json_obj.get('TestDate')

        return Examination(marking_scheme, syllabus, test_centre, test_day, test_name, time_detail, test_date)

    def get_test_date(self) -> Optional[str]:
        """
        Returns the date of the test in ``Thursday : 01 January 1970`` format.

        :return: The date if a valid date is present, else None.
        """
        try:
            return datetime.fromisoformat(self._test_date).strftime('%A : %d %B %Y')
        except ValueError:
            return None
