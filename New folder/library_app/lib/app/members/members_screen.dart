// MODULE: members
// PURPOSE: Members module main screen (placeholder)
// DEPENDS ON: nothing yet
// SAFE TO MODIFY: YES
// DO NOT TOUCH: loans/, books/, db/

import 'package:flutter/material.dart';

class MembersScreen extends StatelessWidget {
  const MembersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.people, size: 64, color: Colors.green),
            SizedBox(height: 16),
            Text('👥 Members Module', style: TextStyle(fontSize: 20)),
            Text('Coming in Phase 2', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
