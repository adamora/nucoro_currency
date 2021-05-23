from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from nucoro_currency.currencies.models import Provider


@receiver(pre_save, sender=Provider)
def process_unique_provider(sender, instance, **kwargs):
    initial_queryset = sender.objects.filter(default=True)
    if instance.default:
        if instance.id:
            initial_queryset = initial_queryset.exclude(id=instance.id)
        initial_queryset.update(default=False)


@receiver(post_delete, sender=Provider)
def process_unique_provider_on_delete(sender, instance, using, *args, **kwargs):
    if instance.default:
        default_instance = sender.objects.get_default()
        default_instance.default = True
        default_instance.save()
