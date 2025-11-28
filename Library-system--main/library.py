"""
Name: Replace with your name
Date: 2025-11-19
Assignment: Library System - library.py
"""

import json
from typing import Dict, Optional, List
from book import Book
from member import Member
import os

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"

class Library:
    def __init__(self, books_file: str = BOOKS_FILE, members_file: str = MEMBERS_FILE):
        # store books as dict keyed by ISBN
        self.books: Dict[str, Book] = {}
        # store members keyed by member_id
        self.members: Dict[str, Member] = {}
        self.books_file = books_file
        self.members_file = members_file

    # ---- Book & Member management ----
    def add_book(self, title: str, author: str, isbn: str) -> bool:
        if isbn in self.books:
            return False  # already exists
        self.books[isbn] = Book(title=title, author=author, isbn=isbn)
        return True

    def register_member(self, name: str, member_id: str) -> bool:
        if member_id in self.members:
            return False
        self.members[member_id] = Member(name=name, member_id=member_id)
        return True

    def find_book(self, isbn: str) -> Optional[Book]:
        return self.books.get(isbn)

    def find_member(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id)

    # ---- Lend / Return ----
    def lend_book(self, member_id: str, isbn: str) -> str:
        member = self.find_member(member_id)
        if not member:
            return "Member not found."

        book = self.find_book(isbn)
        if not book:
            return "Book not found."

        if not book.available:
            return "Book is currently not available."

        # perform borrow
        good = book.borrow()
        if good:
            member.borrow_book(isbn)
            self.save_data()  # persist immediately
            return f"Book '{book.title}' lent to {member.name}."
        else:
            return "Failed to borrow the book (unknown reason)."

    def take_return(self, member_id: str, isbn: str) -> str:
        member = self.find_member(member_id)
        if not member:
            return "Member not found."
        book = self.find_book(isbn)
        if not book:
            return "Book not found."

        # validate member had borrowed it
        removed = member.return_book(isbn)
        if not removed:
            return f"Member {member.name} does not have this book recorded."

        returned = book.return_book()
        if returned:
            self.save_data()
            return f"Book '{book.title}' successfully returned by {member.name}."
        else:
            # If book was already marked available but member had it listed, still clear member's record already done above.
            self.save_data()
            return f"Book '{book.title}' return recorded (book was already available)."

    # ---- Persistence ----
    def save_data(self) -> None:
        # books
        try:
            with open(self.books_file, "w", encoding="utf-8") as f:
                books_list = [b.to_dict() for b in self.books.values()]
                json.dump(books_list, f, indent=2)
        except Exception as e:
            print(f"Error saving books: {e}")

        # members
        try:
            with open(self.members_file, "w", encoding="utf-8") as f:
                members_list = [m.to_dict() for m in self.members.values()]
                json.dump(members_list, f, indent=2)
        except Exception as e:
            print(f"Error saving members: {e}")

    def load_data(self) -> None:
        # load books
        if os.path.exists(self.books_file):
            try:
                with open(self.books_file, "r", encoding="utf-8") as f:
                    books_list = json.load(f)
                for bd in books_list:
                    b = Book.from_dict(bd)
                    self.books[b.isbn] = b
            except Exception as e:
                print(f"Error loading books data: {e}")

        # load members
        if os.path.exists(self.members_file):
            try:
                with open(self.members_file, "r", encoding="utf-8") as f:
                    members_list = json.load(f)
                for md in members_list:
                    m = Member.from_dict(md)
                    self.members[m.member_id] = m
            except Exception as e:
                print(f"Error loading members data: {e}")

    # ---- Analytics ----
    def most_borrowed_book(self) -> Optional[Book]:
        if not self.books:
            return None
        # return book with max borrow_count
        return max(self.books.values(), key=lambda b: b.borrow_count)

    def total_active_members(self) -> int:
        return sum(1 for m in self.members.values() if m.borrowed_books)

    def number_of_books_currently_borrowed(self) -> int:
        return sum(1 for b in self.books.values() if not b.available)

    def library_report(self) -> str:
        most = self.most_borrowed_book()
        most_str = f"'{most.title}' (ISBN: {most.isbn}) borrowed {most.borrow_count} times." if most else "No books yet."
        report = (
            f"Total books: {len(self.books)}\n"
            f"Total members: {len(self.members)}\n"
            f"Active members (with at least one borrowed book): {self.total_active_members()}\n"
            f"Books currently borrowed: {self.number_of_books_currently_borrowed()}\n"
            f"Most borrowed book: {most_str}"
        )
        return report

    # convenience: list books and members
    def list_all_books(self) -> List[str]:
        return [str(b) for b in self.books.values()]

    def list_all_members(self) -> List[str]:
        return [str(m) for m in self.members.values()]
