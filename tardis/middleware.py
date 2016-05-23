from datetime import datetime, timedelta

from celery.task import task
from django.dispatch import receiver
from django.test import override_settings
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from tardis.signals import travel_started, travel_step_completed


class Tardis(object):

    def __init__(self, destination=datetime.now()):
        self.freezer = freeze_time(destination)
        self.callbacks = []

    def is_in_use(self):
        return isinstance(datetime.now(), FakeDatetime)

    def start(self):
        self.freezer.start()

    def stop(self):
        self.freezer.stop()

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def send_travel_step_completed_signal(self):
        travel_step_completed.send(self)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def run_callbacks(self):
        for callback in self.callbacks:
            callback()

    def travel(self, destination, step_size):
        while datetime.now() < destination:
            next_stop = datetime.now() + timedelta(minutes=step_size)
            if next_stop > destination:
                next_stop = destination
            self.freezer.stop()
            self.freezer = freeze_time(next_stop)
            self.freezer.start()
            self.send_travel_step_completed_signal()
        return datetime.now() >= destination


tardis = Tardis()


@task(name='testprint')
def print_time():
    print(datetime.now())


@receiver(travel_step_completed)
def handle_travel_step_completed(sender, **kwargs):
    print_time.delay()


@receiver(travel_started)
def handle_travel_started(sender, **kwargs):
    if tardis.travel(sender.destination_date, sender.step_size):
        sender.completed = True
        sender.save()


class TardisMiddleware(object):

    def process_request(self, request):
        tardis.start()

    def process_response(self, request, response):
        tardis.stop()
        return response

"""
Rough outline of how this should work:

1) User requests a new "trip" which will take the time to a set destination
2) Tardis checks to make sure that no trips are in progress
3) Tardis raises an error if a trip is in progress
4) Tardis creates a new trip if none are in progress
5) Tardis returns "ok" to the user and begins the trip
6) Tardis advances time based on the requested step size
7) As each step is made, Tardis sends a travel_step_completed signal
8) Tardis forces celery tasks to run immediately
9) When the trip completes, Tardis marks the trip completed
10) The user is somehow notified that this is complete
"""
