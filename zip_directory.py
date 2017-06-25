import os
import zipfile
from io import BytesIO
from flask import Flask, make_response


BASE_PATH = '/base/public/directory'
APP = Flask(__name__)

@APP.route('/<some_directory>')
def zip_some_directory(some_directory):
    dir_path = os.path.join(BASE_PATH, some_directory)
    print(dir_path)
    if os.path.isdir(dir_path):
        buff = zip_directory(dir_path)
        response = make_response(buff.read())
        response.headers['Content-type'] = 'application/zip'
        return response
    else:
        return 'The requested directory does not exist', 404


def zip_directory(dir_path):
    buff = BytesIO()
    with zipfile.ZipFile(buff, 'w', zipfile.ZIP_DEFLATED) as my_zip:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                my_zip.write(os.path.join(root, file))
    buff.seek(0, 0)
    return buff


if __name__ == '__main__':
    APP.run()
