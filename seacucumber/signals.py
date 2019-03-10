from django.dispatch import Signal, receiver

message_sending = Signal(providing_args=['message_id', 'message'])
message_sent = Signal(providing_args=['old_message_id', 'new_message_id'])
message_sending_failed = Signal(providing_args=['old_message_id', 'error_code', 'reason'])