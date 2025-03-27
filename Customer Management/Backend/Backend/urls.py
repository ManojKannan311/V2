"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Frontend import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',views.index,name="Landingpage"),
    path('Customers/',views.User_customer,name="User_customer_view"),
    path('customers_details/', views.gEt_C_details, name='customer_view'),
    path("Filter_C_details/<str:number>/",views.Filter_C_details,name="Filer_C_By_Num"),
    path("Ex_Cus_purchase/<str:number>/",views.Ex_Cus_purchase,name="Ex_Cus_purchase"),
    path("Get_customer/<int:id>",views.gEt_details,name="Get_specific_customer"),
    path("dEl_customer/<int:id>",views.dEl_customer,name="Delete_Customer"),
    path("Staff_details/",views.gEt_Product,name="Get_staff"),
    path("Customer_feedback/<str:id>",views.gEt_feedback,name="Customer_feedback"),
    # Staff Page:
    path("Employee/",views.Emp_page,name="Staff"),
    path("Register_user/",views.craete_Users,name="Register"),
    path("dEl_user/<int:id>/<str:name>",views.delete_user,name="User_delete"),
    #Employee:
    path("Status/",views.status_page,name="Status_page"),
    path("Filter_Status/<str:status>",views.gEt_Status,name="Get_status"),
    path("Get_specific/<int:id>/",views.Get_specific,name="Customer_details"),
    # Inventory:
    path("Inventory/",views.Incentives_page,name="Incentives_Page"),
    # User Login 
    path("",views.user_login_page,name="User_login"),
    # path("Login_user/",views.login_user,name="Login"),
    # path("logout_user/",views.logout_user,name="Logout"),
    path("user_Dashboard/",views.user_Dashboard,name="User_dashboard"),
    path("Update_status/<int:id>",views.gEt_details_users,name="Update_status"),
    path('EQ/<str:id>',views.gEt_EQ,name="Get_enquiery"),
    path("Filter_data/<str:date>",views.Filter_data),
    # Admin login
    path("admin_login_page/",views.admin_login_page,name="Admin_login"),
    path("Login_admin/",views.login_admin,name="Login_admin"),
    path("logout_admin/",views.logout_admin,name="Logout_admin"),
    path("manager_task/",views.manager_task,name="Manager_task"),
    
    
    #User_inc:
    path("user_inc/",views.User_incentive,name="User_incentive"),
    path("Get_incentive_data/<str:name>",views.Get_incentive_data,name="Get_incentive_data"),
    path("Get_incentive_month/<int:month>/<int:year>/<str:name>/", views.Get_incentive_month, name="Get_incentive_month"),

    # Broucher
    path("Broucher/",views.admin_broucher,name="Admin_broucher"),
    path("create_catogery/",views.create_catogery,name="Add_catogery"),
    path("add_product/",views.add_product,name="add_product"),
    path("gEt_sub_cat/<int:name>/",views.gEt_sub_cat,name="Get_sub_category"),
    path("pOst_sub_cat/",views.pOst_sub_cat,name="pOst_sub_cat"),
    path("Multi_filter/<int:main>/", views.Multi_filter, name="Multi_filter_main"),
    path("Multi_filter/<int:main>/<int:sub>/", views.Multi_filter, name="Multi_filter_with_sub"),
    path("Edit_product/<int:id>",views.Edit_product,name="Edit_product"),
    path("product_customer/<int:id>/",views.product_customer,name="product_customer"),
    path("Download_Broucher_page/",views.Download_Broucher_page,name="Broucher_Download"),
    path("download-brochure/", views.download_brochure, name="download_brochure"),
    path("Delete_SubCato/<int:id>/",views.Delete_Cato,name="Delete_SubCato"),
    
    # CHARTs
    path("sales_chart/",views.sales_chart,name="sales_chart"),
    path("user_sales_chart/",views.user_sales_chart,name="user_sales_chart")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

