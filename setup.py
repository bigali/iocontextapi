from setuptools import setup

setup(name='FlaskApp',
      version='1.0',
      description='A basic Flask app with static files',
      author='Ryan Jarvinen',
      author_email='ryanj@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['flask', 'tweepy', 'py2neo', 'requests',
                        'Jinja2',
                        'MarkupSafe',
                        'SQLAlchemy',
                        'Werkzeug',
                        'itsdangerous',
                        'PyJWT',
                        'requests-oauthlib',
                        'facebook-sdk'
      ],
)
