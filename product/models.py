from django.db import models
from PIL import Image
import os
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    resume = models.TextField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    price_marketing = models.FloatField()
    price_marketing_promotion = models.FloatField(default=0)
    product_type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variation'),
            ('S', 'Simple'),
        )
    )


    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pil = Image.open(image_full_path)
        original_width, original_height = image_pil.size

        if original_width <= new_width:
            print('Largura original menor que nova largura')
            image_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        mew_image = image_pil.resize((new_width, new_height), Image.LANCZOS)
        mew_image.save(
            image_full_path,
            optimize=True,
            quality=50
        )

        print('Imagem redimencionada')


    def save(self, *args, **kwargs):
        super().save(self, *args, **kwargs)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)


    def __str__(self):
        return self.name


class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    price_promotion = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.name or self.product.name

    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'