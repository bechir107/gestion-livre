import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService } from './book.service';
import { Book } from './book.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  books: Book[] = [];

  book: Book = {
    title: '',
    author: '',
    year: new Date().getFullYear()
  };

  editingId: number | null = null;
  errorMessage = '';
  successMessage = '';

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
  this.bookService.getBooks().subscribe({
    next: (data: any) => {
      console.log('Réponse reçue :', data);

      this.books = Array.isArray(data) ? data : [];

      console.log('Nombre de livres :', this.books.length);
    },
    error: (err) => {
      console.error('Erreur de chargement :', err);
    }
  });
}

  onSubmit(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.book.title.trim() || !this.book.author.trim()) {
      this.errorMessage = 'Veuillez remplir tous les champs.';
      return;
    }

    const request = this.editingId === null
      ? this.bookService.addBook(this.book)
      : this.bookService.updateBook(this.editingId, this.book);

    request.subscribe({
      next: () => {
        this.successMessage = this.editingId === null
          ? 'Livre ajouté avec succès.'
          : 'Livre modifié avec succès.';

        this.resetForm();
        this.loadBooks();
      },
      error: (err) => {
        console.error('Erreur lors de l’enregistrement :', err);
        this.errorMessage = 'Échec de l’enregistrement du livre.';
      }
    });
  }

  editBook(book: Book): void {
    this.book = { ...book };
    this.editingId = book.id ?? null;
    this.errorMessage = '';
    this.successMessage = '';
  }

  deleteBook(id: number): void {
    if (!confirm('Voulez-vous supprimer ce livre ?')) {
      return;
    }

    this.bookService.deleteBook(id).subscribe({
      next: () => {
        this.successMessage = 'Livre supprimé avec succès.';
        this.loadBooks();
      },
      error: (err) => {
        console.error('Erreur de suppression :', err);
        this.errorMessage = 'La suppression a échoué.';
      }
    });
  }

  resetForm(): void {
    this.book = {
      title: '',
      author: '',
      year: new Date().getFullYear()
    };

    this.editingId = null;
    this.errorMessage = '';
  }
}