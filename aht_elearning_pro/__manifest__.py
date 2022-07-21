# -*- coding: utf-8 -*-
{
    'name': 'elearning Pro',
    'version': '1.1',
    'summary': 'elearning Pro',
    'sequence': -10,
    'description': """elearning Pro""",
    'category': 'Website/eLearning',
    'author': "Alhaditech",
    'price': 120, 'currency': 'USD',
    'website': "https://www.alhaditech.com/",
    'depends': ['website_slides','virtual_meeting','slide_local_video'],
    'data': [
        'views/publish_button.xml',
        'views/slide_custom_view_inherit.xml',
        'static/src/xml/website_image.xml',
        'views/elearning_teachers.xml',
        'security/teacher_group.xml',
        'views/teachers_menu_item.xml',
        'views/elearning_home.xml',
    ],
    'images': ['static/description/cover_image.jpeg'],
    'demo': [],
    'assets': {
        'web.assets_frontend_lazy':
            [
                'aht_elearning_pro/static/src/js/fullscreen.js',
            ],
        'web.assets_frontend': [
            'aht_elearning_pro/static/src/css/teachers_registration.css',
            'aht_elearning_pro/static/src/css/style.css',
            'aht_elearning_pro/static/src/js/teachers_registration.js',
            'aht_elearning_pro/static/src/js/main.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
