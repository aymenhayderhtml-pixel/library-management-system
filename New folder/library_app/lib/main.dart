import 'package:flutter/material.dart';

import 'app/db/database.dart';
import 'app/core/router.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final db = AppDatabase();
  final bookCount = await db.select(db.books).get();
  // ignore: avoid_print
  print('✅ Database ready. Books count: ${bookCount.length}');
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Library Manager',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const MainNavigation(),
    );
  }
}
