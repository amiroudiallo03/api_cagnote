from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.validators import ValidationError

# Create your models here.

# model academicien


class Base(models.Model):
    date_add = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Reason(Base):
    name = models.CharField(max_length=200, verbose_name="nom", unique=True)

    class Meta:
        verbose_name = "Motif"
        verbose_name_plural = "Motifs"

    def __str__(self):
        return self.name


class Academician(Base):
    last_name = models.CharField(max_length=30, verbose_name="nom", blank=True)
    first_name = models.CharField(max_length=40, verbose_name="prenom", blank=True)
    register_number = models.CharField(
        max_length=30, verbose_name="matricule", blank=True
    )
    picture = models.FileField(upload_to="pictures", verbose_name="photos", blank=True)
    reasons = models.ManyToManyField(Reason, verbose_name="motif", through="Payment")
    overall_payment = models.PositiveIntegerField(
        default=0, 
        blank=True,
        null=True, 
        verbose_name='paiement total',
        editable=False
        )

    class Meta:
        verbose_name = "Academicien"
        verbose_name_plural = "Academiciens"
        ordering = ['-overall_payment']

    def __str__(self):
        return self.last_name


class Payment(Base):
    academician = models.ForeignKey(
        Academician, 
        on_delete=models.CASCADE,
        related_name='payments'
        )
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_hour = models.TimeField(auto_now_add=True)

    class Meta:
        verbose_name = "paiement"
        constraints = [
            models.UniqueConstraint(
                fields=["academician", "payment_date", "reason"], name="payment_unique"
            )
        ]

    def __str__(self):
        return f"{self.academician}, {self.reason}, {self.montant}"

def update_academician_overall_payment(instance, created, **kwargs):
    if created:
        academician = instance.academician
        total = sum([p.montant for p in academician.payments.all()])
        academician.overall_payment=total
        academician.save() 
    else:
        academician = instance.academician
        total = sum([p.montant for p in academician.payments.all()])
        academician.overall_payment=total
        academician.save()

def delete_and_update_academician_overall_payment(instance, **kwargs):
    academician = instance.academician
    total = sum([p.montant for p in academician.payments.all()])
    academician.overall_payment=total
    academician.save()


post_save.connect(
    receiver=update_academician_overall_payment,
    sender=Payment
    )

post_delete.connect(
    receiver=delete_and_update_academician_overall_payment,
    sender=Payment
    )