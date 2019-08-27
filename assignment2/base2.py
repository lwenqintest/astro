import requests
import uuid
import json
import unittest


BASEURL = "https://beta.todoist.com/API/v8/projects"
TOKEN = "023e271f88e1c440664ad016647a7bceee627eaf"
GET_HEADERS = {"Authorization": "Bearer %s" % TOKEN}
POST_HEADERS = {"Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % TOKEN
                }

class Todoist(unittest.TestCase):
    project_data = {"name": "NewProject"}

    def test_create_project(self):
        r = requests.post(BASEURL, data=json.dumps(self.project_data), headers=POST_HEADERS)
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()