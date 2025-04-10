import csv
import json
from datetime import datetime

def load_books():
    """Load books from the CSV file, creating it if necessary."""
    try:
        with open('library.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        with open('library.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Year', 'Genre', 'Rating'])
            writer.writeheader()
        return []

def save_books(books):
    """Save the list of books to the CSV file."""
    with open('library.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Year', 'Genre', 'Rating'])
        writer.writeheader()
        writer.writerows(books)

def add_book():
    """Prompt the user to add a new book with validation."""
    books = load_books()
    
    # Title (required)
    title = input("Enter the book's title: ").strip()
    while not title:
        print("Title is required.")
        title = input("Enter the book's title: ").strip()
    
    # Author (required)
    author = input("Enter the author's name: ").strip()
    while not author:
        print("Author is required.")
        author = input("Enter the author's name: ").strip()
    
    # Year (optional with validation)
    year = ''
    while True:
        year_input = input("Enter the publication year (optional): ").strip()
        if not year_input:
            break
        try:
            year = int(year_input)
            current_year = datetime.now().year
            if year < 0 or year > current_year:
                print(f"Year must be between 0 and {current_year}.")
            else:
                year = str(year)
                break
        except ValueError:
            print("Please enter a valid integer for the year.")
    
    # Genre (optional)
    genre = input("Enter the genre (optional): ").strip()
    
    # Rating (optional with validation)
    rating = ''
    while True:
        rating_input = input("Enter the rating (0-5, optional): ").strip()
        if not rating_input:
            break
        try:
            rating_val = float(rating_input)
            if 0.0 <= rating_val <= 5.0:
                rating = str(rating_val)
                break
            else:
                print("Rating must be between 0 and 5.")
        except ValueError:
            print("Please enter a valid number for the rating.")
    
    # Add the new book
    new_book = {
        'Title': title,
        'Author': author,
        'Year': year,
        'Genre': genre,
        'Rating': rating
    }
    books.append(new_book)
    save_books(books)
    print(f"Book '{title}' added successfully!")

def list_books():
    """Display all books in the library."""
    books = load_books()
    if not books:
        print("Your library is empty.")
        return
    print("\n--- Your Library ---")
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - Genre: {book['Genre']}, Rating: {book['Rating']}")
    print(f"Total books: {len(books)}\n")

def search_books():
    """Search for books by any field with partial matching."""
    search_term = input("Enter a search term: ").strip().lower()
    books = load_books()
    matches = []
    for book in books:
        if (search_term in book['Title'].lower() or
            search_term in book['Author'].lower() or
            search_term in book['Year'].lower() or
            search_term in book['Genre'].lower() or
            search_term in book['Rating'].lower()):
            matches.append(book)
    if not matches:
        print("No matching books found.")
        return
    print(f"\nFound {len(matches)} matching books:")
    for idx, book in enumerate(matches, 1):
        print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']}) - Genre: {book['Genre']}, Rating: {book['Rating']}")

def delete_book():
    """Delete books by searching and selecting from matches."""
    books = load_books()
    search_term = input("Enter the title to delete: ").strip().lower()
    matches = [book for book in books if search_term in book['Title'].lower()]
    
    if not matches:
        print("No books found with that title.")
        return
    
    print("Matching books:")
    for idx, book in enumerate(matches, 1):
        print(f"{idx}. {book['Title']} by {book['Author']} ({book['Year']})")
    
    while True:
        choice = input("Enter numbers to delete (comma-separated), 'all', or 'cancel': ").strip().lower()
        if choice == 'cancel':
            print("Deletion cancelled.")
            return
        elif choice == 'all':
            books = [book for book in books if book not in matches]
            save_books(books)
            print(f"Deleted {len(matches)} books.")
            return
        else:
            try:
                indices = [int(i.strip()) - 1 for i in choice.split(',')]
                valid = [i for i in indices if 0 <= i < len(matches)]
                if not valid:
                    print("No valid indices entered.")
                    continue
                to_delete = [matches[i] for i in valid]
                books = [book for book in books if book not in to_delete]
                save_books(books)
                print(f"Deleted {len(valid)} books.")
                return
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")

