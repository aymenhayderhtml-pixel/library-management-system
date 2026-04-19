import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:library_app/app/books/books_screen.dart';

void main() {
  testWidgets('Library app smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MaterialApp(home: BooksScreen()));

    // Verify that the BooksScreen loads without crashing.
    expect(find.text('Books'), findsOneWidget);
  });
}
