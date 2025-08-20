from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Student

@receiver(post_save, sender=Student)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and instance.full_name and instance.registration_number:
        nomes = instance.full_name.strip().split()
        if len(nomes) >= 2:
            username = (nomes[0] + nomes[-1]).lower()
        else:
            username = nomes[0].lower()
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                password=instance.registration_number,
                first_name=nomes[0],
                last_name=nomes[-1] if len(nomes) > 1 else '',
                email=instance.email
            )
            # Opcional: associar o user ao aluno, se desejar
            # instance.user = user
            # instance.save()
