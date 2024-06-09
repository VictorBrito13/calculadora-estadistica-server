from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
import os
from wsgiref.util import FileWrapper
import chardet

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

# print("ruta absoluta", os.path.join(os.path.abspath(__file__)))

@csrf_exempt
def controller_generate_excel(request):
  if(request.method == "POST"):
    json_data = json.loads(request.body)
    print(json_data)
    df = pd.DataFrame({
      "li": json_data["data"]["li"],
      "ls": json_data["data"]["ls"],
      "x": json_data["data"]["x"],
      "fi": json_data["data"]["fi"],
      "Fi": json_data["data"]["Fi"],
      "fr": json_data["data"]["fr"],
      "Fr": json_data["data"]["Fr"],
      "fp": json_data["data"]["fp"],
      "Fp": json_data["data"]["Fp"],
      "Medidas de tendencia central": ["", "", "", "", ""],
      "Media": json_data["data"]["media"],
      "Mediana": json_data["data"]["mediana"],
      "Moda": json_data["data"]["moda"]
    })

    if(not(os.path.exists("./statisticCalc/excel-files"))):
      os.mkdir("./statisticCalc/excel-files")
      print("directorio creado")

    df.to_excel(excel_writer="./statisticCalc/excel-files/calculos.xlsx", sheet_name="calculos")
    return HttpResponse("exito en la subida de archivos calculos.xlsx")

def get_file(request):
  return FileResponse(open("./statisticCalc/excel-files/calculos.xlsx", "rb"), as_attachment=True, filename="calculosas.xlsx")
