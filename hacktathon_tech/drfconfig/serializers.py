from rest_framework import serializers
import json
import six
import uuid
import imghdr
from django.core.files.base import ContentFile



class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        json_data = {}
        try:
            if type(value) == type(list()):
                json_data = value
            else:
                json_data = json.loads(value)
        except ValueError as e:
            raise e
        finally:
            return json_data if json_data else []

    def to_internal_value(self, data):
        return json.dumps(data)
