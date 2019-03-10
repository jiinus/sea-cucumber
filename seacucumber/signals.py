from django.dispatch import Signal, receiver

message_sent = Signal(providing_args=['old_message_id', 'new_message_id'])
message_sending_failed = Signal(providing_args=['old_message_id', 'error_code', 'reason'])