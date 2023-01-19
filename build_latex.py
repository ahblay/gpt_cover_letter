from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
from pylatex.base_classes import Environment, Arguments, Options
from pylatex.package import Package


def teletype(text):
    return NoEscape(r'\texttt{' + text + '}')

def make_document(personal_info, business_info, content):
    class Letter(Environment):
        packages = []

    name, street, city, phone, email, website = personal_info
    recipient, company, business_street, city_zip = business_info

    doc = Document(documentclass="letter")

    with doc.create(Letter(arguments=Arguments(NoEscape(rf'{recipient} \\ {company} \\ {business_street} \\ {city_zip}')))):
        doc.append(NoEscape('\opening{Dear Hiring Manager:}'))
        doc.append(NoEscape(content))
        doc.append(Command('closing', 'Sincerely,'))
        doc.append(Command('encl', 'Resume'))

    doc.preamble.append(Command('signature', NoEscape(rf'{name}')))
    doc.preamble.append(Command('address', NoEscape(rf'{street} \\ {city} \\ {phone} \\ {teletype(email)} \\ {teletype(website)}')))

    doc.packages.append(Package('geometry',
                                Options(left='1.5in',
                                        right='1.5in',
                                        top='1.25in',
                                        bottom='1.25in')))

    doc.generate_pdf('/Users/abel/documents/programming/gpt_cover_letter/static/cover', clean_tex=False)
