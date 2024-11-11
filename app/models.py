from typing import List

from pydantic import BaseModel


class CreateBookModel(BaseModel):
    name: str
    count_in_library: int
    authors: List[str]
    genres: List[str]


class EditBookModel(BaseModel):
    id: int
    name: str
    count_in_library: int
    authors: List[str]
    genres: List[str]


class CreateUserModel(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str


class EditUserModel(BaseModel):
    id: int
    name: str
    address: str
    phone_number: str
    email: str


class DeleteModel(BaseModel):
    id: int


class GetBook(BaseModel):
    user_id: int
    book_id: int
    interval: int


class ReturnBook(BaseModel):
    user_id: int
    book_id: int