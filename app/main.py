import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from logging.config import dictConfig
# Data Science libraries
import pandas as pd
import numpy as np
import pickle

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = flask.Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route('/api/v1/', methods=['POST'])
def prediction():
   loaded_model = pickle.load(open('app/model_adaboostclassifier.sav', 'rb'))
   df = pd.DataFrame(data=request.json["body"])
   df.drop(['key','name','prediction'], axis=1, inplace=True)
   df = df.astype(float)
   df['i_vul'] = (df['alums_pref'] + df['alums_prior']) / df['alumns_class']
   df.drop(['alums_pref','alums_prior','alumns_class'],axis=1,inplace=True)
   list_atributos_dummies = ['cod_pro_rbd', 'cod_depe2', 'cod_ense', 'cod_jor', 'cod_des_cur', 'gen_alu']
   for category in list_atributos_dummies:
      df_dummy = pd.get_dummies(data=df[category], drop_first=True, prefix=category)
      df = df.join(df_dummy)
      df.drop(columns=category, inplace=True)
   dummies_columns = ['average_psu', 'average_nem', 'prom_notas_alu', 'rural_rbd', 'edad_alu',
         'i_vul', 'cod_pro_rbd_14', 'cod_pro_rbd_21', 'cod_pro_rbd_22',
         'cod_pro_rbd_23', 'cod_pro_rbd_31', 'cod_pro_rbd_32', 'cod_pro_rbd_33',
         'cod_pro_rbd_41', 'cod_pro_rbd_42', 'cod_pro_rbd_43', 'cod_pro_rbd_51',
         'cod_pro_rbd_52', 'cod_pro_rbd_53', 'cod_pro_rbd_54', 'cod_pro_rbd_55',
         'cod_pro_rbd_56', 'cod_pro_rbd_57', 'cod_pro_rbd_58', 'cod_pro_rbd_61',
         'cod_pro_rbd_62', 'cod_pro_rbd_63', 'cod_pro_rbd_71', 'cod_pro_rbd_72',
         'cod_pro_rbd_73', 'cod_pro_rbd_74', 'cod_pro_rbd_81', 'cod_pro_rbd_82',
         'cod_pro_rbd_83', 'cod_pro_rbd_84', 'cod_pro_rbd_91', 'cod   _pro_rbd_92',
         'cod_pro_rbd_101', 'cod_pro_rbd_102', 'cod_pro_rbd_103',
         'cod_pro_rbd_104', 'cod_pro_rbd_111', 'cod_pro_rbd_112',
         'cod_pro_rbd_113', 'cod_pro_rbd_114', 'cod_pro_rbd_121',
         'cod_pro_rbd_122', 'cod_pro_rbd_123', 'cod_pro_rbd_124',
         'cod_pro_rbd_131', 'cod_pro_rbd_132', 'cod_pro_rbd_133',
         'cod_pro_rbd_134', 'cod_pro_rbd_135', 'cod_pro_rbd_136',
         'cod_pro_rbd_141', 'cod_pro_rbd_142', 'cod_pro_rbd_151',
         'cod_pro_rbd_152', 'cod_depe2_2', 'cod_depe2_3', 'cod_depe2_4',
         'cod_ense_310', 'cod_ense_363', 'cod_ense_410', 'cod_ense_463',
         'cod_ense_510', 'cod_ense_563', 'cod_ense_610', 'cod_ense_663',
         'cod_ense_710', 'cod_ense_763', 'cod_ense_810', 'cod_ense_863',
         'cod_ense_910', 'cod_jor_2', 'cod_jor_3', 'cod_jor_4', 'cod_des_cur_1',
         'cod_des_cur_2', 'cod_des_cur_3', 'gen_alu_2']
   df_reindex = df.reindex(columns = dummies_columns, fill_value=0)
   response = jsonify(list(loaded_model.predict(df_reindex)))
   app.logger.info('%s respuesta generada', response)
   response.headers.add("Access-Control-Allow-Origin", "*")
   return(response)



@app.route('/api/v1/', methods=['GET'])
def instructions():
   response = jsonify({
      "average_psu": "Tipo numérico, nota obtenida del PSU.",
		"average_nem": "Tipo numérico, nota promedia obtenida en media.",
		"prom_notas_alu": "Tipo numérico, nota final obtenida en cuato de medio.",
		"cod_pro_rbd": "Tipo numérico, código de la provincia (ver excel de la app web)",
		"cod_depe2": "Tipo numérico, código de dependencia del establecimiento (2: Particular Subvencionado , 3: Particular Pagado , 4: Corporación de Administración Delegada)",
		"rural_rbd": "Tipo numérico, índice de ruralidad (urbano 0, rural 1).",
		"cod_ense": "Tipo numérico, código de enseñanza (ver excel de la app web).",
		"cod_jor": "Tipo numérico, tipo de jornada (1: Mañana, 2: Tarde, 3: Mañana y tarde, 4: Vespertina / Nocturna).",
		"cod_des_cur": "Tipo numérico, descripción del curso (1: Sólo Liceo, 2: Dual, 3: Otro).",
		"gen_alu": "Tipo numérico, sexo (0: Sin Información, 1: Hombre, 2: Mujer).",
		"edad_alu": "Tipo numérico, edad del alumno.",
		"alums_pref": "Tipo numérico, cantidad de alumnos preferenciales en el aula.",
		"alums_prior": "Tipo numérico, cantidad de alumnos prioritarias en el aula.",
        "alumns_class": "Tipo numérico, cantidad de alumnos total en el aula",
        "key": "Tipo numérico, id único del alumno",
        "name": "Tipo texto, nombre del alumno (en que caso de no proporcionar dejar vacío)",
        "prediction": "Tipo numérico, dejar vacío"
   })
   response.headers.add("Access-Control-Allow-Origin", "*")
   return(response)