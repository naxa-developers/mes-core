from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Activity, ClusterAG, ClusterA, Config


@receiver(post_save, sender=Activity)
def save_activity(sender, **Kwargs):
	config = Config.objects.first()
	config.save()



	