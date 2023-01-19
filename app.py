import os
import openai
from flask import Flask, redirect, render_template, request, url_for
from build_latex import make_document

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


def merge_lists(a, b):
    result = []
    for pair in zip(a, b):
        if pair[0].strip() == "":
            result.append(pair[1])
        else:
            result.append(pair[0])
    return result

@app.route("/", methods=("GET", "POST"))
def index():
    print("Redirected")
    print(request.args)
    print(request.args.getlist('personal_info'))
    if request.method == "POST":
        cover = request.form["cover"]
        job = request.form["job"]
        allowable_response_length = 4096 - len(cover)/4 - len(job)/4
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(cover, job),
            temperature= 0.9,
            max_tokens=int(allowable_response_length),
        )

        submitted = True
        result = response.choices[0].text.strip('Dear Hiring Manager')
        #print(result)
        return redirect(url_for("index",
                                result=result,
                                submitted=submitted,
                                cover=cover,
                                job=job
                        ))
    print("rendering template...")
    return render_template("index.html",
                           submitted=request.args.get("submitted"),
                           result=request.args.get("result"),
                           business=request.args.getlist("business_info"),
                           personal=request.args.getlist("personal_info"),
                           cover=request.args.get("cover"),
                           job=request.args.get("job"),
                           pdf_filepath=request.args.get("pdf_filepath"))

@app.route("/generate_latex", methods=("GET", "POST"))
def generate_latex():
    if request.method == "POST":
        print("POST")
        personal_info = [
            'Name',
            'Street Address',
            'City and ZIP',
            'Phone',
            'Email',
            'Website'
        ]
        business_info = [
            'Hiring Manager',
            'Company',
            'Street Address',
            'City and ZIP'
        ]
        print("Still in generate_latex...")
        data = request.get_json()
        print("DATA POSTED")

        business_info_form = data["business_info"]
        personal_info_form = data["personal_info"]
        business_info = merge_lists(business_info_form, business_info)
        personal_info = merge_lists(personal_info_form, personal_info)
        completion = data["completion"]
        job = data["job"]
        cover = data["cover"]

        make_document(personal_info, business_info, completion)
        pdf_filepath = '/static/cover.pdf'
        submitted = True
        print(personal_info)
        return redirect(url_for("index",
                                submitted=submitted,
                                result=completion,
                                personal_info=personal_info,
                                business_info=business_info,
                                job=job,
                                cover=cover,
                                pdf_filepath=pdf_filepath))
    print("NOT POST")
    return redirect(url_for("index"))


def generate_prompt(cover, job):
    prompt = f"Re-write the following cover letter using keywords from this job description: \n\nCover letter: {cover} \n\nJob description: {job}."
    return prompt
