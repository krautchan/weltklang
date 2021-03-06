__author__ = 'teddydestodes'
import re
import os


disclaimer = """
# AUTOGENERATED BY contrib/parse_fontawesome_icons.py
# DO NOT EDIT THIS FILE!
"""


if __name__ == '__main__':
    icon = re.compile('(fa-.*?):before')
    fontawesome_css = os.path.join(os.path.dirname(__file__), '..', 'static', 'css', 'font-awesome.css')
    icons = []
    with open(fontawesome_css) as f:
        for name in icon.findall(f.read()):
            if name not in icons:
                icons.append(name)

        icons = sorted(icons)

    taglist_py = os.path.join(os.path.dirname(__file__), '..', 'helper', 'taglist.py')

    with open(taglist_py, 'wb') as f:
        f.write(disclaimer)
        f.write('taglist = ("')
        f.write('",\n           "'.join(icons))
        f.write('")')

