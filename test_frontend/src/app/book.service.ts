import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Book } from './book.model';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private apiUrl = 'http://127.0.0.1:5000/books';

  constructor(private http: HttpClient) {}

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>('http://127.0.0.1:5000/books');
  }

  addBook(book: Book): Observable<Book> {
    return this.http.post<Book>('http://127.0.0.1:5000/books', book);
  }

  updateBook(id: number, book: Book): Observable<Book> {
    return this.http.put<Book>(`http://127.0.0.1:5000/books/${id}`, book);
  }

  deleteBook(id: number): Observable<any> {
    return this.http.delete(`http://127.0.0.1:5000/books/${id}`);
  }
}