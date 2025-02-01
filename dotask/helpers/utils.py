from flask import Flask, request, redirect, session
from dotask import app

@app.before_request
def track_history():
    # Initialize history in session if it doesn't exist
    if 'history' not in session:
        session['history'] = []

    # Add the current referrer to the history
    if request.referrer:
        session['history'].append(request.referrer)

    # Keep only the last 2 items in history
    if len(session['history']) > 2:
        session['history'] = session['history'][-2:]

@app.route('/go-back-two')
def go_back_two():
    # Get the second-to-last page from history
    if 'history' in session and len(session['history']) >= 2:
        return redirect(session['history'][-2])  # Redirect to the second-to-last page
    else:
        return redirect('/')  # Fallback to homepage if history is insufficient