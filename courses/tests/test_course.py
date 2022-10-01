from django.urls import reverse

from courses import models


def test_create_course_with_login_user(logged_user, client, subject, image):
    url = reverse('courses:course-create')

    course_data = {
        'title': 'HTML ninja',
        'overview': 'Example overview',
        'slug': '',
        'subject': '1',
        'course_image': image
    }

    response = client.post(url, data=course_data)
    course = models.Course.objects.first()

    assert response.status_code == 302
    assert course.title == course_data['title']