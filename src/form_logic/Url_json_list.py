class url_and_json_info():
    # Url list need in other class

    #登录时需要请求的URL
    login_request_url = "https://moodle.nottingham.ac.uk/login/index.php"
    # 主页的URL
    home_page_url = "https://moodle.nottingham.ac.uk/my/"
    # 退出登录需要请求的URL
    log_out_request_url = "https://moodle.nottingham.ac.uk/login/logout.php?sesskey="
    # 下载文件夹需要请求的URL
    folder_download_request_url = "https://moodle.nottingham.ac.uk/mod/folder/download_folder.php"
    # 请求打印全部课程的目标URL
    course_list_request_url_1 = "https://moodle.nottingham.ac.uk/lib/ajax/service.php?sesskey="
    course_list_request_url_2 = "&info=core_course_get_enrolled_courses_by_timeline_classification"


    # Json list need in other class

    # 请求打印全部课程的json
    all_course_list_json = [{"index": 0, "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                             "args": {"offset": 0, "limit": 0, "classification": "all", "sort": "fullname",
                                      "customfieldname": "", "customfieldvalue": ""}}]
    # 请求打印加星星的课程的json
    stared_course_list_json = [{"index": 0, "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
                                "args": {"offset": 0, "limit": 0, "classification": "favourites", "sort": "fullname",
                                         "customfieldname": "", "customfieldvalue": ""}}]


