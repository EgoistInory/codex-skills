import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/finalize_wrap.py'
spec = importlib.util.spec_from_file_location('finalize_wrap', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FinalizeTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.template = self.root / 'template.png'
        image = Image.new('RGBA', (1024,1024), (0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.rectangle((50,90,350,900), fill=(255,255,255,255))
        draw.rectangle((51,91,349,899), fill=(255,255,255,127))
        image.save(self.template)
        self.alpha = image.getchannel('A').tobytes()
        self.sha = hashlib.sha256(self.template.read_bytes()).hexdigest()
        self.design = self.root / 'design.png'
        Image.new('RGBA', (1024,1024), (25,65,111,96)).save(self.design)

    def run_job(self, **changes):
        args = dict(template=self.template, design=self.design, output=self.root/'Wrap_Test.png',
                    template_sha256=self.sha, model='test-model', base_color='#aeb5bf',
                    allow_rgb_quantization=False)
        args.update(changes)
        return module.finalize(**args)

    def test_real_png_has_exact_template_alpha_and_report_hash(self):
        result = self.run_job()
        output = self.root/'Wrap_Test.png'
        with Image.open(output) as image:
            self.assertEqual(image.format,'PNG')
            self.assertEqual(image.size,(1024,1024))
            self.assertEqual(image.mode,'RGBA')
            self.assertEqual(image.getchannel('A').tobytes(),self.alpha)
            self.assertGreater(image.getpixel((100,100))[0],25)
        report = json.loads((self.root/'Wrap_Test-report.json').read_text())
        self.assertLess(len(output.read_bytes()),1000000)
        self.assertEqual(report['sha256'],hashlib.sha256(output.read_bytes()).hexdigest())
        self.assertEqual(report['bytes'],len(output.read_bytes()))
        self.assertTrue(result['alpha_matches_template'])
        self.assertFalse(result['vehicle_import_verified'])

    def test_wrong_template_hash_creates_no_output(self):
        with self.assertRaisesRegex(ValueError,'哈希'):
            self.run_job(template_sha256='0'*64)
        self.assertFalse((self.root/'Wrap_Test.png').exists())

    def test_wrong_uv_size_is_rejected_without_rescaling(self):
        Image.new('RGBA',(512,512),'red').save(self.design)
        with self.assertRaisesRegex(ValueError,'1024'):
            self.run_job()

    def test_existing_file_is_not_overwritten(self):
        path=self.root/'Wrap_Test.png'; path.write_bytes(b'keep existing work')
        with self.assertRaises(FileExistsError): self.run_job()
        self.assertEqual(path.read_bytes(),b'keep existing work')

    def test_noncompliant_download_filename_is_rejected(self):
        for name in ['中文.png','a'*31+'.png','bad.svg','evil<>.png']:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError,'文件名'):
                self.run_job(output=self.root/name)

    def test_noisy_opaque_artwork_needs_explicit_color_reduction(self):
        import random
        image=Image.new('RGBA',(1024,1024),(255,255,255,255))
        ImageDraw.Draw(image).rectangle((0,0,0,1023),fill=(0,0,0,0))
        image.save(self.template)
        self.sha=hashlib.sha256(self.template.read_bytes()).hexdigest()
        Image.frombytes('RGB',(1024,1024),random.Random(29).randbytes(1024*1024*3)).save(self.design)
        with self.assertRaisesRegex(ValueError,'1 MB'):
            self.run_job()
        report=self.run_job(allow_rgb_quantization=True)
        self.assertLess(report['bytes'],1000000)
        self.assertGreater(report['rgb_quantization_step'],1)
        with Image.open(self.root/'Wrap_Test.png') as output:
            self.assertEqual(output.getchannel('A').tobytes(),image.getchannel('A').tobytes())


if __name__ == '__main__': unittest.main()
