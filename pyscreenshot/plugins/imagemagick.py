from easyprocess import EasyProcess
from easyprocess import extract_version
from PIL import Image
import tempfile

PROGRAM = 'import'
# http://www.imagemagick.org/


class ImagemagickWrapper(object):
    name = 'imagemagick'
    childprocess = True

    def __init__(self):
        EasyProcess([PROGRAM, '-version']).check_installed()

    def grab(self, bbox=None):
        f = tempfile.NamedTemporaryFile(
            suffix='.png', prefix='pyscreenshot_imagemagick_')
        filename = f.name
        self._grab_to_file(filename, bbox=bbox)
        im = Image.open(filename)
        return im

    def _grab_to_file(self, filename, bbox=None):
        command = [PROGRAM, '-silent', '-window', 'root']
        if bbox:
            pbox = '{}x{}+{}+{}'.format(
                bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1])
            command += ['-crop', pbox]
        command += [filename]
        EasyProcess(command).call()

    def backend_version(self):
        return extract_version(
            EasyProcess([PROGRAM, '-version']).call().stdout.replace('-', ' '))
