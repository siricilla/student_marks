from django.shortcuts import render
from django.urls.conf import path
from rest_framework.views import APIView
from rest_framework.response import Response
from markscal.models import Marks
from markscal.serializers import StudentMarkSerializer, TotalMarkSerializer, SubjectAvgMarkSerializer
from django.db.models import Sum, Avg


class MarksView(APIView):
    def post(self, request):
        post_data = request.data
        for item in post_data["subject"]:
            Marks.objects.create(
                student=post_data["student"],
                subject=item,
                marks=post_data["subject"][item],
            )
        data = {
            "status": 201,
            "message": "student Marks created successfully",
            "data": request.data,
        }

        return Response(data=data)

    def get(self, request, id=None):
        try:
            if id:
                stu_marks = Marks.objects.get(id=id)
                serializer = StudentMarkSerializer(stu_marks)
                data = serializer.data
                return Response(data={"status": 200, "message": "Student data based on id  retrieved successfully", "data": data})
            else:
                stu_marks = Marks.objects.all()
                serializer = StudentMarkSerializer(stu_marks, many=True)
                data = get_distinct_data(serializer.data)
                return Response(data={"status": 200, "message": "Student  total data retrieved successfully", "data": data})
        except Marks.DoesNotExist:
            return Response(data={"status": 404, "message": "Student Not Found", "data": {}})

def get_distinct_data(serializer_data):
    data = []
    for item in serializer_data:
        if item not in data:
            data.append(item)
    return data

class TotalMarksView(APIView):
    def get(self, request):
        stu = Marks.objects.all()
        total_marks = TotalMarkSerializer(stu, many=True)
        data = get_distinct_data(total_marks.data)
        return Response(data={"status": 200, "message": "Student total marks.", "data": data})


class AvgMarksView(APIView):
    def get(self, request):
        stu = Marks.objects.all().values("subject")
        subjects = []
        for sub in stu:
            if sub["subject"] not in subjects:
                subjects.append(sub["subject"])
        context = {"subjects": subjects}
        avg = SubjectAvgMarkSerializer(sub, many=True, context=context)
        data = get_distinct_data(avg.data)
        return Response(data={"status": 200, "message": "Subject average marks.", "data": data[0]["avg_marks"]})
