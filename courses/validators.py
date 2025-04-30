from rest_framework import serializers


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

        def __call__(self, value):
            val = dict(value).get(self.field)
            if val and "youtube.com" not in val:
                raise serializers.ValidationError("Некорректная ссылка, ссылка должна содержать адрес youtube.com")
