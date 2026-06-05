from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Серийный номер")
    purchase_date = models.DateField(verbose_name="Дата покупки")
    warranty_months = models.IntegerField(verbose_name="Срок гарантии (в месяцах)")
    # НОВОЕ ПОЛЕ: Адрес хранения чека (ячейка)
    receipt_location = models.CharField(max_length=50, default="Не указано", verbose_name="Ячейка хранения чека")

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
