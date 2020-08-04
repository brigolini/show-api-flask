from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

shows = [{
    'name': 'Friends',
    'episodes': [{'name':'The one that Monica gets a room mate', 'season': 1 }]
}]

@app.route('/', methods=['GET'])
def home():
  return "API Funcionando", 200

#post /show data: {name :}
@app.route('/show' , methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_show = {
    'name':request_data['name'],
    'episodes':[]
  }
  shows.append(new_show)
  return jsonify(new_show)
  #pass

#get /show/<name> data: {name :}
@app.route('/show/<string:name>')
def get_show(name):
  for show in shows:
    if show['name'] == name:
          return jsonify(show)
  return jsonify ({'message': 'show not found'})
  #pass

#get /show
@app.route('/show')
def get_shows():
  return jsonify({'shows': shows})
  #pass

#post /show/<name> data: {name :}
@app.route('/show/<string:name>/item' , methods=['POST'])
def create_item_in_show(name):
  request_data = request.get_json()
  for show in shows:
    if show['name'] == name:
        new_item = {
            'name': request_data['name'],
            'season': request_data['season']
        }
        show['episodes'].append(new_item)
        return jsonify(new_item)
  return jsonify ({'message' :'série não existe'}), 404
  #pass

#get /show/<name>/item data: {name :}
@app.route('/show/<string:name>/item')
def get_item_in_show(name):
  for show in shows:
    if show['name'] == name:
        return jsonify( {'episodes':show['episodes'] } )
  return jsonify ({'message':'Série não existe'}),401

  #pass

app.run(port=5000)