from rest_framework import serializers
from re_api.models import Messages
from re_api.services import KafkaSender
from decouple import config

sender = KafkaSender(bootstrap_servers=config('BOOTSTRAP_SERVERS_SENDER'),
                     output_topic=config('KAFKA_TOPIC'))


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Messages
        fields = '__all__'

    def create(self, validated_data):
        message = Messages.objects.create(
            user_id=validated_data.get("user_id"),
            text=validated_data.get("text"),
            status="review"
        )

        message.save()

        data = {
            'message_id': message.id,
            'text': message.text,
        }

        sender.send_message(data)
        return message


class MessageStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    success = serializers.CharField(source='status')

    def create(self, validated_data):
        message = Messages.objects.get(id = validated_data.get('id'))
        if validated_data.get('status') == 'True':
            message.status = 'correct'
        else:
            message.status = 'blocked'
        message.save()
        return message

    class Meta:
        model = Messages
        fields = ('id', 'success',)