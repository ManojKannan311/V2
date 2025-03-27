from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,HttpResponse
import json
import random
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import logout
from django.utils.timezone import now, timedelta
from django.db import transaction
from django.db.models import Sum
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
import json
import textwrap
from operator import itemgetter
from itertools import groupby
import os
import re
from django.core.files.uploadedfile import InMemoryUploadedFile

from reportlab.platypus import Image

def user_login_page(request):
    return render(request ,"User_logins.html")

def admin_login_page(request):
    return render(request ,"admin_Login.html")

# n error occurred: Cannot assign "<CustomUser: User_1>": "Bill.staff_id" must be a "User_details" instance.
# def login_user(request):
#     if request.method == "POST":
#         username = request.POST.get('name')
#         password = request.POST.get('pass')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user) 
#             request.session['username'] = user.username
#             request.session['role'] = "user" 
#             request.session.set_expiry(8 * 60 * 60)
            
#             return redirect('User_dashboard')
#         else:
#             return render(request, 'User_Logins.html', {"error": "Invalid credentials!"})

#     return render(request, 'admin_logins.html')

def login_admin(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("pass")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            request.session["username"] = user.username
            request.session["role"] = user.role
            request.session.set_expiry(8 * 60 * 60)
            if user.role == "staff":
                return redirect("User_dashboard")
            elif user.role  == "superadmin":
                return redirect("Landingpage")
            elif user.role  == "admin":
                return redirect("Manager_task")
            else:
                messages.error(request, "Invalid role assigned.")
                return redirect("User_login")
        messages.error(request, "Invalid username or password.")
        return redirect("User_login")

    return render(request, "admin_Login.html")
# def logout_user(request):
#     logout(request) 
#     request.session.flush() 
#     return redirect('User_login')

def logout_admin(request):
    if request.user.is_authenticated:
        logout(request) 
        request.session.flush()
        print("Session Flushed out!....")

    return redirect('User_login') 

@login_required(login_url="/") 
def user_Dashboard(request):
    username = request.session.get('username')

    if not username:
        return redirect('User_dashboard')
    get_task = Customer.objects.select_related("Staff_Assign").filter(Staff_Assign__username=username,).values(
         "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "address", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username","Remainder_date",
        "Payment", "added_by", "created_at","Staff_Assign_id"
    )
    get_insentive_data = Bill.objects.select_related("staff_id").filter(staff_id__username=username).values(
        "bill_id","staff_id__username","customer_name",
        "product_value","courier_charge","payment_status",
        "courier_id","couriered_date","staff_id"
        
    )
    
    get_user =CustomUser.objects.filter(username=username).values(
        "username","id"
    )
    return render(request, "User_index.html", {"name": get_user,"customers": get_task,"incentive":get_insentive_data})




# Manager task
@login_required(login_url="/") 
def manager_task(request):
    username = request.session.get('username')
    if not username:
        return redirect('User_dashboard')
    get_task = Customer.objects.select_related("Staff_Assign").filter(Staff_Assign__username=username,).values(
         "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "address", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username","Remainder_date",
        "Payment", "added_by", "created_at","Staff_Assign_id"
    )
    get_insentive_data = Bill.objects.select_related("staff_id").filter(staff_id__username=username).values(
        "bill_id","staff_id__username","customer_name",
        "product_value","courier_charge","payment_status",
        "courier_id","couriered_date","staff_id"
        
    )
    
    get_user =CustomUser.objects.filter(username=username).values(
        "username","id"
    )
    return render(request, "Manager._task.html", {"name": get_user,"customers": get_task,"incentive":get_insentive_data})



@login_required(login_url="/") 
def gEt_details_users(request,id):
    if request.method == "GET":
        customer_details = list(
        Customer.objects.select_related( "Staff_name").filter(id=id).values(
        "status","Remainder_date"
    ))
        return JsonResponse({"Customer_details": customer_details}, safe=False)

    if request.method == "POST":
        print("Received a POST request")

        try:
            data = json.loads(request.body)
            fillup = ""
            customer = get_object_or_404(Customer, id=id)
            print("Customer found:", customer)

            customer.name = data.get("name", customer.name)
            customer.phone_number = data.get("phone_number", customer.phone_number)
            customer.Email_id = data.get("Email_id", customer.Email_id)
            customer.address = data.get("address", customer.address)
            customer.Enquiry_details = data.get("Enquiry_details", customer.Enquiry_details)
            customer.status = data.get("status", customer.status)
            customer.Requried_date = data.get("Requried_date", customer.Requried_date)
            customer.Reminder_date = data.get("Reminder_date", customer.Reminder_date)
            customer.Product_Price = data.get("Product_Price", customer.Product_Price)
            customer.Payment = data.get("Payment", customer.Payment)
            customer.Feed_back = data.get("feedback", customer.Feed_back) or fillup
            customer.Remainder_date = data.get("Remainder_date", customer.Remainder_date) or customer.Remainder_date
            staff_data = Customer.objects.filter(id=id).values("Staff_Assign__id").first()
            print("Staff data fetched:", staff_data)

            if staff_data and staff_data["Staff_Assign__id"]:
                staff_instance = get_object_or_404(CustomUser, id=staff_data["Staff_Assign__id"])
                print("Staff instance found:", staff_instance)
                customer.Staff_Assign = staff_instance
            else:
                print("No Staff_Assign found, skipping assignment.")

            print("Saving customer...")
            customer.save()
            print("Customer updated successfully!")
            messages.success(request,"Status Update sucessfully!.")
            return JsonResponse({"success": True, "message": "Customer updated successfully!"})

        except Exception as e:
            print("Error occurred:", str(e))
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
@login_required(login_url="/")     
def User_incentive(request):
    if request.method == "POST":
        try:
            bill_id = request.POST.get("bill_id")
            customer_id = request.POST.get("customer_name")
            staff_assign = request.POST.get("Staff_Assign")
            product_value = request.POST.get("product_value")
            courier_charge = request.POST.get("courier_charge")
            payment_status = request.POST.get("payment_status")
            courier_id = request.POST.get("courier_id")
            couriered_date = request.POST.get("couriered_date")


            try:
                C_staff = CustomUser.objects.get(id=staff_assign)

            except CustomUser.DoesNotExist:
                messages.error(request, "Staff not found!")
                return redirect("User_dashboard")

            if Bill.objects.filter(bill_id=bill_id).exists():
                messages.error(request, "Incentive already exists for this Bill ID!")
                return redirect("User_dashboard")
            
            
            if Bill.objects.filter(customer_name=customer_id).exists():
                messages.error(request, "Incentive already exists for this Customer ID!")
                return redirect("User_dashboard")

            customer = Customer.objects.filter(Customer_ID=customer_id).first()

            if not customer:
                messages.error(request,"❌ Customer ID not found.")
                return redirect("User_dashboard")
                
               
            if customer:
                if customer.status:  
                    Bill.objects.create(
                        bill_id=bill_id,
                        customer_name=customer_id,
                        staff_id=C_staff,
                        product_value=product_value,
                        courier_charge=courier_charge,
                        payment_status=payment_status,
                        courier_id=courier_id,
                        couriered_date=couriered_date
                    )

                    messages.success(request, "Incentive added successfully!")
                else:
                    messages.error(request, "Order is already Cancelled or Completed, so no incentive can be added.")
            else:
                messages.error(request, "Customer not found!")

        except IntegrityError:
            messages.error(request, "Duplicate Bill ID! Incentive is already added.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("User_dashboard")
    
@login_required(login_url="/")     
def gEt_EQ(request,id):
    if request.method == "GET":
        try:
            customer = Customer.objects.filter(Customer_ID=id).first()

            if not customer:
                messages.error(request,"❌ Customer ID not found.")

                return redirect("User_dashboard")
            else:
                data = Customer.objects.filter(Customer_ID=id).values("Enquiry_details", "id","phone_number","address").first()
                if data:
  
                    return JsonResponse({"Eq": data}, safe=False)        
        except:
            return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)       
            
            
 
@login_required(login_url="/")  
def Filter_data(request, date):
    if request.method == "GET":
        get_task = list( 
            Customer.objects.select_related("Staff_Assign")
            .filter(created_at=date)
            .exclude(status="Completed")
            .values(
                "id", "Customer_ID", "name", "phone_number", "Email_id", 
                "Requried_date", "Reminder_date", "address", "Enquiry_details", 
                "status", "Product_Price", "Staff_Assign__username", "Remainder_date",
                "Payment", "added_by", "created_at", "Staff_Assign_id"
            )
        )
        return JsonResponse({"Eq": get_task}, safe=False)
      
    
    
# def user_Dashboard(request):
#     get_task = Customer.objects.filter(Staff_Assign__username=request.session['username'])

#     print(list(get_task))
#     return render(request, "User_index.html", {"name": request.session.get("username")})




# ADMIN =-------------------------------------------------------------------------------------------- 




def generate_unique_id():
    return str(random.randint(1000, 9999))
@login_required(login_url="/") 
def User_login(request):
    return render(request,"User_Login.html")
    
@login_required(login_url="/") 
def index(request):
    total_sales = Bill.objects.aggregate(total_sales=Sum('product_value'))['total_sales'] or 0
    total_customers = Customer.objects.count()
    
    pending_customers = Customer.objects.filter(status="Pending").count()
    completed_customers = Customer.objects.filter(status="Completed").count()
    online_threshold = now() - timedelta(seconds=3)

    users = CustomUser.objects.values("username","role")
    return render(request,"index.html",{
        "total_sales": total_sales,
        "total_customers": total_customers,
        "pending_customers": pending_customers,
        "completed_customers": completed_customers,
        "users": users
    })
@login_required(login_url="/") 
def User_customer(request):
    details = CustomUser.objects.values(
        "username","id"
    )
    return render(request,"User_Customer.html",{"details": details})

@login_required(login_url="/") 
def Filter_C_details(request,number):

    if request.method == "GET":
        customers = list(Customer.objects.select_related( "Staff_name").filter(phone_number=number).values(
            "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "address", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username",
        "Payment", "added_by", "created_at","Staff_Assign_id")) 
        return JsonResponse({"customers": customers}, safe=False)
    
@login_required(login_url="/")    
def Ex_Cus_purchase(request,number):
        feach_details = Customer.objects.filter(phone_number=number).values(
             "name", "phone_number", "Email_id","address","Payment","address"
        ).first()
        data_set ={"customer": feach_details}

        try:   
            data = json.loads(request.body)
            assign_to = data.get("assign_to")
            required_date = data.get("required_date")
            reminder_date = data.get("reminder_date")
            status = data.get("status")
            enquiry_details = data.get("enquiry_details")

            C_staff =CustomUser.objects.get(id=assign_to)
            
            customer = Customer.objects.create(
            Customer_ID=f"CMS{generate_unique_id()}",
            name=data_set["customer"].get("name"),
            phone_number=data_set["customer"].get("phone_number"),
            Email_id=data_set["customer"].get("Email_id"),
            Requried_date=required_date or None,
            Reminder_date=reminder_date or None,
            Payment=data_set['customer'].get("Payment"),
            Product_Price= None,
            address=data_set["customer"].get("address"),
            Enquiry_details=enquiry_details,
            Staff_Assign=C_staff,
            status=status or "Pending",
            )
            messages.success(request, f"Customer added successfully! Customer_id:{customer.Customer_ID}")
            return redirect('User_customer_view')
        except Exception as e:
            messages.success(request,str(e))
            return JsonResponse({"Staff_details": "Error"})
@login_required(login_url="/") 
def gEt_C_details(request):
    if request.method == "GET":
        select =request.session['username']
        customers = list(Customer.objects.select_related( "Staff_name").values(
            "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "address", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username",
        "Payment", "added_by", "created_at","Staff_Assign_id")) 
        user_role = CustomUser.objects.values("role").get(username=request.user.username)
        return JsonResponse({"customers": customers, "role": user_role["role"]}, safe=False)
        

    if request.method == "POST":
        try:   
            C_name = request.POST.get("name")
            C_phoneNumber = request.POST.get("phone_number")
            
            if Customer.objects.filter(phone_number=C_phoneNumber).exists():
                messages.error(request,"Customer alread exit")
                return redirect('User_customer_view')

            
            
            C_Email_id = request.POST.get("Email_id")
            C_Requried_date = request.POST.get("Requried_d")
            C_Reminder_date = request.POST.get("Reminder_d")
            C_Payment_mode = request.POST.get("Payment")
            C_Product = request.POST.get("Product")
            C_Product_Price = request.POST.get("Product_Price")
            C_address = request.POST.get("address")
            C_Enquiry_details = request.POST.get("Enquiry_details")
            C_Staff_Assign = request.POST.get("Staff_Assign")
            C_status = request.POST.get("C_status")
            
            C_staff =CustomUser.objects.get(id=C_Staff_Assign)
            
            customer = Customer.objects.create(
            Customer_ID=f"CMS{generate_unique_id()}",
            name=C_name,
            phone_number=C_phoneNumber,
            Email_id=C_Email_id,
            Requried_date=C_Requried_date or None,
            Reminder_date=C_Reminder_date or None,
            Payment=C_Payment_mode,
            Product_Price=float(C_Product_Price) if C_Product_Price else None,
            address=C_address,
            Enquiry_details=C_Enquiry_details,
            Staff_Assign=C_staff,
            status=C_status or "Pending",
            )

            messages.success(request, f"Customer added successfully! Customer_id:{customer.Customer_ID}")
            return redirect('User_customer_view')
        except Exception as e:
            messages.success(request,str(e))
            return JsonResponse({"Staff_details": "Error"})
@login_required(login_url="/")             
def gEt_Product(request):
    if request.method == "GET":
        Staff_details = list(CustomUser.objects.values("id", "username"))
        return JsonResponse({"Staff_details": Staff_details})
    
    
@login_required(login_url="/") 
def gEt_details(request,id):
    if request.method == "GET":
        customer_details = list(
        Customer.objects.select_related( "Staff_name").filter(id=id).values(
        "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "address", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username","Remainder_date",
        "Payment", "added_by", "created_at","Staff_Assign_id"
    ))
        return JsonResponse({"Customer_details": customer_details}, safe=False)

    if request.method == "POST":
        print("Received a POST request")
        
        try:
            data = json.loads(request.body)


            customer = get_object_or_404(Customer, id=id)

            customer.name = data.get("name", customer.name)
            customer.phone_number = data.get("phone_number", customer.phone_number)
            customer.Email_id = data.get("Email_id", customer.Email_id)
            customer.address = data.get("address", customer.address)
            customer.Enquiry_details = data.get("Enquiry_details", customer.Enquiry_details)
            customer.status = data.get("status", customer.status)
            customer.Requried_date = data.get("Requried_date", customer.Requried_date)
            customer.Reminder_date = data.get("Reminder_date", customer.Reminder_date)
            customer.Product_Price = data.get("Product_Price", customer.Product_Price)
            customer.Payment = data.get("Payment", customer.Payment)


            staff_id = data.get("Staff_Assign_id")
            if staff_id:
                customer.Staff_Assign = get_object_or_404(CustomUser, id=staff_id)

            customer.save()
            messages.success(request, "Customer updated successfully!")
            
            return JsonResponse({"success": True, "message": "Customer updated successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@login_required(login_url="/") 
def dEl_customer(request,id):
    if request.method == "DELETE":
        try:
            Remove_cus = Customer.objects.get(id=id)
            Remove_cus.delete()
            messages.success(request,"Customer Deleted Sucessfully!")
            return redirect('User_customer_view')
        except:
            return JsonResponse({"success": False, "error": "Bad Request"}, status=400)


# Employee:
@login_required(login_url="/") 
def Emp_page(request):
    roles = CustomUser.ROLE_CHOICES
    return render(request, "Employee.html", {"roles": roles})

@login_required(login_url="/") 
def craete_Users(request):
    if request.method == "GET":
        users = list(CustomUser.objects.values(
            "id", "username", "email", "phone_number", "role", 
            "date_joined", "last_login", "is_superuser"
        ))  


        return JsonResponse({"roles": users}, safe=False)
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("Staff")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("Staff")

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already registered!")
            return redirect("Staff")

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.phone_number = phone_number
        user.role = role
        user.save()

        messages.success(request, "User registered successfully!")
        return redirect("Staff")

        # user = User.objects.create_user(username=User_name, email=User_email, password=DOB_PassWord)
        # messages.success(request, "User registered successfully!")
        # return redirect("Staff")
@login_required(login_url="/")    
def delete_user(request, id,name):

    try:
        remove_user_detail = get_object_or_404(CustomUser, id=id)
        remove_user_detail.delete()
        remove_login = get_object_or_404(User, Username=name)
        remove_login.delete()
        messages.success(request, "User deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting user: {str(e)}")

    return redirect("Staff")


# Status:
@login_required(login_url="/") 
def status_page(request):
    return render(request,"Status.html")

@login_required(login_url="/") 
def gEt_Status(request,status):
    if request.method == "GET":
        customer_details = list(
        Customer.objects.select_related( "Staff_name").filter(status=status).values(
        "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username", "Staff_Assign__email",
        "Payment", "added_by", "created_at"
    ))
        return JsonResponse({"Customer_details": customer_details}, safe=False)
 
def Get_specific(request,id):
    if request.method == "GET":
        customer_details = list(
        Customer.objects.select_related( "Staff_name").filter(id=id).values(
        "id", "Customer_ID", "name", "phone_number", "Email_id", "Requried_date", 
        "Reminder_date", "Enquiry_details", "status", "Product_Price", 
        "Staff_Assign__username", "Staff_Assign__email",
        "Payment", "added_by", "created_at"
    ))
        return JsonResponse({"Specific_Customer_details": customer_details}, safe=False) 
    
    
# Incentives  
@login_required(login_url="/") 
def Incentives_page(request):
    today = date.today()
    current_month = today.month
    current_year = today.year
    staff_sales = (
        Bill.objects.filter(created_at__month=current_month, created_at__year=current_year)
        .values("staff_id__username","staff_id__id")
        .annotate(Total_Product_Price=Sum("product_value"))
    )

    staff_list = [
        {
            "username": staff["staff_id__username"],
            "Total_Product_Price": staff["Total_Product_Price"] or 0 
        }
        for staff in staff_sales
    ]
    return render(request, "Incentives.html", {"Staff_details": staff_list})


def Get_incentive_data(request,name):
    if request.method == "GET":
        staff_sales =list(Bill.objects.select_related("staff_id").filter(staff_id__username=name).values(
            "bill_id","customer_name","staff_id","product_value","payment_status","created_at"
        ))

        return JsonResponse({"Details":staff_sales},safe=False)
    
@login_required(login_url="/")     
def Get_incentive_month(request, month, year, name):
    if request.method == "GET":
        staff_sales = list(
            Bill.objects.select_related("staff_id")
            .filter(
                staff_id__username=name,
                created_at__month=month,
                created_at__year=year
            )
            .values("bill_id", "customer_name", "product_value", "payment_status", "created_at")
        )

        return JsonResponse({"Details": staff_sales}, safe=False)

@login_required(login_url="/") 
def gEt_feedback(request,id):
    if request.method == "GET":
        try:
            customer = Customer.objects.filter(Customer_ID=id).first()
            if not customer:
                messages.error(request,"❌ Customer ID not found.")
                return redirect("User_dashboard")
            else:
                data = Customer.objects.filter(Customer_ID=id).values("Feed_back", "id","updated_at","phone_number").first()
                if data:

                    return JsonResponse({"Eq": data}, safe=False)        
        except:
            return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)    


# --------------------------------------------------------Broucher &  Product  secetion -------------------------------------------------------------

def Product_unique_id():
    return str(random.randint(10000, 99999))

def admin_broucher(request):
    Catogery_name = Catogery.objects.values(
        "name","id"
    )
    categories = Catogery.objects.all()
    
    category_data = []
    for category in categories:
        subcategories = Subcategory.objects.filter(category=category).values("id", "name")
        category_data.append({
            "id": category.id,
            "name": category.name,
            "subcategories": list(subcategories)
        })
        
    role = request.session.get("role")
    if role in ["superadmin", "admin"]:
        return render(request, "Admin_brocher.html", {"Catogery": Catogery_name, "categories": category_data})
    elif role == "staff":
        print("Hello  i am in ")
        return render(request, "Users_brocher.html", {"Catogery": Catogery_name, "categories": category_data})
    else:
        return redirect("User_login")
    
        

# Create catogery
def create_catogery(request):
    if request.method == "POST":
        try:
            Catogery_name = request.POST.get("Catogery_name").lower()
           
            if Catogery.objects.filter(name=Catogery_name).exists():
                messages.error(request, "Catogery is already exist !")
                return redirect("Admin_broucher")
            
            Catogery.objects.create(
                name=Catogery_name
            )
            messages.success(request,"Catogery add successfully!.")
            return redirect("Admin_broucher")
        except Exception as e:
            return JsonResponse({"Error":e})

def add_product(request):
    if request.method == "GET":
        all_values = Product.objects.select_related("category").values(
            "id", "name", "stock", "category__name", "product_id",
            "Retail_Price", "Re_seller_Price", "Wholesale_Price"
        )
        product_list = []

        for product in all_values:
            product_data = dict(product)
            # Fetch all product images
            product_images = list(ProductImage.objects.filter(product_id=product["id"]).values_list("image", flat=True))
            # Build absolute URLs for images
            product_data["images"] = [
                request.build_absolute_uri(settings.MEDIA_URL.rstrip("/") + "/" + img) for img in product_images
            ] if product_images else []
            product_list.append(product_data)
        return JsonResponse({"Products": product_list, "role": request.session.get("role")}, safe=False)
    
    
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("AddPcategory")
        stock = request.POST.get("stock")
        images = request.FILES.getlist("image")
        description = request.POST.get("add_description")
        subcategory_id = request.POST.get("subcategory1")
        Retail_Price = request.POST.get("Retail_P")
        Re_seller_Price = request.POST.get("Re_seller_P")
        Wholesale_Price = request.POST.get("Wholesale_P")
        print(images)
  
        try:
            category = Catogery.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
        except Catogery.DoesNotExist:
            messages.error(request, "Invalid Category.")
            return redirect("Admin_broucher")
        except Subcategory.DoesNotExist:
            messages.error(request, "Invalid Subcategory.")
            return redirect("Admin_broucher")

        # Create Product
        product = Product.objects.create(
            product_id=f"SN{Product_unique_id()}",
            name=name.lower(),
            category=category,
            stock=stock,
            subcategory=subcategory,
            Retail_Price=Retail_Price,
            Re_seller_Price=Re_seller_Price,
            Wholesale_Price=Wholesale_Price,
            description=description,
        )

        # Validate and Save Multiple Images
        max_size = 3 * 1024 * 1024  # 3MB limit per image
        for image in images:
            if isinstance(image, InMemoryUploadedFile) and image.size > max_size:
                messages.error(request, "Each image must be less than 3MB.")
                continue  # Skip this image and process others

            ProductImage.objects.create(product=product, image=image)

        messages.success(request, "Product added successfully!")
        return redirect("Admin_broucher")
    
# Get Sub-Category
def gEt_sub_cat(request,name):
    if request.method == "GET":
        data_set = list(
                Subcategory.objects.select_related("category")
                .filter(category__id=name)
                .values("id", "name", "category__id")
            )
       
        return JsonResponse({"sub": data_set}, status=200)
    
def pOst_sub_cat(request):
    if request.method == "POST":
        sub_name =request.POST.get("subcategory_name")
        main_name=request.POST.get("main_category")
        if Subcategory.objects.filter(name=sub_name).exists():
            messages.error(request,"Subcategory already exist !")
            return redirect("Admin_broucher")
            
        main_category = Catogery.objects.get(id=main_name)

        try:
            Subcategory.objects.create(
                name=sub_name,
                category=main_category
            )
            
            messages.success(request, "Subcategory Created Successfully!..")
            return redirect("Admin_broucher")
              
        except Catogery.DoesNotExist:
            messages.error(request, "Main Category Not Found!")
            return redirect("Admin_broucher")
        
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=400)
    return JsonResponse({"Error": "Invalid request method"}, status=405)

def Multi_filter(request, main, sub=None):
    if request.method == "GET":
        try:
            get_object_or_404(Catogery, id=main)
            products = Product.objects.filter(category__id=main)
            if sub is not None:
                products = products.filter(subcategory__id=sub)

            product_list = []
            for product in products:
                product_data = {
                    "id": product.id,
                    "name": product.name,
                    "stock": product.stock,
                    "category__name": product.category.name,
                    "subcategory__name": product.subcategory.name if product.subcategory else None,
                    "product_id": product.product_id,
                    "Retail_Price": product.Retail_Price,
                    "Re_seller_Price": product.Re_seller_Price,
                    "Wholesale_Price": product.Wholesale_Price,
                    "images": [
                        request.build_absolute_uri(settings.MEDIA_URL + img.image.name)
                        for img in product.images.all()
                    ],
                }
                product_list.append(product_data)

            return JsonResponse({"products": product_list, "role": request.session.get("role", "guest")}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
def Edit_product(request,id):
    if request.method == "GET":
        try:
            product = list(
                Product.objects.filter(id=id).values("stock","id","Retail_Price","Re_seller_Price","Wholesale_Price"))
            return JsonResponse({"product":product},safe=False,status=200)
        except Product.DoesNotExist as e :
            return JsonResponse({"Error":e} ,status=500)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            stock = data.get("stock")
            Retail= data.get("Retail")
            Re_sellers = data.get("Re_sellers")
            Wholesellers =data.get("Wholesellers")
 
            if stock is None or not str(stock).isdigit():
                return JsonResponse({"error": "Invalid stock value"}, status=400)
            product = get_object_or_404(Product, id=id)
            product.stock = int(stock)
            product.Retail_Price =float(Retail)
            product.Re_seller_Price =float(Re_sellers)
            product.Wholesale_Price =float(Wholesellers)
            
            product.save()
            return JsonResponse({"success": "Stock updated successfully!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def product_customer(request,id):
    if request.method == "DELETE":
        try:
            Remove_cus = Product.objects.get(id=id)
            Remove_cus.delete()
            messages.success(request,"Customer Deleted Sucessfully!")
            return redirect('User_customer_view')
        except:
            return JsonResponse({"success": False, "error": "Bad Request"}, status=400)
        
        
# User Side Broucher:


def Download_Broucher_page(request):
    return render(request ,"User_B_D.html")

def normalize_product_name(name):
    """Remove dimensions like 3*3, 4*4, etc., to group products under a base name."""
    return re.sub(r"\b\d+\*\d+\b", "", name).strip()


def check_space_and_move(pdf, y_position, required_space):
    """Move to the next page if there isn't enough space left."""
    if y_position - required_space < MIN_Y_POSITION:
        pdf.showPage()
        return TOP_MARGIN
    return y_position
PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 50
TOP_MARGIN = 750
IMAGE_HEIGHT = 250
IMAGE_WIDTH = 200
LINE_HEIGHT = 15
BOTTOM_MARGIN = 0
MIN_Y_POSITION = BOTTOM_MARGIN + 50

from reportlab.lib.colors import HexColor
from django.views.decorators.csrf import csrf_exempt

def download_brochure(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category_id = data.get("category")
            subcategory_id = data.get("subcategory")
            buyer_type = data.get("buyer_type")
            price_range = data.get("price_range")
            Minimum_stock =data.get("Minimum_stock")
            Product_code =data.get("Product_code")
            # **Filtering Products**
            filters = {}
            if category_id:
                filters["category_id"] = category_id
            if subcategory_id:
                filters["subcategory_id"] = subcategory_id
            if price_range and buyer_type:
                filters[f"{buyer_type}__lte"] = price_range
            if Minimum_stock:
                filters["stock__gte"] =Minimum_stock
            if Product_code:
                filters["product_id"]=Product_code

            products = Product.objects.filter(**filters).prefetch_related("images")

            # **Processing Product Data**
            product_list = [
                {
                    "name": product.name,
                    "normalized_name": normalize_product_name(product.name),
                    "product_id": product.product_id,
                    "stock": product.stock,
                    "description": product.description or "No description available",
                    buyer_type: getattr(product, buyer_type, None),
                    "images": [img.image.url for img in product.images.all()],
                }
                for product in products if product.stock > 0
            ]

            # **Group Products by Normalized Name**
            product_list.sort(key=lambda p: p["normalized_name"])
            grouped_products = {
                key: list(group) for key, group in groupby(product_list, key=lambda p: p["normalized_name"])
            }

            # **PDF Creation**
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setTitle("Premium Product Brochure")

            # **Brand Colors**
            primary_color = HexColor("#2C3E50")  # Dark Blue
            secondary_color = HexColor("#E74C3C")  # Red Accent
            text_color = HexColor("#333333")  # Dark Gray

            # **First Page - Branding**
            pdf.setFillColor(primary_color)
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawCentredString(PAGE_WIDTH / 2, 700, "Saravana Naithukada")
            pdf.setFont("Helvetica", 14)
            pdf.setFillColor(text_color)
            pdf.drawCentredString(PAGE_WIDTH / 2, 660, "Timeless Elegance & Unmatched Craftsmanship")


            # **Each Grouped Product on a New Page**
            for base_name, product_variants in grouped_products.items():
                pdf.showPage()
                y_position = TOP_MARGIN  # Reset position for new page

                # **Product Group Title**
                pdf.setFillColor(primary_color)
                pdf.setFont("Helvetica-Bold", 18)
                pdf.drawCentredString(PAGE_WIDTH / 2, y_position, base_name)
                y_position -= 30

                for product in product_variants:
                    # **Check Space & Move to New Page if Needed**
                    y_position = check_space_and_move(pdf, y_position, 200)  

                    default_image_path = os.path.join(settings.MEDIA_ROOT, 'no_image.png')
                    x_start = 130  # Left margin
                    images_per_row = 2  # Set number of images per row
                    image_spacing = 20  # Space between images
                    row_height = IMAGE_HEIGHT + image_spacing

                    image_count = len(product["images"])
                    x_position = x_start
                    images_in_row = 0

                    # **Check if only one image is present**
                    if image_count == 1:
                        img_url = product["images"][0]

                        if img_url.startswith(settings.MEDIA_URL):
                            img_url = img_url.replace(settings.MEDIA_URL, "")
                        img_path = os.path.join(settings.MEDIA_ROOT, img_url)

                        if not os.path.exists(img_path):
                            img_path = default_image_path  # Use fallback image

                        # **Ensure Space Before Adding Image**
                        if y_position - (IMAGE_HEIGHT * 1.5) < BOTTOM_MARGIN:
                            pdf.showPage()  # Move to next page
                            y_position = TOP_MARGIN  # Reset y position

                        try:
                            img = Image(img_path, width=IMAGE_WIDTH * 1.5, height=IMAGE_HEIGHT * 1.5)  # Increase size for single image
                            x_center = (PAGE_WIDTH - (IMAGE_WIDTH * 1.5)) / 2  # Centering image
                            img.drawOn(pdf, x_center, y_position - (IMAGE_HEIGHT * 1.5))
                        except Exception:
                            pdf.setFont("Helvetica", 10)
                            pdf.drawString(x_center, y_position, "[Image Error]")

                        # y_position -= IMAGE_HEIGHT * 1.5 + 40  # Move down for next content

                    else:
                        for img_url in product["images"]:
                            if img_url.startswith(settings.MEDIA_URL):
                                img_url = img_url.replace(settings.MEDIA_URL, "")
                            img_path = os.path.join(settings.MEDIA_ROOT, img_url)

                            if not os.path.exists(img_path):
                                img_path = default_image_path  # Use fallback image

                            # **Ensure Space Before Adding New Image**
                            # if y_position - row_height < BOTTOM_MARGIN:
                            #     # pdf.showPage()  # Move to next page
                            #     y_position = TOP_MARGIN  # Reset y position

                            try:
                                img = Image(img_path, width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
                                img.drawOn(pdf, x_position, y_position - IMAGE_HEIGHT)
                            except Exception:
                                pdf.setFont("Helvetica", 10)
                                pdf.drawString(x_position, y_position, "[Image Error]")

                            # **Adjust Position for Next Image**
                            x_position += IMAGE_WIDTH + image_spacing
                            images_in_row += 1

                            # **Move to Next Row if Needed**
                            if images_in_row == images_per_row:
                                y_position -= row_height  # Move down for next row
                                x_position = x_start  # Reset x position
                                images_in_row = 0
                    y_position -= IMAGE_HEIGHT +150


                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.setFillColor(text_color)
                    pdf.drawString(160, y_position, f"Product Code: {product['product_id']}")
                    pdf.drawString(160, y_position - 20, f"Current Stock: {product['stock']}")

                    pdf.setFillColor(secondary_color)
                    pdf.drawString(160, y_position - 40, f"Price: {product.get(buyer_type, 'N/A')}")
                    y_position -= 60

                    # **Image Grid Layout (2 per row)**
                    

                    # **Description Section**
                    y_position = check_space_and_move(pdf, y_position, 50)
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.setFillColor(primary_color)
                    pdf.drawString(160, y_position, "Description:")
                    y_position -= 15
                    pdf.setFont("Helvetica-Oblique", 12)
                    pdf.setFillColor(text_color)
                    description_text = product["description"].split("\n")  # Split by actual new lines

                    for paragraph in description_text:
                        y_position = check_space_and_move(pdf, y_position, LINE_HEIGHT)

                        if paragraph.strip():  # If the paragraph is not empty, wrap and print it
                            wrapped_lines = textwrap.wrap(paragraph, width=70)  # Wrap text to fit within PDF width

                            for line in wrapped_lines:
                                y_position = check_space_and_move(pdf, y_position, LINE_HEIGHT)
                                pdf.drawString(160, y_position, line)
                                y_position -= LINE_HEIGHT  # Move down for next wrapped line

                        else:  # If it's an empty line, leave a blank space
                            y_position -= LINE_HEIGHT  # Just move down without writing anythin
                y_position -= 100 
            pdf.showPage()       

            # **Finalize PDF**
            pdf.save()
            buffer.seek(0)

            return HttpResponse(buffer, content_type="application/pdf", headers={"Content-Disposition": 'attachment; filename="Premium_Brochure.pdf"'})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def Delete_Cato(request, id):
    if request.method == "DELETE":
        try:
            delete_data = Subcategory.objects.get(id=id)
            delete_data.delete()
            messages.success(request,"Subcategory deleted successfully!")
            return JsonResponse({"status": "success", "message": "Subcategory deleted successfully!"}, status=200)
        except Subcategory.DoesNotExist:
            messages.success(request,"Subcategory not found!")
            return JsonResponse({"status": "error", "message": "Subcategory not found!"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

            
# Charts:
from django.db.models.functions import TruncMonth,TruncDay
import calendar

def sales_chart(request):
    sales_data = (
        Bill.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_sales=Sum("product_value"))
        .order_by("month")
    )
    all_months = [calendar.month_name[i] for i in range(1, 13)]
    sales_dict = {sale["month"].month: float(sale["total_sales"]) for sale in sales_data}
    labels = all_months
    sales_values = [sales_dict.get(i, 0) for i in range(1, 13)]
    return JsonResponse({"labels": labels, "sales_values": sales_values})



def user_sales_chart(request):
    user_sales_data = (
        Bill.objects.select_related("staff_id")
        .values("staff_id__username")
        .annotate(total_sales=Sum("product_value"))
        .order_by("-total_sales")
    )

    
    labels = [user["staff_id__username"] for user in user_sales_data]
    sales_values = [float(user["total_sales"]) for user in user_sales_data]

    return JsonResponse({"labels": labels, "sales_values": sales_values})
