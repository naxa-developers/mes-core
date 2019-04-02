from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Activity, ClusterAG, ClusterA, Config


@receiver(post_save, sender=Activity)
@receiver(post_save, sender=ClusterAG)
@receiver(post_save, sender=ClusterA)
def save_activity(sender, **Kwargs):
	config = Config.objects.first()
	config.save()




	