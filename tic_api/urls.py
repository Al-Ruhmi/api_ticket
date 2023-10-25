
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import  UserViewSet
from tic_api import views

router = routers.DefaultRouter()
router.register('users', UserViewSet)
# تسجيل حساب الطلاب ونوع المستخدم الافتراضي ليس موظف

urlpatterns = [
    path('', include(router.urls)),

    path('std_ticket_create/', views.StdTicketCreate.as_view()), 
    # للطالب ينشىء تدكرة ويعرضها ويعرض جميع التداكر الدي حجزها شخصيا

    path('std_tic_update/<int:pk>', views.StdTicUpdate.as_view()),
     # يعرض ويعدل ويحدف التدكرة برقم ايدي الخاصة بالطالب نفسة

    path('view_emp_open_task/', views.ViewEmpOpenTask.as_view()),
     # يعرض لاي موظف جميع التداكر المقدمة من جميع الطلاب ومازالت في حالة مفتوحة للمراجعه

    path('emp_update_open_task/<int:pk>', views.EmpUpdateOpenTask.as_view()),
     # يعرض ويحدث للموظف حالة التدكرة من مفتوحة الى قيد المعالجة او غيرها بالرقم وفقط ادا كانت في حالة مفتوحة

    path('view_emp_self_task/', views.ViewEmpSelfTask.as_view()),
     # يعرض للموظف نفسة كل التداكر التي قام بمراجعتها سابقا

    path('emp_update_self_task/<int:pk>', views.EmpUpdateSelfTask.as_view()),
     # يعرض ويعدل التداكر التي قد تم مراجعتها بالرقم في حال تم الانجاز او الرفض

]