from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class NameField(models.CharField):

    def camel_case(self,str_val):
        if not str_val:
            return str_val
        return str_val.replace(str_val[0], str_val[0].upper(), 1)

    def get_prep_value(self, value):
        if value is None:
            return value
        lwr =  str(value).lower()
        lwr = self.camel_case(lwr)
        # return re.sub('[^\w\d]', '', lwr)
        return lwr.strip()
    
class Item(models.Model):
    name = NameField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)
    item_img = models.ImageField(upload_to='images/')
    item_qty = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    item_desc = models.TextField(max_length=750, blank=True, null=True)
    tags = TaggableManager(blank=True)
    def __str__(self) -> str:
        return self.name


class BorrowRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    RETURNED = 'returned'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (RETURNED, 'Returned'),
        (REJECTED, 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrow_requests')
    requester_name = models.CharField(max_length=100)
    requester_email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    purpose = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.requester_name} - {self.item.name} ({self.quantity})'
