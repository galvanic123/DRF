import re

from rest_framework.exceptions import ValidationError


class YouTubeValidator:

    def __init__(self, field):
        self.field = field

        def __cal__(self, value):
            if value is not None:
                tmp_field = dict(value).get(self.field)
                if tmp_field:
                    youtube_pattern = r"^(https?://)?(www\.)?youtube\.com/.+"
                    if not re.match(youtube_pattern, tmp_field):
                        raise ValidationError("Доступны только ссылки на youtube.com")
