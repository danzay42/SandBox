import subprocess

from src.cli import main


def test_international():
    in_ = "hello world"
    out_ = f"processed: {in_}"
    pipe = subprocess.Popen(
        ["my_py_cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    out, err = pipe.communicate(in_)

    assert pipe.returncode == 0
    assert out_ in out


def test_unit(capsys, tmp_path):
    in_ = "hello world"
    out_ = f"processed: {in_}\n"
    file_ = tmp_path / "temp"
    file_.write_text(in_)

    main(["-i", str(file_.absolute())])

    assert out_ == capsys.readouterr().out
