from django.urls import path
from FP import views, views2

urlpatterns = [
    path('', views.index, name='index'),
    path('signuppage/', views.signuppage, name='signuppage'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('goalpage/', views.goalpage, name='goalpage'),
    path('first/', views.first, name='first'),
    path('base/', views.base, name='base'),
    path('contact/', views.contact, name='contact'),
    path('homep/', views.homep, name='homep'),
    path('Chart/', views.Chart),
    path('ChartIncome/', views.ChartIncome),
    path('UI/', views.UI, name='UI'),
    path('cpy/', views.cpy),
    path('cpy2/', views.cpy2),
    path('barchart/', views.barchart),
    path('aincome/', views.aincome),
    path('ain/', views.ain),
    path('report/', views.report,name='report'),
    path('ai_insights/', views2.ai_insights_page,name='ai_insights'),
    path('budget/', views.budget,name='budget'),
    path('LOGIN/', views.LOGIN,name='LOGIN'),
    path('LOGOUT/', views.LOGOUT,name='LOGOUT'),
    path('signup/', views.signup),
    path('addGoal/', views.addGoal),
    path('forgot_password/', views.forgot_password),

    path('verify-otp/', views.verify_otp),
    path('reset-password/', views.reset_password),
    path('delete-data/', views.delete_data),
    path('delete-data-budget/', views.delete_data_budget),
    path('user-data/', views.user_data),



]
