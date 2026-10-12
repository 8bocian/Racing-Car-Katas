from text_converter import UnicodeFileToHtmlTextConverter
from pytest import fixture

@fixture
def tmp_file(tmp_path):
    return tmp_path / "input.txt"

@fixture
def convert(content):
    def _convert(tmp_path):
        path = tmp_path / "input.txt"
        path.write_text(content, encoding="utf-8")
        converter = UnicodeFileToHtmlTextConverter(path)
        return converter.convert_to_html()
    return _convert

def test_filename_gets_saved():
    converter = UnicodeFileToHtmlTextConverter("foo")
    assert "foo" == converter.full_filename_with_path

def test_empty_string(tmp_file):
    # tmp_file.write_text("")
    # converter = UnicodeFileToHtmlTextConverter(tmp_file)
    # converted = converter.convert_to_html()
    # assert converted == ""
    assert convert("") == ""

def test_each_line_contains_br(tmp_file):
    tmp_file.write_text("test\ntest")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "test<br />test<br />"

def test_each_sign_is_converted(tmp_file):
    tmp_file.write_text("&<>\"'")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "&amp;&lt;&gt;&quot;&#x27;<br />"

def test_converted_sign_gets_converted_again(tmp_file):
    tmp_file.write_text("&amp;")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "&amp;amp;<br />"

def test_leading_spaces_persist(tmp_file):
    tmp_file.write_text("   test")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "   test<br />"

def test_trailing_spaces_are_cut(tmp_file):
    tmp_file.write_text("test   ")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "test<br />"

def test_removes_space_in_each_line(tmp_file):
    tmp_file.write_text(" \n \n \n")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "<br /><br /><br />"

def test_polish_signs(tmp_file):
    tmp_file.write_text("ąężćółń", encoding="utf-8")
    converter = UnicodeFileToHtmlTextConverter(tmp_file)
    converted = converter.convert_to_html()
    assert converted == "ąężćółń<br />"
