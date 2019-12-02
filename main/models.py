from django.db import models

class Bus(models.Model):
	bus_code =  models.CharField('Bus Code', max_length=120, primary_key=True)
	trip_id = models.CharField('Trip Id', max_length=120)
	koridor = models.CharField('Koridor', max_length=120)
	gps_timestamp = models.DateField('GPS Timestamp')

	@classmethod
	def create(cls, code, trip, koridor, gps):
		bus = cls(bus_code = code, trip_id = trip, koridor = koridor, gps_timestamp = gps)
		return bus
	