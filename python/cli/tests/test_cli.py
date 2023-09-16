import subprocess


def test_base():
    in_ = "hello world"
    out_ = f"processed: {in_}"
    pipe = subprocess.Popen(
        ["my_py_cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    out, err = pipe.communicate(in_)

    assert pipe.returncode == 0
    assert out_ in out
