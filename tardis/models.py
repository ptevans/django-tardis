from __future__ import unicode_literals

from django.db import models
from tardis.signals import travel_started


class Trip(models.Model):

    start_date = models.DateTimeField(auto_now_add=True)
    destination_date = models.DateTimeField()
    step_size = models.IntegerField(
        help_text='Step size in minutes. The Tardis will take us to our '
                  'destination stopping at intervals to execute any callbacks'
                  'that are defined for our trips.')
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    @classmethod
    def request_trip(cls, destination_date, step_size):
        """Creates and returns a new Trip if there is not one in progress."""
        if not cls.objects.filter(started=True, completed=False).exists():
            return cls.objects.create(destination_date=destination_date,
                                      step_size=step_size)

    def start(self):
        self.started = True
        self.save()
        travel_started.send(self)

    def __unicode__(self):
        return '{} to {}'.format(self.start_date, self.destination_date)

    __str__ = __unicode__
