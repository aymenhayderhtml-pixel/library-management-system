// MODULE: books
// PURPOSE: Books module main screen (placeholder)
// DEPENDS ON: nothing yet
// SAFE TO MODIFY: YES
// DO NOT TOUCH: loans/, members/, db/

import 'package:flutter/material.dart';

class BooksScreen extends StatelessWidget {
  const BooksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.book, size: 64, color: Colors.blue),
            SizedBox(height: 16),
            Text('📚 Books Module', style: TextStyle(fontSize: 20)),
            Text('Coming in Phase 1', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
