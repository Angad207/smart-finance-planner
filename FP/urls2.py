from django.urls import path
from FP import views2, views


urlpatterns = [
    path('linechart/', views2.linechart),
    path('addGoalJson/', views.addGoalJson),
    path('singleGoalAi/<int:index>/', views.singleGoalAi),
    path('ai_goal_coach/', views2.ai_goal_coach),
    path('chat_ai/', views2.chat_ai),
    path('addExpenceOnGoal/', views.addExpenceOnGoal),
    path('all_Transaction/', views2.all_Transaction),
    path('MonthlyBudget/', views.MonthlyBudget),
    path('budgetJson/', views.budgetJson),
    path('budgetai/', views.budgetai),
    path('resetbudget/', views.resetbudget),
    path('ai-insights-data/', views2.ai_insights_data),
    path('ask-ai/', views2.ask_ai),
    path('report-data/', views2.report_data, name='report_data'),
    path('ai-report/', views2.ai_report),
    path('download-report/', views2.download_report),
    ]