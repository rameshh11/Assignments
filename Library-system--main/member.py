"""
Name: Replace with your name
Date: 2025-11-19
Assignment: Library System - member.py
"""

from typing import List, Dict

class Member:
    def __init__(self, name: str, member_id: str, borrowed_books: List[str] = None):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def borrow_book(self, isbn: str) -> None:
        """Add ISBN to the member's borrowed list (no validation here)."""
        if isbn not in self.borrowed_books:
            self.borrowed_books.append(isbn)

    def return_book(self, isbn: str) -> bool:
        """Remove ISBN from borrowed_books. Returns True if removed, False if not found."""
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False

    def list_books(self) -> List[str]:
        """Return the list of currently borrowed ISBNs."""
        return list(self.borrowed_books)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            name=data["name"],
            member_id=data["member_id"],
            borrowed_books=data.get("borrowed_books", [])
        )

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_books)}"