def generate_reports():
    """Generate and display library reports."""
    books = load_books()
    if not books:
        print("Your library is empty. No reports to generate.")
        return
    
    # Genre Report
    genre_counts = {}
    for book in books:
        genre = book['Genre'] if book['Genre'] else 'Uncategorized'
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    print("\n--- Genre Report ---")
    for genre, count in genre_counts.items():
        print(f"{genre}: {count} book(s)")
    
    # Average Rating
    total = 0
    count = 0
    for book in books:
        if book['Rating']:
            try:
                total += float(book['Rating'])
                count += 1
            except ValueError:
                pass
    avg = total / count if count > 0 else 0
    print(f"\n--- Average Rating ---\n{avg:.2f} (from {count} rated books)")
    
    # Oldest and Newest Books
    years = []
    for book in books:
        if book['Year']:
            try:
                years.append(int(book['Year']))
            except ValueError:
                pass
    if years:
        oldest = min(years)
        newest = max(years)
        oldest_books = [book for book in books if book['Year'] == str(oldest)]
        newest_books = [book for book in books if book['Year'] == str(newest)]
        print("\n--- Oldest Book(s) ---")
        for book in oldest_books:
            print(f"{book['Title']} by {book['Author']} ({book['Year']})")
        print("\n--- Newest Book(s) ---")
        for book in newest_books:
            print(f"{book['Title']} by {book['Author']} ({book['Year']})")
    else:
        print("\nNo publication years available for oldest/newest report.")

def export_library():
    """Export the library to a JSON or text file."""
    books = load_books()
    if not books:
        print("Your library is empty. Nothing to export.")
        return
    
    fmt = input("Enter export format (json/txt): ").strip().lower()
    if fmt not in ['json', 'txt']:
        print("Invalid format. Use 'json' or 'txt'.")
        return
    
    filename = input("Enter filename: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        if fmt == 'json':
            with open(filename, 'w') as f:
                json.dump(books, f, indent=4)
        else:
            with open(filename, 'w') as f:
                for book in books:
                    f.write(f"Title: {book['Title']}\n")
                    f.write(f"Author: {book['Author']}\n")
                    f.write(f"Year: {book['Year']}\n")
                    f.write(f"Genre: {book['Genre']}\n")
                    f.write(f"Rating: {book['Rating']}\n\n")
        print(f"Library exported to {filename} successfully.")
    except Exception as e:
        print(f"Error exporting: {e}")

def import_library():
    """Import books from a JSON or text file."""
    fmt = input("Enter import format (json/txt): ").strip().lower()
    if fmt not in ['json', 'txt']:
        print("Invalid format. Use 'json' or 'txt'.")
        return
    
    filename = input("Enter filename: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return
    
    try:
        existing = load_books()
        new_books = []
        
        if fmt == 'json':
            with open(filename, 'r') as f:
                imported = json.load(f)
                for book in imported:
                    if 'Title' in book and 'Author' in book:
                        new_books.append({
                            'Title': book['Title'],
                            'Author': book['Author'],
                            'Year': book.get('Year', ''),
                            'Genre': book.get('Genre', ''),
                            'Rating': book.get('Rating', '')
                        })
        else:
            with open(filename, 'r') as f:
                current = {}
                for line in f:
                    line = line.strip()
                    if line.startswith('Title: '):
                        current['Title'] = line[7:]
                    elif line.startswith('Author: '):
                        current['Author'] = line[8:]
                    elif line.startswith('Year: '):
                        current['Year'] = line[6:]
                    elif line.startswith('Genre: '):
                        current['Genre'] = line[7:]
                    elif line.startswith('Rating: '):
                        current['Rating'] = line[8:]
                    elif line == '':
                        if 'Title' in current and 'Author' in current:
                            new_books.append(current)
                        current = {}
                if current and 'Title' in current and 'Author' in current:
                    new_books.append(current)
        
        combined = existing + new_books
        save_books(combined)
        print(f"Imported {len(new_books)} books successfully.")
    except Exception as e:
        print(f"Error importing: {e}")

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\n--- Personal Library Manager ---")
        print("1. Add a book")
        print("2. List all books")
        print("3. Search for a book")
        print("4. Delete a book")
        print("5. Generate reports")
        print("6. Export library")
        print("7. Import library")
        print("8. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            search_books()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            generate_reports()
        elif choice == '6':
            export_library()
        elif choice == '7':
            import_library()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1-8.")

if __name__ == "__main__":
    main_menu()