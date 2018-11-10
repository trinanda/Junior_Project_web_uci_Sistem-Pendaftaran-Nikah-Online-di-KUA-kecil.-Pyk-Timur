# https://pypi.org/project/Flask-CSV/

from flask import Flask
from flask_csv import send_csv
from marshmallow import Schema, fields

app = Flask(__name__)


class IdSchema(Schema):
    city_id = fields.Integer()

@app.route('/')
def index():
    name_CL_to_CSV = []
    name_CL = ['Lolo', 'Fadli', 'Jori', 'Andi', 'Budi', 'Dedi', 'Nori']
    for i in name_CL:
        name_CL_to_CSV.append(i)

    return send_csv([{'Nama Catin Laki-laki' : name_CL_to_CSV}],
            "testing.csv", ['Nama Catin Laki-laki'], cache_timeout=1, delimiter=';')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




# https://stackoverflow.com/questions/30024948/flask-download-a-csv-file-on-clicking-a-button?lq=1
# from flask import Flask, Response
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return '''
#         <html><body>
#         Hello. <a href="/getPlotCSV">Click me.</a>
#         </body></html>
#         '''
#
# @app.route("/getPlotCSV")
# def getPlotCSV():
#     # with open("outputs/Adjacency.csv") as fp:
#     #     csv = fp.read()
#     csv = '1,2,3\n4,5,6\n'
#     return Response(
#         csv,
#         mimetype="text/csv",
#         headers={"Content-disposition":
#                  "attachment; filename=myplot.csv"})
#
#


# @app.route('/')
# def index():
#     name_CL_to_CSV = []
#     name_CL = ['Lolo', 'Fadli', 'Jori', 'Andi', 'Budi', 'Dedi', 'Nori']
#     for i in name_CL:
#         # name_CL_to_CSV.append(i)
#         name_CL_to_CSV.append({'Name CL' : i})
#
#     return send_csv(name_CL_to_CSV,
#                     "testing.csv", ['Name CL'], cache_timeout=1, delimiter=';')


