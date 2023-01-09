try:
    1/0
except Exception as e:
    e.add_note("моя записка")
    raise