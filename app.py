from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# For Vercel deployment, we'll use in-memory storage
# In production, this should be replaced with a proper database
sessions_data = {'sessions': [], 'streak': 0, 'last_session_date': None}

def load_data():
    """Load session data from memory"""
    return sessions_data

def save_data(data):
    """Save session data to memory"""
    global sessions_data
    sessions_data = data

def update_streak(data):
    """Update streak counter based on session completion"""
    today = datetime.now().date().isoformat()
    last_date = data.get('last_session_date')
    
    if last_date:
        last_session = datetime.fromisoformat(last_date).date()
        today_date = datetime.now().date()
        
        # If more than 1 day has passed, reset streak
        if (today_date - last_session).days > 1:
            data['streak'] = 0
    
    # Check if session was completed today
    today_sessions = [s for s in data['sessions'] if s['date'] == today and s['completed']]
    if today_sessions:
        if last_date != today:
            data['streak'] += 1
            data['last_session_date'] = today
    else:
        data['streak'] = 0
    
    return data

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/start_session', methods=['POST'])
def start_session():
    """Start a new breathing session"""
    data = request.json
    bpm = data.get('bpm', 6)
    
    session_data = load_data()
    
    # Create new session
    session = {
        'id': len(session_data['sessions']) + 1,
        'date': datetime.now().date().isoformat(),
        'bpm': bpm,
        'started_at': datetime.now().isoformat(),
        'completed': False
    }
    
    session_data['sessions'].append(session)
    save_data(session_data)
    
    return jsonify({
        'success': True,
        'session_id': session['id'],
        'bpm': bpm,
        'cycle_duration': get_cycle_duration(bpm)
    })

@app.route('/api/complete_session', methods=['POST'])
def complete_session():
    """Mark session as completed"""
    data = request.json
    session_id = data.get('session_id')
    
    session_data = load_data()
    
    # Find and update session
    for session in session_data['sessions']:
        if session['id'] == session_id:
            session['completed'] = True
            session['completed_at'] = datetime.now().isoformat()
            break
    
    # Update streak
    session_data = update_streak(session_data)
    save_data(session_data)
    
    return jsonify({
        'success': True,
        'streak': session_data['streak']
    })

@app.route('/api/get_streak', methods=['GET'])
def get_streak():
    """Get current streak count"""
    session_data = load_data()
    return jsonify({'streak': session_data['streak']})

@app.route('/api/get_sessions', methods=['GET'])
def get_sessions():
    """Get recent sessions"""
    session_data = load_data()
    recent_sessions = session_data['sessions'][-10:]  # Last 10 sessions
    return jsonify({'sessions': recent_sessions})

def get_cycle_duration(bpm):
    """Calculate cycle duration in seconds based on BPM"""
    durations = {6: 10, 5: 12, 4: 15, 3: 20}
    return durations.get(bpm, 10)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
