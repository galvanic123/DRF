from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('title', 'description', 'lessons', 'lesson_count')
