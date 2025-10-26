# Breath Center

A simple 10-minute breathing practice app that helps train your breathing rhythm from 6 to 3 breaths per minute for autonomic balance.

## Features

- **Breathing Timer**: Cycles at selected BPM (6=10s, 5=12s, 4=15s, 3=20s)
- **Session Clock**: Fixed 10-minute countdown with auto-stop
- **Streak Counter**: Tracks daily completion streaks
- **Phase Selector**: Choose between 6, 5, 4, or 3 breaths per minute
- **Minimal Logging**: Stores session data locally
- **Clean UI**: Single page with animated breathing guide

## Setup

1. Install dependencies:
```bash
pip install -r reqs.txt
```

2. Run the app:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## Usage

1. Select your breathing phase (6, 5, 4, or 3 breaths per minute)
2. Click "Start 10 min Session"
3. Follow the animated breathing guide
4. Complete the session to maintain your streak

## Technical Details

- **Backend**: Python Flask with JSON file storage
- **Frontend**: HTML/CSS/JavaScript with smooth animations
- **Data**: Local JSON file storage (no database required)
- **Port**: 5000 (configurable in app.py)
