import random
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from scoringalgoritme import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/DisneyWorldDagPlanner/home')
def home():
    return render_template('index.html')

@app.route('/DisneyWorldDagPlanner/planning', methods=['GET', 'POST'])
def planning():
    if request.method == 'POST':
        #input!!!!!!!!!!!!!!!!!!hier!!!!!!!!!!!!!!!
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        weather_preference = data.get('weather_preference')
        attractions = data.get('attractions')
        day_type = data.get('day_type')
        if not attractions or len(attractions) > 4:
            return jsonify({'error': 'Invalid number of attractions'}), 400
        #backend!!!!!!!!!!!!!!!hier!!!!!!!!!!!!!!!!!!!!!!!!!
        odf = OptimalDayFinder(start_date, end_date, day_type, weather_preference, attractions, "Cool model")
        odf_output = odf.plan()
        #output!!!!!!!!!!!!!!!!hier!!!!!!!!!!!!
        session['start_date'] = start_date
        session['end_date'] = end_date
        session['weather_preference'] = weather_preference
        session['attractions'] = odf_output[0]
        session['attraction_times'] = odf_output[1]
        session['day_type'] = day_type
        session['picked_date'] = odf_output[2]

        return redirect(url_for('planning'))

    return render_template('planning.html',
                           start_date=session.get('start_date'),
                           end_date=session.get('end_date'),
                           weather_preference=session.get('weather_preference'),
                           attractions=session.get('attractions'),
                           attraction_times=session.get('attraction_times'),
                           day_type=session.get('day_type'),
                           picked_date=session.get('picked_date'))

@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.clear()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
