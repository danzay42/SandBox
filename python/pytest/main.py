class Context:

    def __init__(self) -> None:
        print("context init")

    def _exec(self, some):
        print("context exec")
        print(some)

    def __enter__(self):
        print("context enter")
        return self._exec

    def __exit__(self, *args):
        print("context exit")


class Creator:

    def __init__(self, cm: Context) -> None:
        self.cm = cm

    def build(self):
        with self.cm as runner:
            print(f"build {runner=}")
            runner("build args")
  
