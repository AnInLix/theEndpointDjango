from django.db import models
from django.contrib.auth.models import User

# Book
class Book(models.Model):
    # Every book gets an id automatically when added => predictable name
    book_id = models.AutoField(primary_key=True, auto_created=True)

    # Name of the book < 100 characters
    # Once title is entered, we can not change it because it will cause confusion
    # Different editions can always have a different id and a different description
    title = models.CharField(max_length=100)

    # description of the book e.g synopsis
    description = models.TextField(blank=True)

    # Time book was added - set to current time
    created = models.DateTimeField(auto_now_add=True)

    # User who added the book first
    # If user drops account, book remains => No cascading effect
    # User notes are a valuable resource for future generations => transfered to admin
    # 10NNNNNN => 1001 - 1099, 10001 - 10999, 100001 - 109999, ....
    # if we are at 109999 => 9999 + 999 + 99 users have droped accounts
    # Only admin is allowed to have id 10NNNN => 1 followed by a single 0 then the rest
    # PROTECT => do not delete user with this USERID. Why?
    #       We need to maintain users just in case they need to retrieve account.
    #       Still their thoughts get attributed to administrator 10USERID
    #       => mark them as dropped => !active
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    # If book is currently being read by user(s)
    # To enable joining a group of people to share ideas
    complete = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str({
            "title": self.title,
            "description": self.description,
            "meta": {
                "bookid": self.book_id,
                "created": self.created
            }
        })

class Progress(models.Model):
    # Every book gets an id automatically when added => predictable name
    progress_id = models.AutoField(primary_key=True, auto_created=True)

    # Can contain many entries of one book from one user
    # Progress is given by entry id
    # If many users reading same book. How to differentiate entries => user_id
    book_id = models.IntegerField(null=False)

    # Many users can read same boook => can aggregate experiences
    user_id = models.CharField(max_length=20, null=False)

    # User thoughts for this particular book entry
    thoughts = models.TextField(max_length=1000, blank=False)

    # If user completed the book
    active = models.BooleanField(default=False)

    # If reading sequentially, page number
    page = models.IntegerField(null=True)

    def __str__(self):
        return str({
            "completed": self.completed,
            "user": self.user_id,
            "thoughts": self.thoughts,
            "page": self.page
        })
