from django.test import TestCase
from django.db import IntegrityError
from maypi.models import DoorCode
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class DoorCodeTestCase(TestCase):
	def test_door_codes_are_unique(self):
		"""DoorCodes should have a unique numeric value"""
		user, created = User.objects.get_or_create(username='tester')
		doorcode, created = DoorCode.objects.get_or_create(code='123456')
		with self.assertRaises(IntegrityError):
			DoorCode.objects.create(code="123456", user=user)

		# self.assertEqual(lion.speak(), 'The lion says "roar"')
		# self.assertEqual(cat.speak(), 'The cat says "meow"')

	def test_door_codes_created_by_different_users_are_unique(self):
		"""DoorCodes should have a unique numeric value regardless of user"""
		user1, created = User.objects.get_or_create(username='tester')
		user2, created = User.objects.get_or_create(username='tester2')
		doorcode, created = DoorCode.objects.get_or_create(code='123456', user=user1)
		with self.assertRaises(IntegrityError):
			DoorCode.objects.create(code="123456", user=user2)

	def test_expired_codes(self):
		"""Expired DoorCodes should be valid or expired"""
		user1, created = User.objects.get_or_create(username='tester')
		doorcode, created = DoorCode.objects.get_or_create(code='123456', user=user1)
		# set the start time to two days ago
		doorcode.start = timezone.localtime(timezone.now()) - datetime.timedelta(days=2)
		# set the end time to one day ago
		doorcode.end = timezone.localtime(timezone.now()) - datetime.timedelta(days=1)
		self.assertTrue(doorcode.is_expired())
		self.assertFalse(doorcode.is_valid())
		

		doorcode.start = timezone.localtime(timezone.now()) - datetime.timedelta(days=2)
		# set the end time to one day from now
		doorcode.end = timezone.localtime(timezone.now()) + datetime.timedelta(days=1)

		self.assertTrue(doorcode.is_valid())
		self.assertFalse(doorcode.is_expired())

