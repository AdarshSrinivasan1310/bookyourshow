import tkinter as tk
from tkinter import messagebox

class Movie:
    def __init__(self, title, duration, genre):
        self.title = title
        self.duration = duration
        self.genre = genre

class Theater:
    def __init__(self, name, total_rows, total_cols):
        self.name = name
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.seats = {
            movie.title: [['Available' for _ in range(total_cols)] for _ in range(total_rows)]
            for movie in system.get_movie_list()
        }

    def is_seat_available(self, movie_title, row, col):
        return self.seats[movie_title][row][col] == 'Available'

    def book_seats(self, movie, customer_name, selected_seats):
        for (row, col) in selected_seats:
            if self.seats[movie.title][row][col] == 'Booked':
                return False
        for (row, col) in selected_seats:
            self.seats[movie.title][row][col] = 'Booked'
        return True

class TreeNode:
    def __init__(self, movie):
        self.movie = movie
        self.left = None
        self.right = None

class MovieTree:
    def __init__(self):
        self.root = None

    def insert(self, movie):
        if self.root is None:
            self.root = TreeNode(movie)
        else:
            self._insert_recursive(self.root, movie)

    def _insert_recursive(self, node, movie):
        if movie.title < node.movie.title:
            if node.left is None:
                node.left = TreeNode(movie)
            else:
                self._insert_recursive(node.left, movie)
        elif movie.title > node.movie.title:
            if node.right is None:
                node.right = TreeNode(movie)
            else:
                self._insert_recursive(node.right, movie)

    def search(self, title):
        return self._search_recursive(self.root, title)

    def _search_recursive(self, node, title):
        if node is None:
            return None
        if title == node.movie.title:
            return node.movie
        elif title < node.movie.title:
            return self._search_recursive(node.left, title)
        else:
            return self._search_recursive(node.right, title)

class QueueNode:
    def __init__(self, customer_name, movie_title, seats):
        self.customer_name = customer_name
        self.movie_title = movie_title
        self.seats = seats
        self.next = None

class BookingQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, customer_name, movie_title, seats):
        new_node = QueueNode(customer_name, movie_title, seats)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp

    def is_empty(self):
        return self.front is None

class MovieBookingSystem:
    def __init__(self):
        self.movies = []
        self.theaters = []
        self.movie_tree = MovieTree()
        self.booking_queue = BookingQueue()

    def add_movie(self, movie):
        self.movies.append(movie)
        self.movie_tree.insert(movie)

    def add_theater(self, theater):
        self.theaters.append(theater)

    def get_movie_list(self):
        return self.movies

    def get_theater_list(self):
        return self.theaters

    def book_ticket(self, customer_name, movie_title, seats):
        self.booking_queue.enqueue(customer_name, movie_title, seats)

    def process_all_bookings(self):
        bookings_processed = []
        while not self.booking_queue.is_empty():
            booking = self.booking_queue.dequeue()
            bookings_processed.append(f"{booking.customer_name} booked {self.format_seat_numbers(booking.seats)} for movie {booking.movie_title}")
        return bookings_processed

    def format_seat_numbers(self, seats):
        return ', '.join([f"{r + 1},{c + 1}" for (r, c) in seats])

system = MovieBookingSystem()

movie1 = Movie("Inception", 148, "Sci-Fi")
movie2 = Movie("The Dark Knight", 152, "Action")
system.add_movie(movie1)
system.add_movie(movie2)

theater1 = Theater("PVR Cinemas", 5, 5)
theater2 = Theater("INOX", 5, 5)
system.add_theater(theater1)
system.add_theater(theater2)

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Booking System with Seat Selection")
        
        tk.Label(root, text="Select Movie:").grid(row=0, column=0)
        self.movie_var = tk.StringVar()
        self.movie_menu = tk.OptionMenu(root, self.movie_var, *[movie.title for movie in system.get_movie_list()])
        self.movie_menu.grid(row=0, column=1)

        tk.Label(root, text="Select Theater:").grid(row=1, column=0)
        self.theater_var = tk.StringVar()
        self.theater_menu = tk.OptionMenu(root, self.theater_var, *[theater.name for theater in system.get_theater_list()])
        self.theater_menu.grid(row=1, column=1)

        tk.Label(root, text="Customer Name:").grid(row=2, column=0)
        self.customer_name = tk.Entry(root)
        self.customer_name.grid(row=2, column=1)

        tk.Label(root, text="Select Seats:").grid(row=3, column=0)

        self.seat_buttons = []
        self.selected_seats = []

        self.book_button = tk.Button(root, text="Book Seats", command=self.book_seats)
        self.book_button.grid(row=4, column=1)

        self.finish_button = tk.Button(root, text="Finish Booking", command=self.finish_booking)
        self.finish_button.grid(row=4, column=2)

        self.theater_var.trace('w', self.display_seats)

    def display_seats(self, *args):
        theater_name = self.theater_var.get()
        selected_theater = next((theater for theater in system.get_theater_list() if theater.name == theater_name), None)
        
        if selected_theater:
            for button in self.seat_buttons:
                button.grid_forget()
            self.seat_buttons.clear()

            selected_movie_title = self.movie_var.get()
            for row in range(selected_theater.total_rows):
                for col in range(selected_theater.total_cols):
                    if selected_theater.is_seat_available(selected_movie_title, row, col):
                        btn = tk.Button(self.root, text=f"{row+1},{col+1}", width=5, command=lambda r=row, c=col: self.toggle_seat(r, c))
                    else:
                        btn = tk.Button(self.root, text=f"{row+1},{col+1}", width=5, state='disabled')
                    btn.grid(row=row+6, column=col)
                    self.seat_buttons.append(btn)
            self.selected_seats.clear()

    def toggle_seat(self, row, col):
        seat = (row, col)
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
        else:
            self.selected_seats.append(seat)

    def book_seats(self):
        movie_title = self.movie_var.get()
        theater_name = self.theater_var.get()
        customer_name = self.customer_name.get()

        if not movie_title or not theater_name or not customer_name or len(self.selected_seats) == 0:
            messagebox.showerror("Input Error", "Please provide valid inputs and select seats.")
            return

        selected_movie = system.movie_tree.search(movie_title)
        selected_theater = next((theater for theater in system.get_theater_list() if theater.name == theater_name), None)

        if selected_theater and selected_movie:
            success = selected_theater.book_seats(selected_movie, customer_name, self.selected_seats)
            if success:
                system.book_ticket(customer_name, movie_title, self.selected_seats)
                messagebox.showinfo("Success", f"Seats {self.format_seat_numbers(self.selected_seats)} successfully booked for {customer_name}.")
                self.display_seats()
            else:
                messagebox.showerror("Booking Error", "Error: One or more selected seats are already booked for this movie.")
        else:
            messagebox.showerror("Selection Error", "Invalid movie or theater selection.")

    def format_seat_numbers(self, seats):
        return ', '.join([f"{r + 1},{c + 1}" for (r, c) in seats])

    def finish_booking(self):
        bookings_processed = system.process_all_bookings()
        if bookings_processed:
            messagebox.showinfo("Finished", "Booking process completed:\n" + "\n".join(bookings_processed))
        else:
            messagebox.showinfo("No Bookings", "There are no bookings to process.")

root = tk.Tk()
app = MovieBookingApp(root)
root.mainloop()
