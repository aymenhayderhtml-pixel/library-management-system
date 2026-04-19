import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import '../book_repository.dart';
import '../ui/widgets/app_text_field.dart';

/// AddBookScreen allows users to add a new book via a validated form.
class AddBookScreen extends StatefulWidget {
  const AddBookScreen({super.key});

  @override
  State<AddBookScreen> createState() => _AddBookScreenState();
}

class _AddBookScreenState extends State<AddBookScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _authorController = TextEditingController();
  final _categoryController = TextEditingController();
  final _quantityController = TextEditingController();

  bool _isSaving = false;

  @override
  void dispose() {
    _titleController.dispose();
    _authorController.dispose();
    _categoryController.dispose();
    _quantityController.dispose();
    super.dispose();
  }

  bool get isFormValid {
    final title = _titleController.text.trim();
    final author = _authorController.text.trim();
    final quantity = int.tryParse(_quantityController.text.trim()) ?? 0;
    return title.isNotEmpty &&
        author.isNotEmpty &&
        quantity >= 1 &&
        (_categoryController.text.trim().isEmpty ||
            _categoryController.text.trim().isNotEmpty);
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isSaving = true);
    try {
      final book = Book(
        id: const Uuid().v4(),
        title: _titleController.text.trim(),
        author: _authorController.text.trim(),
        category: _categoryController.text.trim().isEmpty
            ? null
            : _categoryController.text.trim(),
        quantity: int.parse(_quantityController.text.trim()),
      );
      await BookRepository().addBook(book);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Book added successfully')),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error adding book: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _isSaving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add Book')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              AppTextField(
                controller: _titleController,
                label: 'Title',
                maxLength: 200,
                validator: (v) => v!.trim().isEmpty ? 'Title is required' : null,
              ),
              const SizedBox(height: 12),
              AppTextField(
                controller: _authorController,
                label: 'Author',
                maxLength: 100,
                validator: (v) => v!.trim().isEmpty ? 'Author is required' : null,
              ),
              const SizedBox(height: 12),
              AppTextField(
                controller: _categoryController,
                label: 'Category (optional)',
                maxLength: 50,
                validator: (v) => null, // optional
              ),
              const SizedBox(height: 12),
              AppTextField(
                controller: _quantityController,
                label: 'Quantity',
                keyboardType: TextInputType.number,
                maxLength: 5,
                validator: (v) {
                  final val = int.tryParse(v!.trim());
                  return val != null && val >= 1 ? null : 'Quantity must be at least 1';
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: isFormValid && !_isSaving ? _save : null,
                child: _isSaving
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Save'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// Reusable text form field widget to reduce boilerplate.
class AppTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String label;
  final int? maxLength;
  final TextInputType keyboardType;
  final String? Function(String?)? validator;

  const AppTextField({
    required this.controller,
    required this.label,
    this.maxLength,
    this.keyboardType = TextInputType.text,
    this.validator,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      maxLines: maxLength != null ? 1 : null,
      maxLength: maxLength,
      keyboardType: keyboardType,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        counterText: '',
      ),
      validator: validator,
    );
  }
}
