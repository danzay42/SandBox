import typing
import pathlib
import io
import json
import re
from html.parser import HTMLParser
import dataclasses
import collections


def manipulating_paths_as_strings():
    def bad():
        path = "path/to/data/my_data.json"
        zipped_file = path.removesuffix(".json") + ".zip"
        data_dir = "/".join(path.split("/")[:-1])
        other_file = f"{data_dir}/other_file.txt"
        deeper_dir = f"{data_dir}/abc/def"
    def good():
        path = pathlib.Path("path/to/data/my_data.json")
        zipped_file = path.with_suffix(".zip")
        data_dir = path.parent
        other_file = path.with_name("other_file.txt")
        deeper_dir = data_dir.joinpath("abc", "def")


def noob_do_io_taking_path(path: str):
    with open(path, "W") as fp:
        fp.write("...")
def do_io_taking_io(fp: typing.TextIO):
    fp.write("...")


def concatenation_strings_with_plus():
    def bad():
        s = ""
        for i in range(100):
            s += f"some string {i}"
    def good():
        ss = io.StringIO()
        for i in range(100):
            ss.write(f"some string {i}")
        s = ss.getvalue()


def using_eval_as_a_parser():
    data_str = '{"a":1, "b":2, "c":3}'
    data = eval(data_str) # not the best solution
    data = json.loads(data_str) # or pydantic


def using_div_and_mod_instead_of_divmod(x, p):
    # wrong
    q, r = x // p, x % p
    # correct
    q, r = divmod(x, p)
    

def ntrying_to_parse_html_or_xml_using_regex():
    html = """
    <html>
    <body>
    <a href="https://google.com">Some Url</a>
    </body>
    </html>
    """
    
    def wrong():
        links_regex = '<a href="(.*?)">'
        for match in re.finditer(links_regex, html):
            print(f"noob found link: {match.group(1)}")
    
    def correct():
        class UrlParser(HTMLParser):
            def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
                if tag != "a":
                    return
                for attr, val in attrs:
                    if attr == "href":
                        print(f"pro found link: {val}")
                        break
        UrlParser().feed(html)


def inheritance_model():
    class Root:
        def f(self):
            print("root.f")
    class A(Root):
        def f(self):
            print("a.f")
            super().f()
    class B(Root):
        def f(self):
            print("b.f")
            super().f()
    class C(A, B):
        def f(self):
            print("c.f")
            super().f()
    C().f()


def passing_structed_data_as_dict_or_tuple():
    def wrong_way():
        # take some measurments
        measurement = 1.0001
        timestamp = ...
        location = ...
        return {
            "measurement": measurement,
            "timestamp": timestamp,
            "location": location,
        }
    
    @dataclasses.dataclass
    class Measurement:
        value: float
        timestamp: float
        location: tuple[float, float]
    # or named tupled
    class Measurement(typing.NamedTuple):
        value: float
        timestamp: float
        location: tuple[float, float]
    
    def good_way():
       # take some measurments
        measurement = 1.0001
        timestamp = ...
        location = ...
        return Measurement(
            value=measurement,
            timestamp=timestamp,
            location=location,
        )
    
    wrong_way()
    good_way()


def using_namedtuple_instead_of_NamedTuple():
    # Old way
    Point = collections.namedtuple("Point", ["x", "y", "z"])
    # New way
    class Point(typing.NamedTuple):
        x: float
        y: float
        z: float
    
    p = Point(1,2,3)
    print(p.x + p.y + p.z)
