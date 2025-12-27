from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='products')

    def __str__(self):
        return f'{self.title} - {self.price} - {self.category}'
    
   
    
class Review(models.Model):
    stars = models.IntegerField(choices=((i, i) for i in range(1, 6)), default=4)
    text = models.CharField(max_length=1000, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text
    
   

    
   


