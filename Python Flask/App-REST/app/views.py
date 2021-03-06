from flask import render_template, url_for, request,jsonify
from flask import Response
import json
import jwt, datetime
from app import app
from app.model.TechModel import Tech

@app.route('/')
def index():
	return render_template('public/index.html')

@app.route('/login')
def login():
	app.logger.info('login method start')
	expire_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
	token = jwt.encode({'exp': expire_date}, app.config['SECRET_KEY'], algorithm='HS256')
	app.logger.info('login method end')
	return token

# GET
@app.route('/get-tech')
def get_tech():
	"""
	app.logger.info('get_tech method start')
	token = request.args['token']
	try:
		jwt.decode(token, app.config['SECRET_KEY'])
	except:
		app.logger.info('get_tech method end')
		return jsonify({'error' : 'Please use proper token'})
	app.logger.info('get_tech method end')
	"""
	return jsonify({'technology': Tech.get_all_tech()})

@app.route('/get-tech/<int:rank>')
def get_tech_by_rank(rank):
	return jsonify({rank: Tech.get_tech_by_rank(rank)})

# POST
def valid_tech_object(tech_object):
	if ('name' in tech_object and 'nod' in tech_object and 'rank' in tech_object):
		return True
	else:
		return False

def convert_valid_object(tech_object):
	return {
	'name' : tech_object['name'],
	'nod' : tech_object['nod'],
	'rank' : tech_object['rank']
	}

def validate_object_empty(tech_object):
	return tech_object['name'] == '' or tech_object['nod'] == 0 or tech_object['rank'] == 0

@app.route('/add-tech', methods=['POST'])
def add_tech():
	request_data = request.get_json()
	if(validate_object_empty(request_data)):
		emptyDict = {}
		if(request_data['name'] == ''):
			emptyDict['name'] ='Name Required'
		if(request_data['nod'] == 0):
			emptyDict['nod'] ='No of Developer Required'
		if(request_data['rank'] == 0)	:
			emptyDict['rank'] ='Rank Required'
		response = Response(json.dumps(emptyDict), status=400, mimetype='application/json')
		return response
	elif(valid_tech_object(request_data)):
		Tech.add_tech(request_data['name'], request_data['nod'], request_data['rank'])
		response = Response('', status=201, mimetype='application/json')
		response.headers['Location'] = '/get-tech/'+str(request_data['rank'])
		return jsonify(Tech.get_tech_by_rank(request_data['rank']))
	else:
		error_object_msg = {
			'error': 'Invalid tech object is passed in request',
			'help': 'Sample tech data : {"name":"AI", "nod":23000, "rank":1}'
		}
		response = Response(json.dumps(error_object_msg), status=400, mimetype='application/json')
		return jsonify({'result':error_object_msg})

# PUT
def valid_put_tech_object(tech_object):
	if ('name' in tech_object and 'nod' in tech_object):
		return True
	else:
		return False

@app.route('/replace-tech/<int:rank>', methods=['PUT'])
def replace_tech(rank):
	request_data = request.get_json()
	print(request_data)
	if(not valid_put_tech_object(request_data)):
		error_object_msg = {
			"error": "Invalid tech object is passed in request",
			"help": "Sample tech data : {'name':'AI', 'nod':23000, 'rank':1}"
		}
		response = Response(json.dumps(error_object_msg), status=400, mimetype='application/json')
		return jsonify({'result': 'failed'})
	else:
		Tech.replace_tech(rank, request_data['name'], request_data['nod'])
		response = Response('', status=204)
		return jsonify(Tech.get_tech_by_rank(rank))

# PATCH
@app.route('/update-tech/<int:rank>', methods=['PATCH'])
def update_tech(rank):
	request_data = request.get_json()
	if ('name' in request_data):
		Tech.update_tech_name(rank, request_data['name'])
	if ('nod' in request_data):
		Tech.update_tech_nod(rank, request_data['nod'])
	response = Response('', status=204)
	response.headers['Location'] = '/get-tech/'+str(rank)
	return response

#DELETE
@app.route('/delete-tech/<int:rank>', methods=['DELETE'])
def delete_tech(rank):
	if(Tech.delete_tech(rank)):
		response = Response('', status=204)
		return jsonify({})
	delete_error_msg = {
	'error' : 'This requested rank is not available.So, Please give proper rank.',
	}
	response = Response(json.dumps(delete_error_msg), status=404, mimetype='application/json')
	return jsonify({})