from django.dispatch import Signal

destination_changed = Signal(providing_args=['new_time'])
travel_started = Signal()
travel_step_completed = Signal()
travel_completed = Signal()
