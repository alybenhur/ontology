#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 13:04:27 2021

@author: aly
"""
from owlready2 import *
from rdflib import *

onto = get_ontology("estilosR.owl").load()
graph = default_world.as_rdflib_graph()

from flask import Flask, request

app = Flask(__name__)
@app.route('/')
def ontology_page():
    html  = """<html><body>"""
    html += """<h2>Consultas disponibles</h2>""" 
    html += """<h2>'%s' ontology</h2>""" % onto.base_iri
    html += """<h3>Root classes</h3>"""
    for Class in Thing.subclasses():
        html += """<p>>%s</p>""" % Class.name
    
    
    html += """<div>
                <p>Seleccione su consulta:</p>
  <form action="/result">
    <input type="radio" id="1" name="c" value="1">
  <label for="1">Consulta 1</label><br>
  <input type="radio" id="2" name="c" value="2">
  <label for="2">Consulta 2</label><br>
  <input type="radio" id="3" name="c" value="3">
  <label for="3">Consulta 3</label>
  </p>
<p><input type="submit"></p>
    </form>
    </div>""" 
    
    return html

@app.route('/result')
def consulta():
  consul = request.args.get("c"," ")
  
  html = ""
  sync_reasoner_hermit()
  if consul == "1" :
        html = """<p>>%s</p>""" % onto.Mat_Vis_Glo_M.instances()
  else:
     if consul == "2" :
        html = """<p>>%s</p>""" % onto.Persona_Estilo_Verbal_Global_Fuerte.instances()
     else:
         d = (list(graph.query_owlready("""
                              PREFIX rdf-syntax: <http://www.w3.org/1999/02/22-rdf-syntax.ns#>
                              PREFIX estilo: <http://www.semanticweb.org/root/ontologies/estilo#>
                              SELECT distinct ?a ?b ?c WHERE {
                                  ?a estilo:se_relaciona_con estilo:verbal_secuencial_fuerte.
                                  ?b estilo:tiene estilo:verbal_secuencial_fuerte.
                                              }""")))
         for x in range(0,len(d)):
           html += """<br>>%s</br>""" % str(d[x])
    
  return html
           
  
  #  sync_reasoner_hermit()
  #  html = """<p>>%s</p>""" % onto.Mat_Vis_Glo_M.instances()


#import werkzeug.serving
#werkzeug.serving.run_simple("localhost", 5000, app)
app.run('0.0.0.0', 5000, debug=True)