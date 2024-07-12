from django.db import models

class Kompaniya(models.Model):
    nom = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15, blank=True, null=True)
    manzil = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nom

    @property
    def mahsulotlar_soni(self):
        return self.mahsulotlar.count()

    class Meta:
        verbose_name_plural = 'Kompaniyalar'

class Mahsulot(models.Model):
    nom = models.CharField(max_length=100)
    kompaniya = models.ForeignKey(Kompaniya, related_name='mahsulotlar', on_delete=models.CASCADE)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    soni = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom} {self.kompaniya}"

class Savdo(models.Model):
    mijoz_nomi = models.CharField(max_length=100)
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.PROTECT)
    soni = models.PositiveIntegerField()
    savdo_sanasi = models.DateTimeField(auto_now_add=True)

    @property
    def umumiy_narx(self):
        return self.mahsulot.narx * self.soni

    @property
    def mahsulot_nomi(self):
        return self.mahsulot.nom

    @property
    def kompaniya_nomi(self):
        return self.mahsulot.kompaniya.nom

    def save(self, *args, **kwargs):
        if self.mahsulot.soni < self.soni:
            raise ValueError('Omborda yetarli mahsulot yo\'q')
        self.mahsulot.soni -= self.soni
        self.mahsulot.save()
        super().save(*args, **kwargs)
