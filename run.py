from app import create_app

# 1. We call the factory function to build the app instance
app = create_app()

if __name__ == "__main__":
    # 2. Start the development server
    # debug=True means the server will restart automatically when you change code
    # and give you a detailed error page if things crash.
    app.run(debug=True)