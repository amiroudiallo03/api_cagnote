from email import charset
from tabnanny import verbose
from django.db import models

# Create your models here.

#model academicien

class Base(models.Model):
    date_add = models.DateField(auto_now_add=True)
    date_update = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Reason(Base):
    name = models.CharField(max_length=200, verbose_name='nom', unique=True)

    class Meta:
        verbose_name = "Motif"
        verbose_name_plural = "Motifs"

    def __str__(self):
        return self.name

class Academician(Base):
    last_name = models.CharField(max_length=30 , verbose_name="nom", blank=True)
    first_name = models.CharField(max_length=40, verbose_name="prenom", blank=True)
    register_number = models.CharField(max_length=30,verbose_name="matricule", blank=True)
    picture = models.FileField(upload_to="pictures" , verbose_name="photos", blank=True)
    reasons = models.ManyToManyField(Reason, verbose_name="motif", through='Payment')

    class Meta:
        verbose_name = "Academicien"
        verbose_name_plural = "Academiciens"
    
    def __str__(self):
        return self.last_name


class Payment(Base):
    academician = models.ForeignKey(Academician, on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    montant = models.DecimalField( max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True) 
    payment_hour = models.TimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'paiement'
        constraints = [models.UniqueConstraint(fields=['academician', 'payment_date', 'reason'], name='payment_unique')]
    
    def __str__(self):
        return f"{self.academician}, {self.reason}, {self.montant}"
    


