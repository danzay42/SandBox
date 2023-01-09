from life import __version__, core


def test_version():
    assert __version__ == '0.1.1'


def test_update_state():
    assert core.new_cell(1, 2)
    assert core.new_cell(1, 3)
    assert core.new_cell(0, 3)

    assert not core.new_cell(0, 0)
    assert not core.new_cell(0, 1)
    assert not core.new_cell(0, 2)
    assert not core.new_cell(0, 4)
    assert not core.new_cell(0, 5)
    assert not core.new_cell(0, 6)
    assert not core.new_cell(0, 7)
    assert not core.new_cell(0, 8)
    assert not core.new_cell(1, 0)
    assert not core.new_cell(1, 1)
    assert not core.new_cell(1, 4)
    assert not core.new_cell(1, 5)
    assert not core.new_cell(1, 6)
    assert not core.new_cell(1, 7)
    assert not core.new_cell(1, 8)

