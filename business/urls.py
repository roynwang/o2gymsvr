from django.conf.urls import patterns, url
from business.views import *
'''
c: course
g: gym
b: book
s: schedule
r: read
'''
urlpatterns = patterns('',
		#url(r'^api/c/$', CourseList.as_view()),
		#url(r'^api/c/(?P<pk>[0-9]+)/$', CourseItem.as_view()),
		url(r'^api/groupcourse/(?P<pk>[0-9]{0,8})/$', GroupCourseItem.as_view()),
		url(r'^api/groupcoursebook/(?P<pk>[0-9]{0,8})/$', GroupCourseBookItem.as_view()),
		url(r'^api/groupcourseinstance/(?P<pk>[0-9]{0,8})/$', GroupCourseInstanceItem.as_view()),
		url(r'^api/todo/(?P<pk>[0-9]+)/$', TodoItem.as_view()),
		url(r'^api/todo/(?P<pk>[0-9]+)/recur/$', RecurTodoView.as_view()),
		url(r'^api/g/$', GymList.as_view()),
		url(r'^api/st/(?P<pk>[0-9]+)/$', SelfTrainItem.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/$', GymItem.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/selftrain/$', SelfTrainList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/todo/$', GymTodoList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/todo/(?P<date>[0-9]{8})/$', GymTodoList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/selftrain/(?P<date>[0-9]{8})/$', SelfTrainByDateList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/chargepricing/$', ChargePricingList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/finance/$', FinanceList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/flow/$', FlowList.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/flow/(?P<date>[0-9]{8})/$', FlowItemByDate.as_view()),
		url(r'^api/g/(?P<gymid>[0-9]+)/flow/(?P<pk>[0-9]+)/$', FlowItem.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/groupcourse/$', GymGroupCourseList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/groupcourseinstance/$', GroupCourseInstanceList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/groupcourseinstance/(?P<date>[0-9]{8})/$', GymGroupCourseDayList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/groupcoursebook/(?P<date>[0-9]{8})/$', GymGroupCourseDayBookList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/salesum/$', GymSumSale.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/customermonthaverage/(?P<date>[0-9]{6})/$', CustomerMonthAverageView.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/customermonthdetail/(?P<date>[0-9]{6})/$', customer_month_detail_view),
		url(r'^api/g/(?P<pk>[0-9]+)/incomplete/$', GymIncompleteList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/(?P<date>[0-9]{8})/$', GymScheduleList.as_view()),
		url(r'^api/g/(?P<pk>[0-9]+)/(?P<date>[0-9]{8})/load/$', GymLoadList.as_view()),
		#url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/$',ScheduleBulkCreate.as_view()),
		#schedule item
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/(?P<date>[0-9]{8})/(?P<hour>[0-9]{1,2})/$',ScheduleItem.as_view()),
		#schedule day booked items
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/b/(?P<date>[0-9]{8})/$',ScheduleList.as_view()),
		#read week booked items
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/w/(?P<date>[0-9]{8})/$',ScheduleForRead.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/w/$',ScheduleForReadQuery.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/kpi/$',CoachKPI.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/todaykpi/$',CoachTodayKPI.as_view()),
		#read availiable hours in day
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/d/(?P<date>[0-9]{8})/$',DayAvaiableTime.as_view()),

		#body eval

                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/discount/(?P<date>[0-9]{8})/$', UserDateDiscountView.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/summary/(?P<gym>[0-9]+)/$', UserSummaryView.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/incomplete/$', CoachIncompleteList.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/coach/$', CurrentCoach.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/trial/$', TrialBookView.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,20})/groupcourse/$', CustomerGroupCourseList.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/$',BodyEvalDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/all/$',BodyEvalAllView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/data/$',BodyEvalDataView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/option/(?P<option>.+)/$',BodyEvalByOptionView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/(?P<date>[0-9]{8})/$',BodyEvalByDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/e/(?P<date>[0-9]{8})/(?P<pk>\d+)/$',BodyEvalItemView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/h/$',HealthQuesDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/h/(?P<date>[0-9]{8})/$', HealthQuesByDateView.as_view()),
		url(r'^api/e/$',AllEvalOptionsView.as_view()),
		url(r'^api/h/$',AllHealthQuesOptionsView.as_view()),

		#train
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/(?P<date>[0-9]{8})/a/(?P<pk>[0-9]+)/$',TrainItemView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/$',TrainDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/(?P<date>[0-9]{8})/$',TrainByDateView.as_view()),
		url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/t/(?P<date>[0-9]{8})/(?P<schedule>[0-9]+)/$',TrainByScheduleView.as_view()),
		url(r'^api/a/$',NearByView.as_view()),
		url(r'^api/a/(?P<pk>[0-9]+)/$', GymMap.as_view()),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/evalresult/$',show_customer_eval),
                url(r'^api/cs/(?P<courseid>[0-9]+)/$',show_post_survey),
                url(r'^api/cs/(?P<courseid>[0-9]+)/complete/$',show_complete_survey),
                url(r'^api/(?P<name>[a-zA-Z0-9]{4,64})/gesture/$',show_gesture_eval),
                url(r'^api/risk/$',get_health_risk),
		)
