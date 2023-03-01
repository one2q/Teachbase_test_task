from typing import Dict, List, Optional, Union, Callable

import requests

# TODO !!!!!!!!!!!
bas_url = "https://go.teachbase.ru/"

key = "8bdf8070ca5eb1ee7565aa4722e9772a60612310f62f0a04ba4774e7527c836b"
secret = "c2c76197cc8de37d0d04a9cc4127ef7bb5c0961d4f96eeec6fff403e30b304dd"


class TeachbaseException(Exception):
	pass


class TeachbaseClient:
	def __init__(self, client_id: str, client_secret: str, base_url: str):
		self.client_id = client_id
		self.client_secret = client_secret
		self.base_url = base_url
		self.api_endpoint = "endpoint/v1/"
		self.token_data = None
		self.token = None

	def authentication(self) -> None:
		path: str = "oauth/token/"
		url = self.base_url + path
		data = {
			"grant_type":    "client_credentials",
			"client_id":     self.client_id,
			"client_secret": self.client_secret,
		}

		response = requests.post(url, data=data)
		result = response.json()

		self.token_data = result
		self.token = result.get("access_token")

	def is_token_valid(self) -> bool:
		path: str = "_ping"
		url = self.base_url + self.api_endpoint + path
		response = requests.get(
				url=url,
				headers=self.headers,
		)
		return response.status_code == 200

	@staticmethod
	def refresh_token(func: Callable) -> Callable:
		"""
		This decorator make authentication and refresh token if necessary
		"""

		def wrapper_refresh(self, *args, **kwargs):
			if not self.is_token_valid():
				self.authentication()
			return func(self, *args, **kwargs)

		return wrapper_refresh

	@property
	def headers(self) -> Dict[str, str]:
		return {
			"Authorization": f"Bearer {self.token}",
		}

	@refresh_token
	def get_courses_list(
		self,
		page: int = None,
		per_page: int = None,
		types: Optional[list] = None,
	) -> List[dict]:
		path: str = "courses/"
		url = self.base_url + self.api_endpoint + path
		if page is not None:
			url += f"?page={page}"

		if per_page is not None:
			url += f"&per_page={per_page}"

		if types is not None:
			for i in range(len(types)):
				url += f"&types%5B%5D={types[i]}"

		response = requests.get(
				url=url,
				headers=self.headers,
		)
		return response.json()

	@refresh_token
	def get_course_detail(self, pk: int = 55894) -> Dict[str, Union[str, int]]:
		path: str = "courses/"
		url = self.base_url + self.api_endpoint + path + f"{pk}"

		response = requests.get(
				url=url,
				headers=self.headers,
		)
		return response.json()

	@refresh_token
	def create_user(self, json: dict) -> Dict[str, Union[str, int, dict]]:
		path: str = "users/create"
		url = self.base_url + self.api_endpoint + path
		headers = {
			"Content-Type": "application/json",
		}
		headers.update(self.headers)

		response = requests.post(
				json=json,
				url=url,
				headers=headers,
		)
		return response.json()

	@refresh_token
	def register_user_for_session(self, json: dict, session_pk: int = 495682):
		"""
		:param json: {
						"email": "email_1_2@factory.tb",
						"phone": 792177788666,
						"user_id": 334
					}
		"""

		path = f"course_sessions/{session_pk}/register"
		url = self.base_url + self.api_endpoint + path
		headers = {
			"Content-Type": "application/json",
		}
		headers.update(self.headers)

		response = requests.post(
				json=json,
				url=url,
				headers=headers,
		)
		return response.json()

	@refresh_token
	def get_courses_sessions_list(
		self,
		course_pk: int = 55894,
		session_status: str = "active",
		page: int = None,
		per_page: int = None,
		participant_ids: List[int] = None,
	):
		path = f"courses/{course_pk}/course_sessions"
		url = self.base_url + self.api_endpoint + path + f"?filter={session_status}"

		if page is not None:
			url += f"&page={page}"

		if per_page is not None:
			url += f"&per_page={per_page}"

		if participant_ids is not None:
			for i in range(len(participant_ids)):
				url += f"&participant_ids%5B%5D={participant_ids[i]}"

		response = requests.get(
				url=url,
				headers=self.headers,
		)
		return response.json()


#####################################################################
usr = {
	"users":           [
		{
			"email":       "test@teachbase.ru",
			"name":        "John",
			"description": "Corrupti natus quia recusandae.",
			"last_name":   "Doe",
			"phone":       "string",
			"role_id":     1,
			"auth_type":   0,
			"external_id": "u-0007",
			"labels":      {"1": "2", "3": "4"},
			"password":    "qwerty",
			"lang":        "ru",
		}
	],
	"external_labels": True,
	"options":         {
		"activate":                 True,
		"verify_emails":            True,
		"skip_notify_new_users":    True,
		"skip_notify_active_users": True,
	},
}
#
a = TeachbaseClient(client_id=key, client_secret=secret, base_url=bas_url)
# a.authentication()

get_course_list = a.register_user_for_session(json={
						"email": "email_1_2@factory.tb",
						"phone": 792177788666,
						"user_id": 334
					})

print(get_course_list)
