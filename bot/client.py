import requests
import json

from conf import TEST_URL


def create_exam(fullname, group, uuid=None):
    request = requests.post(
        f"{TEST_URL}/api/exam/{uuid}/",
        data={"student_fullname": fullname, "student_group": group},
    )
    if request.status_code == 201:
        response = json.loads(request.content)
        return response

    return {}


def submit_exam(answers, exam_uuid):
    url = f"{TEST_URL}/api/exam/check/{exam_uuid}/"
    request = requests.post(url=url, json={"answers": answers})
    print("Data: ", {"answers": answers})
    if request.status_code == 201:
        response = request.json()
        return response
    else:
        print(request.content)
        return {}


if __name__ == "__main__":
    print(create_exam("men", "sadhalsjdfk"))
