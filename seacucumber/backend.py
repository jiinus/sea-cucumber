"""
This module contains the SESBackend class, which is what you'll want to set in
your settings.py::

    EMAIL_BACKEND = 'seacucumber.backend.SESBackend'
"""

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from seacucumber.tasks import SendEmailTask
from seacucumber.signals import message_sending

class SESBackend(BaseEmailBackend):
    """
    A Django Email backend that uses Amazon's Simple Email Service.
    """

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of
        email messages sent.

        :param EmailMessage email_messages: A list of Django's EmailMessage
            object instances.
        :rtype: int
        :returns: The number of EmailMessage objects that were successfully
            queued up. Note that these are not in a state where we can
            guarantee delivery just yet.
        """

        queue = getattr(settings, 'CUCUMBER_ROUTE_QUEUE', '')
        num_sent = 0
        for message in email_messages:

            message_id = message.extra_headers.get('Message-ID', None)
            message_sending.send(sender=self.__class__, message_id=message_id, message=message)

            # Hand this off to a celery task.
            SendEmailTask.apply_async(args=[
                    message.from_email,
                    message.recipients(),
                    message.message().as_string().decode('utf8'),
                    message_id],
                queue=queue,
            )
            num_sent += 1
        return num_sent
