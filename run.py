from app.app import app

if __name__ == "__main__":
    app.config.from_object("config.default")
    app.run()
