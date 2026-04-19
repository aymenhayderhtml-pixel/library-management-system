// MODULE: loans
// PURPOSE: Loans module main screen (placeholder)
// DEPENDS ON: nothing yet
// SAFE TO MODIFY: YES
// DO NOT TOUCH: books/, members/, db/

import 'package:flutter/material.dart';

class LoansScreen extends StatelessWidget {
  const LoansScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.swap_horiz, size: 64, color: Colors.orange),
            SizedBox(height: 16),
            Text('🔄 Loans Module', style: TextStyle(fontSize: 20)),
            Text('Coming in Phase 3', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
