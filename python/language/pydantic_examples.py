import json
import pydantic


class ISBN10FormatError(Exception):
    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class ISBNMissingError(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message) 


class Book(pydantic.BaseModel):
    title: str
    author: str
    publisher: str
    price: float
    isbn_10: str | None
    isbn_13: str | None
    subtitle: str | None

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn10_or_isbn13(cls, values):
        if "isbn_10" not in values and "isbn_13" not in values:
            raise ISBNMissingError(values["title"], "Document should have either an ISBN10 or ISBN13")
        return values

    @pydantic.validator("isbn_10")
    @classmethod
    def isbn_10_validator(cls, value):
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(value, "ISBN should be 10 digits")
        
        def char_to_int(char: str) -> int:
            if char in "xX":
                return 10
            return int(char)
        
        weighted_sum = sum((10-i)*char_to_int(x) for i,x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(value, "ISBN digits sum should be divisible by 11")
    

    class Config:
        allow_mutation = False
        anystr_lower = True


def json_std_lib_example():
    with open("./data.json") as file:
        data = json.load(file)
        print(data[0])


def main():
    with open("./data.json") as file:
        data = json.load(file)
        books: list[Book] = [Book(**item) for item in data]
        print(books[0])
        books[0].title = "new title"


if __name__ == "__main__":
    # json_std_lib_example()
    main()

