import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

NAV_LINKS = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
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
        {"name": "Business Case Competitions", "image": "img/hobbies/business-case-competitions.jpeg"},
    ]
    return render_template('hobbies.html', title="Hobbies", hobbies=hobby_cards, url=os.getenv("URL"))
