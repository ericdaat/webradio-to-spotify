from application.app import app as application

if __name__ == '__main__':
    application.run(port=9999, debug=False)