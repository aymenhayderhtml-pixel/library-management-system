import 'package:flutter/material.dart';

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
