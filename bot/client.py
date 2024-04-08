import requests
import json

from conf import TEST_URL


def create_exam(fullname, group, uuid=None):
    uuid = "a583559a-c3ea-42f9-949e-1fedcdc5fc53"
    request = requests.post(
        f"{TEST_URL}/api/exam/{uuid}/",
        data={"student_fullname": fullname, "student_group": group},
    )
    if request.status_code == 201:
        response = json.loads(request.content)
        return response
    return {}


def submit_exam():
    pass


if __name__ == "__main__":
    print(create_exam("men", "sadhalsjdfk"))
