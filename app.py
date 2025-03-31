from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# homepage lay-out @templates/index.html
@app.route('/')
def home():
    return render_template('index.html')

# API voor planner
@app.route('/api/plan', methods=['POST'])
def plan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        weather_preference = data.get('weather_preference')
        attractions = data.get('attractions')

        print("Received plan:")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Weather Preference: {weather_preference}")
        print(f"Attractions: {', '.join(attractions)}")

        return jsonify({
            "message": "Plan successfully received!",
            "data": {
                "start_date": start_date,
                "end_date": end_date,
                "weather_preference": weather_preference,
                "attractions": attractions
            }
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process the request"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

