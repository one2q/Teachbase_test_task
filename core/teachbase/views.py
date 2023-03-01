from django.views import View
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from core import settings
from teachbase.client import TeachbaseClient
from teachbase.models import Course, CustomUser
from teachbase.serializers import CourseSerializer, UserCreateSerializer


class BaseView(View):
	def __int__(self):
		self.teachbase_client = TeachbaseClient(client_id=settings.CLIENT_ID,
		                                        client_secret=settings.CLIENT_SECRET,
		                                        base_url=settings.BASE_URL
		                                        )


class CreateUserView(BaseView, CreateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserCreateSerializer

	def post(self, request, *args, **kwargs):
		client = TeachbaseClient(client_id=settings.CLIENT_ID,
		                         client_secret=settings.CLIENT_SECRET,
		                         base_url=settings.BASE_URL
		                         )
		data = request.data
		print(data, "__________________________")
		final_data = _make_user_create_dict(data)
		print(final_data)

		user = client.create_user(json=final_data)
		CustomUser.objects.create(email=user["email"], name=user["name"], password=user["password"])
		user_data = self.serializer_class(user, many=True)
		# user_data = self.serializer_class(data=user, many=True)
		# user_data.is_valid(raise_exception=True)
		# user_data.save()
		return Response(user_data.data)


class CoursesListView(BaseView, ListAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

	def list(self, request, *args, **kwargs):
		courses = Course.objects.all()
		if courses:
			courses_data = self.serializer_class(courses, many=True)
			return Response(courses_data.data)
		else:
			#  client = self.teachbase_client  # TODO !!!!!!!
			client = TeachbaseClient(client_id=settings.CLIENT_ID,
			                         client_secret=settings.CLIENT_SECRET,
			                         base_url=settings.BASE_URL
			                         )
			courses = client.get_courses_list()
			courses_data = self.serializer_class(data=courses, many=True)
			courses_data.is_valid(raise_exception=True)
			courses_data.save()
			return Response(courses_data.data)


class CoursesDetailView(BaseView, RetrieveAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer


def _make_user_create_dict(data: dict) -> dict:
	final_dict = {
		"users":           [
			{
				"email":       data.get("email"),
				"name":        data.get("name"),
				"description": "Corrupti natus quia recusandae.",
				"last_name":   data.get("last_name"),
				"password": f'{data.get("password")}',
				"lang":     "ru",
				"phone":       "string",
				"role_id":     1,
				"auth_type":   0,
				"external_id": "u-0130",
				"labels":      {
					"234": "2524334"
				},
			}
		],
		"external_labels": True,
		"options":         {
			"activate":                 True,
			"verify_emails":            True,
			"skip_notify_new_users":    True,
			"skip_notify_active_users": True
		}
	}
	return final_dict