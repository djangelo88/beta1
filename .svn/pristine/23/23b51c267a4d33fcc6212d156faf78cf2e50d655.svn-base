from django.dispatch.dispatcher import Signal

trial_memeber_email = Signal(providing_args=['subscription', 'stripe_task'])
trial_memeber_change_status = Signal(providing_args=['subscription', 'stripe_task'])
trial_memeber = Signal(providing_args=['subscription', 'stripe_task'])

canceled_subscription_email = Signal(providing_args=['subscription', 'stripe_task'])
canceled_subscription_change_status = Signal(providing_args=['subscription', 'stripe_task'])
canceled_subscription = Signal(providing_args=['subscription', 'stripe_task'])

trial_will_end = Signal(providing_args=['subscription','trial_end', 'stripe_task'])

payment_failed = Signal(providing_args=['stripe_invoice','last_attempt' ,'stripe_task'])

charge_failed = Signal(providing_args=['stripe_charge','stripe_json_error','stripe_task'])

become_past_due = Signal(providing_args=['subscription', 'stripe_task'])

past_due_active = Signal(providing_args=['subscription', 'stripe_task'])

proposal_accepted = Signal(providing_args=['proposal'])

changing_event_data = Signal(providing_args=['proposal','invoice'])
changing_item_data = Signal(providing_args=['proposal'])

# invoice_has_been_send = Signal(providing_args=['invoice'])