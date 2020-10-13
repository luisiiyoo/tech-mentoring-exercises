from App import create_app

PORT = 5050
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
