import boto3
from botocore.client import ClientError
from mypy_boto3_sns.client import SNSClient

CLIENT_NAME = "SMOK"


class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, title):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource: SNSClient = boto3.client('sns')
        self.title = title

    def publish_text_message(self, phone_number, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.

        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        try:
            response = self.sns_resource.publish(
                PhoneNumber=phone_number, Message=message,
                    MessageAttributes={
                        'AWS.SNS.SMS.SenderID': {
                            'DataType': 'String',
                            'StringValue': self.title,
                        }
                    })
            message_id = response['MessageId']
        except ClientError:
            raise
        else:
            return message_id


if __name__ == "__main__":
    wraper = SnsWrapper(CLIENT_NAME)
    phone_number = "+48xxxyyyxxx"
    message = "This is test message"
    wraper.publish_text_message(phone_number, message)
