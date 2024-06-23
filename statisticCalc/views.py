from django.http import HttpResponse
from django.http import FileResponse
import datetime
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.

test_data = pd.DataFrame({
  "li": [1.000, 3.000, 5.000, 7.000, 9.000],
  "ls": [3.000, 5.000, 7.000, 9.000, 11.000],
  "x": [2.000, 4.000, 6.000, 8.000, 10.000],
  "fi": [4.000, 5.000, 6.000, 2.000, 1.000],
  "Fi": [4, 9, 15, 17, 18],
  "fr": [0.222, 0.278, 0.333, 0.111, 0.056],
  "Fr": [0.222, 0.500, 0.833, 0.944, 1.000],
  "fp": [22.222, 27.778, 33.333, 11.111, 5.556],
  "Fp": [22.2, 50.000, 83.333, 94.444, 100.000],
  "Medidas de tendencia central": [None, None, None, None, None],
  "Media": [5, None, None, None, None],
  "Mediana": [5, None, None, None, None],
  "Moda": [5, None, None, None, None]
})

@csrf_exempt
def controller_generate_excel(request):

  if(request.method == "POST"):
    json_data = json.loads(request.body)

    if(json_data == {}):
      data = { "msg": "No hay datos para generar su archivo" }
      response = HttpResponse(json.dumps(data))
      response.status_code = 400
      return response

    try:
      df = pd.DataFrame({
        "Informacion Básica": json_data["BI"],
        "Ancho de clase": json_data["anchoClase"],
        "min": json_data["numMin"],
        "max": json_data["numMax"],
        "rango": json_data["rango"],
        "li": json_data["li"],
        "ls": json_data["ls"],
        "x": json_data["x"],
        "fi": json_data["fi"],
        "Fi": json_data["Fi"],
        "fr": json_data["fr"],
        "Fr": json_data["Fr"],
        "fp": json_data["fp"],
        "Fp": json_data["Fp"],
        "Medidas de tendencia central": json_data["MCT"],
        "Media": json_data["media"],
        "Mediana": json_data["mediana"],
        "Moda": json_data["moda"]
      })
    except KeyError as KE:
      data = { "msg": f"Falta informacion para generar el archivo{KE}" }
      response = HttpResponse(json.dumps(data))
      response.status_code = 400
      return response


    if(not(os.path.exists("./statisticCalc/excel-files"))):
      os.mkdir("./statisticCalc/excel-files")
      print("directorio creado")

    time = datetime.datetime.now().timestamp()

    file_name = f"calculos{time}"

    df.to_excel(excel_writer=f"./statisticCalc/excel-files/{file_name}.xlsx", sheet_name="calculos")
    response = HttpResponse(json.dumps({ "msg": "archivo creado con exito", "file_name": file_name }))
    response.status_code = 201
    return response
  else:
    response = HttpResponse(json.dumps({"msg": f"No hay accion para este metodo: {request.method}"}))
    response.status_code = 400
    return response

def get_file(request):
  file_name = request.GET["file_name"]
  if(not(os.path.exists(f"./statisticCalc/excel-files/{file_name}.xlsx"))):
    response = HttpResponse(json.dumps({"msg": f"No existe el archivo {file_name}"}))
    response.status_code = 404
    return response

  return FileResponse(open(f"./statisticCalc/excel-files/{file_name}.xlsx", "rb"), as_attachment=True, filename=f"calculos{file_name}.xlsx")
