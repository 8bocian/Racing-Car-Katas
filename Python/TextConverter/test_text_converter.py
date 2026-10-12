import pytest

from text_converter import UnicodeFileToHtmlTextConverter, lines_to_html

@pytest.fixture
def convert(tmp_path):
    def _convert(content):
        path = tmp_path / "input.txt"
        path.write_text(content, encoding="utf-8", newline="")
        converter = UnicodeFileToHtmlTextConverter(path)
        return converter.convert_to_html()
    return _convert

def test_filename_gets_saved():
    converter = UnicodeFileToHtmlTextConverter("foo")
    assert "foo" == converter.full_filename_with_path


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        UnicodeFileToHtmlTextConverter("does_not_exist.txt").convert_to_html()

def test_empty_string():
    assert lines_to_html([]) == ""

def test_each_line_contains_br():
    assert lines_to_html(["test\n","test"]) == "test<br />test<br />"

def test_each_sign_is_converted():
    assert lines_to_html(["&<>\"'"]) == "&amp;&lt;&gt;&quot;&#x27;<br />"

def test_converted_sign_gets_converted_again():
    assert lines_to_html(["&amp;"]) == "&amp;amp;<br />"

def test_leading_spaces_persist():
    assert lines_to_html(["   test"]) == "   test<br />"

def test_trailing_spaces_are_cut():
    assert lines_to_html(["test   "]) == "test<br />"

def test_removes_space_in_each_line():
    assert lines_to_html([" \n"," \n"," \n"]) == "<br /><br /><br />"

def test_tabs_get_stripped():
    assert lines_to_html(["test\t"]) == "test<br />"

def test_empty_line_produces_br():
    assert lines_to_html(["a\n","\n","b"]) == "a<br /><br />b<br />"

def test_trailing_newline_adds_no_extra_br(convert):
    assert convert("test\n") == "test<br />"

def test_windows_line_endings_convert_to_br(convert):
    assert convert("a\r\nb") == "a<br />b<br />"

def test_polish_signs(convert):
    assert convert("ąężćółń") == "ąężćółń<br />"
