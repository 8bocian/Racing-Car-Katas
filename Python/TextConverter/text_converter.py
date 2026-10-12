
# This is for Python 3
import html as html_converter

# for Python 2 uncomment this line
#import cgi as html_converter


def lines_to_html(lines):
    html = ""
    for line in lines:
        html += html_converter.escape(line.rstrip(), quote=True) + "<br />"
    return html

class UnicodeFileToHtmlTextConverter(object):

    def __init__(self, full_filename_with_path):
        self.full_filename_with_path = full_filename_with_path

    def convert_to_html(self):
        with open(self.full_filename_with_path, "r", encoding="utf-8") as f:
            return lines_to_html(f)
