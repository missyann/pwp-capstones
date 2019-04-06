class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('Your email has been updated')

    def __repr__(self):
        return 'User ' + self.name + ', email: ' + self.email + ', number of books read: ' + str(len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        ratings = [rating for rating in self.books.values() if rating is not None]
        if len(ratings) > 0:
            return sum(ratings) / len(ratings)  
        else:
            return 0  


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        
    def get_title(self):
        return self.title 

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("This book's ISBN has been updated")

    def add_rating(self, rating):
        if rating is not None and rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print('Invalid Rating')    

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))     
                       


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):   
        return self.title + ' by ' + self.author


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ', a ' + self.level + ' manual on ' + self.subject             


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbns = []

    def create_book(self, title, isbn):
        self.check_dupe_isbn(isbn)
        return Book(title, isbn)
    
    def create_novel(self, title, author, isbn):
        self.check_dupe_isbn(isbn)
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        self.check_dupe_isbn(isbn)
        return Non_Fiction(title, subject, level, isbn)

    def check_dupe_isbn(self, isbn):
        if isbn in self.isbns:
            print('The ISBN already exists:' + str(isbn))
        else:
            self.isbns.append(isbn)    

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print('No user with email ' + email + ' !')
            return

        user = self.users[email]
        user.read_book(book, rating)

        book.add_rating(rating)

        if book not in self.books:
            self.books[book] = 1
        else:
            self.books[book] += 1            

    def add_user(self, name, email, user_books=None):
        if not self.valid_email(email): 
            return         

        if email in self.users:
            print('The user already exists: ' + email)
            return    

        user = User(name, email)
        self.users[email] = user

        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)  

    def valid_email(self, email):
        has_correct_ending = email.endswith('.org') or email.endswith('.com') or email.endswith('.edu')
        has_at_sign = email.count('@')

        if has_correct_ending and has_at_sign:
            return True
        else: 
            print ('Email ' + email + ' is not a valid email')
            return False
                  

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        new_dict = {v:k for k,v in self.books.items()} #this line flips dictionaries around (see lines 140 and 141 for examples)
        mrb_res = max(new_dict)
        return new_dict[mrb_res]

        #self.books = {gone with the wind : 10, charolettes web: 6}
        #new_dict = {10 : gone with the wind, 6 : charloettes web}
    
    def highest_rated_book(self):  #this is moving the key (book) and placing as value in new_dict. book.get_average_rating becomes the key
        new_dict = {}
        for book in self.books:
            new_dict[book.get_average_rating()] = book
        average_rating = max(new_dict)    
        return new_dict[average_rating]      

    def most_positive_user(self): #this is moving the value (user) as the value in new_dict. users.get_average_rating is the new key of new_dict
        new_dict = {}
        for user in self.users.values():
            new_dict[user.get_average_rating()] = user
        highest_rating = max(new_dict)
        return new_dict[highest_rating]

     
# For most_read_book, highest_rated_book, and most_positive_user these dictionaries could potentialy have dupliated values in the original dictionary.
# When the dictioaries are flipped, the values now become the keys and there can only be one unique key per value
# So if there are muliple values from the original dictionary, the last value to take the place of the key will win. 
# Meaning that not all information will be display. 
# In a real world scenario, we would need to speak with people who want this program to see how they would want this information to display.      

   


