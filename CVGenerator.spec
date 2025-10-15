# -*- mode: python ; coding: utf-8 -*-

import reportlab
import os

reportlab_dir = os.path.dirname(reportlab.__file__)

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'), 
        ('static', 'static'), 
        ('render_templates', 'render_templates'),
        (reportlab_dir, 'reportlab')
    ],
    hiddenimports=[
        'reportlab.graphics.barcode.code128',
        'reportlab.graphics.barcode.code39',
        'reportlab.graphics.barcode.code93',
        'reportlab.graphics.barcode.common',
        'reportlab.graphics.barcode.eanbc',
        'reportlab.graphics.barcode.qr',
        'reportlab.graphics.barcode.usps',
        'reportlab.graphics.barcode.usps4s',
        'reportlab.graphics.barcode.ecc200datamatrix',
        'reportlab.graphics.barcode.widgets',
        'xhtml2pdf',
        'xhtml2pdf.default',
        'xhtml2pdf.document',
        'xhtml2pdf.parser',
        'xhtml2pdf.context',
        'xhtml2pdf.tags',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CVGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)