from flask import Flask
from flask import jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

app=Flask(__name__)
CORS(app)

# engine=create_engine('sqlite:///assets/data/breweries.sqlite')

# Base=automap_base()
# Base.prepare(engine, reflect=True)
# Brewery=Base.classes.breweries

@app.route('/')
def index():
	return 'Welcome'
	# return jsonify({'message': 'Welcome'})

@app.route('/sample/')
def sample():
	return jsonify([{'state': 'CA', 'city': 'Napa', 'name': 'Sample'}])

# read csv and store in the cache of the server

@app.route('/breweries/')
@app.route('/breweries/<query_string>')
def fetch(query_string=None): 
	# session=Session(engine)
	# results=session.query(Brewery.state, Brewery.city, Brewery.name).all()
	# session.close()
	query_param='where '
	params=0
	if query_string: 
		for each_param in query_string.split('&'): 
			key, value=each_param.split('=')
			if params>0: 
				query_param+='and '
			if key.lower()=='state': 
				query_param+=f'state="{value.upper()}"'
				params=params+1
			if key.lower()=='name': 
				query_param+=f'name like "%{value.capitalize()}%"'
				params=params+1
			if key.lower()=='city': 
				query_param+=f'city="{value.capitalize()}"'
				params=params+1
		# results=engine.execute(f'select state, city, name from breweries where state="{query_string.upper()}"')
		results=engine.execute(f'select state, city, name from breweries {query_param}')
	else: 
		results=engine.execute('select state, city, name from breweries')
	# return jsonify(list(results))
	return jsonify([{'state': result[0], 'city': result[1], 'name': result[2]} for result in results])

if __name__ == '__main__':
    app.run()