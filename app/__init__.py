import os
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         password=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306,
                         )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

NAV_LINKS = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
    {"name": "Timeline", "endpoint": "timeline"},
]

EDUCATION = [
    {
        "school": "NYU Tandon School of Engineering",
        "degree": "B.S. in Computer Science",
        "date": "Expected May 2027",
        "details": ["Minors in Mathematics and Cybersecurity"],
    },
]

EXPERIENCES = [
    {
        "role": "MLH Fellow",
        "organization": "Major League Hacking Fellowship",
        "date": "June 2026 – August 2026",
    },
    {
        "role": "Data Structures Teaching Assistant",
        "organization": "NYU Tandon School of Engineering",
        "date": "September 2024 – May 2026",
    },
]


@app.context_processor
def inject_nav_links():
    return {"nav_links": NAV_LINKS}


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        education=EDUCATION,
        experiences=EXPERIENCES,
        url=os.getenv("URL"),
    )


@app.route('/hobbies')
def hobbies():
    hobby_cards = [
        {"name": "Traveling", "image": "img/hobbies/traveling.jpeg"},
        {"name": "Boxing", "image": "img/hobbies/boxing.jpeg"},
        {"name": "Business Case Competitions",
            "image": "img/hobbies/business-case-competitions.jpeg"},
    ]
    return render_template('hobbies.html', title="Hobbies", hobbies=hobby_cards, url=os.getenv("URL"))


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name or name.strip() == '':
        return "Invalid name", 400

    if not content or content.strip() == '':
        return "Invalid content", 400

    if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(
        name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p) for p in TimelinePost.select().
            order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)
    if post is None:
        return {'error': 'Timeline post not found'}, 404

    post.delete_instance()
    return {'deleted': post_id}
