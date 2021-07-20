from django.db import models
from django.db.models import fields
from django.db.models.aggregates import Sum, Avg
from rest_framework import serializers
from markscal.models import Marks


class StudentMarkSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Marks
        fields = ["student", "subject"]

    def get_subject(self, obj):
        data = {}
        marks_obj = Marks.objects.filter(student=obj.student)
        for sub_marks in marks_obj:
            data.update({sub_marks.subject: sub_marks.marks})
        return data


class TotalMarkSerializer(serializers.ModelSerializer):
    total_marks = serializers.SerializerMethodField()

    class Meta:
        model = Marks
        fields = ["student", "total_marks"]

    def get_total_marks(self, obj):
        mark = Marks.objects.filter(student=obj.student).aggregate(Sum("marks"))
        return mark["marks__sum"]


class SubjectAvgMarkSerializer(serializers.ModelSerializer):
    avg_marks = serializers.SerializerMethodField()

    class Meta:
        model = Marks
        fields = ["avg_marks"]

    def get_avg_marks(self, obj):
        subjects = self.context["subjects"]
        sub_obj = Marks.objects.filter(subject__in=subjects)
        res = {}
        for sub in sub_obj:
            avg = Marks.objects.filter(subject=sub.subject).aggregate(Avg("marks"))
            res.update({sub.subject: avg["marks__avg"]})
        return res
