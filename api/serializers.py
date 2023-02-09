from rest_framework import serializers

from bookprog.models import Book

class BookSerializer(serializers.ModelSerializer):
    # When a book was added cannot be changed
    created = serializers.ReadOnlyField()
    
    class Meta:
        model = Book

        # the user that creates books can point to a certain influence.
        # Can always track how many followed their book to gain their influence
        fields = ['book_id','title','description','complete','created']

class BookCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # boo updated by the id
        fields = ['book_id', 'title', 'complete']
        # readonly fields
        read_only_fields = ['book_id','title','description','complete','created']


