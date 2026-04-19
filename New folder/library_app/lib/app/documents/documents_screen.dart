// MODULE: documents
// PURPOSE: Documents & Reports module main screen (placeholder)
// DEPENDS ON: nothing yet
// SAFE TO MODIFY: YES
// DO NOT TOUCH: books/, members/, loans/, db/

import 'package:flutter/material.dart';

class DocumentsScreen extends StatelessWidget {
  const DocumentsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.picture_as_pdf, size: 64, color: Colors.red),
            SizedBox(height: 16),
            Text('📄 Documents Module', style: TextStyle(fontSize: 20)),
            Text('Coming in Phase 5', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
