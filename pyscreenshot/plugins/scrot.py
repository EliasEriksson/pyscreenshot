from easyprocess import EasyProcess
from easyprocess import extract_version
from PIL import Image
import tempfile
import logging

log = logging.getLogger(__name__)


PROGRAM = 'scrot'


class ScrotWrapper(object):
    name = 'scrot'
    childprocess = True

    def __init__(self):
        EasyProcess([PROGRAM, '-version']).check_installed()

    def grab(self, bbox=None):
        f = tempfile.NamedTemporaryFile(
            suffix='.png', prefix='pyscreenshot_scrot_')
        filename = f.name
        self._grab_to_file(filename)
        im = Image.open(filename)
        if bbox:
            im = im.crop(bbox)
        return im

    def _grab_to_file(self, filename):
        EasyProcess([PROGRAM, '--silent', "--overwrite", filename]).call()

    def backend_version(self):
        return extract_version(
            EasyProcess([PROGRAM, '-version']).call().stdout)
