from backend import app

if __name__ == "__main__":
    # socketio.run(app, host="localhost")
    app.run(debug=True)
