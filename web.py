#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 13:04:27 2021

@author: aly
"""
from owlready2 import *
#from rdflib import *
import json
import rdflib
from flask_cors import CORS

# onto = get_ontology("estilosR.owl").load()  ontologia vieja
onto = get_ontology("Estilos_de_Aprendizaje.owl").load()
graph = default_world.as_rdflib_graph()

g = rdflib.Graph()
g.parse("Estilos_de_Aprendizaje.owl")


from flask import Flask, request

app = Flask(__name__)
CORS(app)
@app.route('/')
def ontology_page():
    html  = """<html><body>"""
    html += """<h2>Consultas disponibles</h2>""" 
    html += """<h2>'%s' ontology</h2>""" % onto.base_iri
    html += """<h3>Root classes</h3>"""
    for Class in Thing.subclasses():
        html += """<p>>%s</p>""" % Class.name
        html += """<p>>%s</p>""" % len(g)
   
    
    html += """<div>
                <p>Seleccione su consulta:</p>
  <form action="/result">
    <input type="radio" id="1" name="c" value="1">
  <label for="1">Consulta 1</label><br>
  <input type="radio" id="2" name="c" value="2">
  <label for="2">Consulta 2</label><br>
  <input type="radio" id="3" name="c" value="3">
  <label for="3">Consulta 3 Saludos hola</label>
  </p>
<p><input type="submit"></p>
    </form>
    </div>""" 
    
    return html

@app.route('/result')
def consulta():
  consul = request.args.get("c"," ")
  ruta = []
  html = ""
  #sync_reasoner_hermit()
    
  if consul == "1" :
       # html = """<p>>%s</p>""" % onto.Mat_Vis_Glo_M.instances()
        qres = g.query("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX  :<http://www.semanticweb.org/miguelangel/ontologies/2022/estilos#>
        SELECT   ?x WHERE { 
          ?x :se_identifica_con_e_a  :visual_secuencial_apropiado.
          ?x :formato  ?y.  
          ?x :nivel ?w.  
        }""")
        unique_category = []
        for row in qres:
           category = ("%s" % row).rsplit('/',1)[-1]
           unique_category.append(category)
        #archivo = json.dumps(unique_category)
        #html = archivo
	
       #for x in range(0,len(d)):
        #    st = str(d[x])
            #st = st[1:-1]
         #   ruta.append(st)
       #archivo = json.dumps(d)
       #html = "hola"
            
       
  else:
     if consul == "2" :
        html = """<p>>%s</p>""" % onto.Persona_Estilo_Verbal_Global_Fuerte.instances()
     else:
         d = (list(graph.query_owlready("""
                              PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                              PREFIX owl: <http://www.w3.org/2002/07/owl#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                              PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                              PREFIX  :<http://www.semanticweb.org/miguelangel/ontologies/2022/estilos#>
                              SELECT distinct ?a WHERE {
                                  ?a estilo:se_relaciona_con estilo:verbal_secuencial_fuerte.
                                       }""")))
         
         
         for x in range(0,len(d)):
            st = str(d[x])
            st = st[1:-1]
            ruta.append(st)
         # str(d[x]) html += """<br>>%s</br>""" % str(d[x])
         archivo = json.dumps(ruta)
         html = archivo
    
  return html
           
  
  #  sync_reasoner_hermit()
  #  html = """<p>>%s</p>""" % onto.Mat_Vis_Glo_M.instances()


#import werkzeug.serving
#werkzeug.serving.run_simple("localhost", 5000, app)
port=os.environ["PORT"]
app.run('0.0.0.0',port, debug=True)
