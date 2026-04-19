import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import '../ui/widgets/app_text_field.dart';

/// Book model for library entries.
class Book {
  final String id;
  final String title;
  final List<String> authors;
  final String? summary;
  final List<String> subjects;
  final List<String> languages;
  final int downloadCount;
  final String? formatsUrl;

  Book({
    required this.id,
    required this.title,
    required this.authors,
    this.summary,
    this.subjects = const [],
    this.languages = const [],
    this.downloadCount = 0,
    this.formatsUrl,
  });

  factory Book.fromJson(Map<String, dynamic> json) {
    final formats = json['formats'] as Map<String, dynamic>? ?? {};
    String? url;
    // Prefer text/plain; charset=utf-8, fallback to text/html, then epub
    url = formats['text/plain; charset=utf-8'] as String? ??
        formats['text/html'] as String? ??
        formats['application/epub+zip'] as String?;

    return Book(
      id: json['id']?.toString() ?? const Uuid().v4(),
      title: json['title'] as String? ?? '',
      authors: (json['authors'] as List? ?? [])
          .map((a) => a is Map ? a['name']?.toString() ?? '' : a.toString())
          .where((a) => a.isNotEmpty)
          .cast<String>()
          .toList(),
      summary: json['summary'] as String?,
      subjects: (json['subjects'] as List? ?? []).cast<String>(),
      languages: (json['languages'] as List? ?? []).cast<String>(),
      downloadCount: json['download_count'] as int? ?? 0,
      formatsUrl: url?.isNotEmpty == true ? url : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'authors': authors,
      'summary': summary,
      'subjects': subjects,
      'languages': languages,
      'download_count': downloadCount,
      'formats_url': formatsUrl,
    };
  }
}

class BookRepository {
  static const _baseUrl = 'https://gutendex.com/books';
  final http.Client _client;

  BookRepository({http.Client? client}) : _client = client ?? http.Client();

  Future<List<Book>> getAllBooks() async {
    return _fetchBooks('$_baseUrl?languages=en&copyright=false&sort=popular&limit=32');
  }

  Future<List<Book>> searchBooks(String query) async {
    final url = '$_baseUrl?q=$query&languages=en&copyright=false&sort=popular&limit=32';
    return _fetchBooks(url);
  }

  Future<List<Book>> _fetchBooks(String url) async {
    List<Book> books = [];
    String? nextUrl = url;

    while (nextUrl != null) {
      final response = await _client.get(Uri.parse(nextUrl));
      if (response.statusCode != 200) {
        throw Exception('Failed to fetch books: ${response.statusCode}');
      }
      final data = json.decode(response.body) as Map<String, dynamic>;
      books.addAll((data['results'] as List).map((item) => Book.fromJson(item)));
      nextUrl = data['next'] as String?;
      // Respect API with small delay between pages
      await Future.delayed(const Duration(seconds: 1));
    }
    return books;
  }

  Future<Book> getBookById(String id) async {
    final url = '$_baseUrl/$id';
    final response = await _client.get(Uri.parse(url));
    if (response.statusCode != 200) {
      throw Exception('Failed to fetch book: ${response.statusCode}');
    }
    return Book.fromJson(json.decode(response.body) as Map<String, dynamic>);
  }

  Future<void> addBook(Book book) async {
    // Note: Gutendex is read-only API; this would require a backend service
    // For local persistence, you'd post to your own backend API instead
    throw UnimplementedError('Gutendex is read-only; implement your own backend API for adding books');
  }

  void dispose() {
    _client.close();
  }
}

// Convenience access to repository instance
final bookRepository = BookRepository();
