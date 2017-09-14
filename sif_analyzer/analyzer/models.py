from django.db import models

# Create your models here.
class Event(models.Model):
	start_date		= models.DateField()
	end_date		= models.DateField()
	name			= models.CharField(max_length=40)
	event_link		= models.CharField(max_length=100)
	point_sr 		= models.CharField(max_length=8)	# foreignkey?
	point_sr_link 	= models.CharField(max_length=100)
	rank_sr 		= models.CharField(max_length=8)	# foreignkey?
	rank_sr_link 	= models.CharField(max_length=100)
	point_cutoff_1 	= models.PositiveIntegerField()
	rank_cutoff_1 	= models.PositiveIntegerField()
	point_cutoff_2 	= models.PositiveIntegerField()
	rank_cutoff_2 	= models.PositiveIntegerField()
	point_cutoff_3	= models.PositiveIntegerField()
	rank_cutoff_3	= models.PositiveIntegerField()
	note = models.TextField()

	def __str__(self):
		return '{}: {} - {}\t{}\t{}\t{}'.format(self.__class__.__name__,
			self.start_date,
			self.end_date,
			self.name,
			self.point_sr,
			self.rank_sr,
			)

	def __lt__(self, other):
		return self.start_date < other.start_date