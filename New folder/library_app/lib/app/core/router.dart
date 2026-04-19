// MODULE: core
// PURPOSE: App routing and navigation
// DEPENDS ON: books/, members/, loans/, documents/ (placeholder screens)
// SAFE TO MODIFY: Yes, add more tabs or routes here
// DO NOT TOUCH: db/

import 'package:flutter/material.dart';

import '../books/books_screen.dart';
import '../documents/documents_screen.dart';
import '../loans/loans_screen.dart';
import '../members/members_screen.dart';

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = [
    BooksScreen(),
    MembersScreen(),
    LoansScreen(),
    DocumentsScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.book), label: 'Books'),
          BottomNavigationBarItem(icon: Icon(Icons.people), label: 'Members'),
          BottomNavigationBarItem(
            icon: Icon(Icons.swap_horiz),
            label: 'Loans',
          ),
          BottomNavigationBarItem(icon: Icon(Icons.folder), label: 'Documents'),
        ],
      ),
    );
  }
}
