from common.djangoapps.student.models import CourseEnrollment, User

class EnrollmentsService(object):
    def get_enrollments_by_course(self, course_id):
        return CourseEnrollment.objects.filter(course_id=course_id)