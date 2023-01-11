import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from build_latex import make_document

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

business_info = [
            'Hiring Manager',
            'Company',
            'Street Address',
            'City and ZIP'
        ]


@app.route("/", methods=("GET", "POST"))
def index():
    global business_info
    if request.method == "POST":
        cover = request.form["cover"]
        job = request.form["job"]
        business_info = [
            request.form["recipient"],
            request.form["company"],
            request.form["address"],
            request.form["city"]
        ]
        allowable_response_length = 4096 - len(cover)/4 - len(job)/4
        print(allowable_response_length)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(cover, job),
            temperature= 0.9,
            max_tokens=int(allowable_response_length),
        )
        print(response.choices)
        print(response.choices[0])
        return redirect(url_for("index", result=response.choices[0].text.strip('Dear Hiring Manager')))

    result = request.args.get("result")
    return render_template("index.html", result=result)

@app.route("/generate_latex", methods=("GET", "POST"))
def generate_latex():
    if request.method == "POST":
        completion = request.form["completion"]
        personal_info = [
            '1525 Griffith Park Blvd, Apt. 107',
            'Los Angeles, CA 90026',
            '(707) 913-7014',
            'abel.e.romer@gmail.com',
            'https://www.abelromer.com'
        ]
        global business_info
        print(completion)
        make_document(personal_info, business_info, completion)
        path = '/static/cover.pdf'
    return render_template("index.html", pdf_filepath=path)


def generate_prompt(cover, job):
    prompt = f"Re-write the following cover letter using keywords from this job description: \n\nCover letter: {cover} \n\nJob description: {job}."
    return prompt
