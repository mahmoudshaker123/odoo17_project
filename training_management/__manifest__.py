
{
    'name': "Traning Management",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/training_instructor_view.xml',
        'views/training_course_view.xml',
        'views/training_student_view.xml',
        'views/training_attendance_view.xml',
        'reports/student_report.xml',
        'reports/attendance_course_report.xml',

],

    'application': True,
}
