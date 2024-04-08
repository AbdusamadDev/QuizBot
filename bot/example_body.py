"""
Request:
    {
        "fullname": "john doe",
        "group": "12B group"
    }
Response:
    {
        "id": 5,
        "questions": [
            {
                "id": 1,
                "created_at": "2024-04-08T05:11:42.588264Z",
                "updated_at": "2024-04-08T05:11:42.588264Z",
                "title": "sdbvjhagsdhjfghjjlhgjhjkhkjlhgsadfasdfawfdf",
                "option_1": "asdfasadsf",
                "option_2": "dfsaasdf",
                "option_3": "asdfsdaf",
                "option_4": "asdfsdfdf",
                "answer": 4,
                "quiz": 7
            },
            {
                "id": 2,
                "created_at": "2024-04-08T05:14:59.405720Z",
                "updated_at": "2024-04-08T05:14:59.405720Z",
                "title": "sdbvjhagsdhjfghjjlhgjhjkhkjlhgsadfasdfawfdf",
                "option_1": "asdfasadsf",
                "option_2": "dfsaasdf",
                "option_3": "asdfsdaf",
                "option_4": "asdfsdfdf",
                "answer": 4,
                "quiz": 7
            }
        ],
        "uuid": "b009c85c-02f3-4759-8ee7-0eb3bf522469",
        "student_fullname": "Abdusamad",
        "student_group": "12b Group",
        "begin_date": "2024-04-08T10:15:05.019199Z",
        "end_date": "2024-04-07T15:56:11.856795Z",
        "solving_time": 0,
        "status": false,
        "created_at": "2024-04-08T05:15:05.023004Z",
        "answers": null,
        "quiz": 7
    }
"""

"""
Request:
    {
        "answers": [
            {
                "qid": 1,
                "ans": 2
            },
            {
                "qid": 2,
                "ans": 4
            }
        ]
    }        
Response:
    {
        "id": 1,
        "uuid": "dcfc61db-a275-433d-aaad-2d3b22514dd0",
        "score": 50.0,
        "created_at": "2024-04-08T05:21:09.919785Z",
        "exam": 5,
    }
"""
