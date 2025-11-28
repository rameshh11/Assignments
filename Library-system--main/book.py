"""
Name: Replace with your name
Date: 2025-11-19
Assignment: Library System - book.py
"""

from typing import Dict

class Book:
    def __init__(self, title: str, author: str, isbn: str, available: bool = True, borrow_count: int = 0):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
        # analytics field: how many times the book has been borrowed
        self.borrow_count = borrow_count

    def borrow(self) -> bool:
        """Mark book as borrowed if available. Return True if borrowed, else False."""
        if not self.available:
            return False
        self.available = False
        self.borrow_count += 1
        return True

    def return_book(self) -> bool:
        """Mark book as available. Return True if returned, else False."""
        if self.available:
            return False
        self.available = True
        return True

    def to_dict(self) -> Dict:
        """Serialize Book to dict for JSON persistence."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
            "borrow_count": self.borrow_count
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            available=data.get("available", True),
            borrow_count=data.get("borrow_count", 0)
        )

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status} (borrowed {self.borrow_count} times)"
