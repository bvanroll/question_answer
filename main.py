import os
import cherrypy
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
model_name = "deepset/roberta-base-squad2"

path   = os.path.abspath(os.path.dirname(__file__))
config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
  },
}

class Root(object):

  @cherrypy.expose
  def index(self, *args, **kwargs):
    answer = ""

    with open('data.txt') as f:
        context = f.read()
        f.close()

    if cherrypy.request.params.get('question'):
        question_answerer = pipeline('question-answering', model=model_name, tokenizer=model_name)
        temp = question_answerer({'question': cherrypy.request.params.get('question'), 'context': context})
        answer = "<h1>answer</h1><p>{}</p>".format(temp["answer"])

    return "<html><head><title>reinout project 1</title></head><body><h1>question</h1><form method=\"POST\" action=\"index\"><input type=\"text\" name=\"question\" size=\"50\"/><button type=\"submit\">send!</button></form>{}</body></html>".format(answer) 
 

if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', config)
