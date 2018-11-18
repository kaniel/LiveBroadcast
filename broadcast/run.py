from broadcast import create_app

if __name__ == "__main__":
    from settings import DEV
    app = create_app(DEV)
    app.run()
else:
    from settings import PROD
    app = create_app(PROD)
