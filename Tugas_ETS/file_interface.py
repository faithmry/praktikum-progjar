import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def upload(self, params=[]):
        try:
            if len(params) < 2:
                return dict(status='ERROR', data='Parameter upload kurang.')

            filename = params[0]
            encoded_content = params[1]

            isifile = base64.b64decode(encoded_content)
            with open(filename, 'wb+') as fp:
                fp.write(isifile)
            return dict(status='OK', message=f"File '{filename}' berhasil diupload.")
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            if len(params) < 1:
                return dict(status='ERROR', data='Parameter delete belum ada.')

            filename = params[0]
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f"File '{filename}' tidak ditemukan.")

            os.remove(filename)
            return dict(status='OK', message=f"File '{filename}' berhasil dihapus.")
        except Exception as e:
            return dict(status='ERROR', data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
