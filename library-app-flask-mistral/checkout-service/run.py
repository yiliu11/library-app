from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)  # Using port 5002 for Checkout Service
