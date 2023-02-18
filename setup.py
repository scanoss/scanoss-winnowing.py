from setuptools import setup, Extension

winnowing_ext = Extension('_winnowing',
                          language='c',
                          sources=['src/scanoss_winnowing/_winnowing.c'],
                          include_dirs=['.'],
                          extra_compile_args=["-O3"])


setup(
    ext_modules=[winnowing_ext]
)
