from rest_framework import serializers


class XmlDataSerializer(serializers.Serializer):
    xml_data = serializers.CharField()
