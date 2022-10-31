import inspect
from dataclasses import dataclass, astuple, asdict, field
from pprint import pprint
from typing import NamedTuple


@dataclass(frozen=True, order=True)  # frozen makes it immutable (read only)
class Comment:
	id: int
	text: str
	replies: list[int] = field(default_factory=list, compare=False, hash=False)


def main():
	commnet = Comment(1, "foo")
	print(commnet)
	print(asdict(commnet)) 
	print(astuple(commnet))
	commnet.replies.append(1)
	print(commnet)

	# pprint(inspect.getmembers(Comment, inspect.isfunction))  # get implemented functions


if __name__ == "__main__":
	main()
