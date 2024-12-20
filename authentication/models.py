from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
	CREATOR = 'CREATOR'
	SUBSCRIBER = 'SUBSCRIBER'

	ROLE_CHOICES = (
		(CREATOR, 'Createur'),
		(SUBSCRIBER, 'Abonne'),
	)

	profile_photo = models.ImageField(verbose_name='Photo de profil')
	role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Role')

	follows = models.ManyToManyField(
	'self',
	limit_choices_to={'role': CREATOR},	
	symmetrical=False,
	verbose_name='Suit',
	)