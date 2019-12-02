from django.db import models
import datetime

class Bus(models.Model):
	bus_code =  models.CharField('Bus Code', max_length=120, primary_key=True)
	trip_id = models.CharField('Trip Id', max_length=120)
	koridor = models.CharField('Koridor', max_length=120)
	timestamp_epoch = models.CharField('Timestamp Epoch', max_length=120)

	@classmethod
	def create(cls, code, trip, koridor, timestamp_epoch):
		bus = cls(bus_code = code, trip_id = trip, koridor = koridor, timestamp_epoch = timestamp_epoch)
		return bus

class GpsPing(models.Model):
	bus_code =  models.CharField('Bus Code', max_length=120)
	longitude = models.CharField('Longitude', max_length=120)
	latitude = models.CharField('Latitude', max_length=120)
	gps_timestamp = models.DateTimeField()

	@classmethod
	def create(cls, code, latitude,longitude, timestamp):
		ping = cls(bus_code = code, latitude = latitude, longitude = longitude, gps_timestamp = timestamp)
		return ping