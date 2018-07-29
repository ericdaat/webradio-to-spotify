import sys
sys.path.append('application')
from application.app import app as application

if __name__ == '__main__':
    application.run()
