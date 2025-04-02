from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from django.views import View
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from rest_framework.response import Response
from rest_framework import status

from schedules.models import Schedule, Tag, TimeTable
from schedules.serializers import ScheduleSerializer
from users.utils import (
    check_error,
    get_courses,
    get_events,
    get_syllabus,
    login_attempt,
    save_to_timetable,
)


# 학번, 비밀번호 유효성 검사
class StudentInfoCheckView(APIView):
    def post(self, request):
        student_id = request.data.get("student_id")
        student_password = request.data.get("student_password")

        driver = webdriver.Chrome()
        # ecampus login
        login_attempt(driver, student_id, student_password)
        if check_error(driver):
            driver.quit()
            return Response(
                {"message": "로그인 실패: 학번 또는 비밀번호가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            driver.quit()
            return Response(
                {"message": "올바른 학번, 비밀번호 입니다."}, status=status.HTTP_200_OK
            )
