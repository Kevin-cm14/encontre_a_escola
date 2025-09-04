from flask import Flask, render_template, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal do WebGIS"""
    return render_template('index.html')

@app.route('/map')
def map_view():
    """Visualização do mapa principal"""
    return render_template('map.html')

@app.route('/data/escolas_possiveis_rj_inep')
def get_escolas_possiveis():
    return send_file('escolas_possiveis_rj_inep.geojson', mimetype='application/json')

@app.route('/data/mun_leste_flu_2')
def get_mun_leste_flu_2():
    return send_file('mun_leste_flu_2.geojson', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 