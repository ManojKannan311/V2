from django.db import models
from django.contrib.auth.models import AbstractUser

class User_details(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    Role =models.CharField(max_length=50)
    New_pass =models.CharField(max_length=20)
    DOB =models.CharField(max_length=20)
    
    def __str__(self):
        return self.username
    
    
class CustomUser(AbstractUser):
    ROLE_CHOICES  = [
        ("superadmin", "SuperAdmin"),
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("Reseller", "Reseller"),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="admin_manager")
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    new_pass = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Staff(models.Model):
    user = models.OneToOneField(User_details, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
  
class Customer(models.Model):
    Customer_ID = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255,unique=False)
    phone_number = models.CharField(max_length=15, unique=False)
    Email_id = models.EmailField(max_length=255,null=True) 
    address = models.TextField(null=True)
    Enquiry_details = models.TextField(null=True)
    age = models.IntegerField(null=True, blank=True) 
    status = models.CharField(max_length=50)   
    Requried_date = models.DateField(null=True, blank=True)
    Reminder_date = models.DateField(null=True, blank=True)
    Product_Price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Staff_Assign = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Staff_name")
    Payment = models.CharField(max_length=50)
    added_by = models.CharField(max_length=200)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    Feed_back =models.TextField(null=True,blank=True)
    Remainder_date =models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task_status = models.CharField(max_length=50,blank=True)
    assigned_date = models.DateField(auto_now_add=True)
    Customer_feedback =models.TextField(blank=True)

    def __str__(self):
        return self.customer
    
class Catogery(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Catogery, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class Product(models.Model):  
    product_id = models.CharField(max_length=50,null=True)
    # image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    name = models.CharField(max_length=255, unique=False) 
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Catogery,on_delete=models.CASCADE,related_name="category")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    Retail_Price = models.IntegerField(default=0 ,null=True)
    Re_seller_Price = models.IntegerField(default=0,null=True)
    Wholesale_Price = models.IntegerField(default=0,null=True)
    Created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE ,null=True)
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"
    
class Incentive(models.Model):
    bill_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_mobile_no = models.CharField(max_length=15)
    product_value = models.DecimalField(max_digits=10, decimal_places=2)
    courier_charge = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=60)
    handled_staff_name = models.CharField(max_length=100)
    courier_id = models.CharField(max_length=100)
    couriered_date = models.DateField(auto_now=True)
    product_weight = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
    
    
class Bill(models.Model):

    bill_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=255)
    staff_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product_value = models.DecimalField(max_digits=10, decimal_places=2)
    courier_charge = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=30)
    courier_id = models.CharField(max_length=50)
    couriered_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return self.customer_name



