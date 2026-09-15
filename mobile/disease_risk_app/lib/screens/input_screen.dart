import 'package:flutter/material.dart';
import 'dart:ui';
import '../api_service.dart';
import 'result_screen.dart';

class InputScreen extends StatefulWidget {
  final dynamic diseaseConfig;

  const InputScreen({super.key, required this.diseaseConfig});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, dynamic> _formData = {};
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    // Initialize default values for select fields
    for (var field in widget.diseaseConfig['fields']) {
      if (field['type'] == 'select' && field['options'] != null && field['options'].isNotEmpty) {
        _formData[field['name']] = field['options'][0]['value'];
      }
    }
  }

  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();

    setState(() => _isLoading = true);

    try {
      final result = await ApiService.predictRisk(
        widget.diseaseConfig['endpoint'], 
        _formData
      );
      
      if (!mounted) return;
      
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            resultData: result,
            diseaseName: widget.diseaseConfig['name'],
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.toString(), style: const TextStyle(color: Colors.white)),
          behavior: SnackBarBehavior.floating,
          backgroundColor: Colors.redAccent.withValues(alpha: 0.9),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        )
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Widget _buildField(dynamic field) {
    final theme = Theme.of(context);
    
    if (field['type'] == 'select') {
      return Padding(
        padding: const EdgeInsets.only(bottom: 20.0),
        child: DropdownButtonFormField<dynamic>(
          dropdownColor: theme.colorScheme.surface,
          decoration: InputDecoration(
            labelText: field['label'],
            labelStyle: const TextStyle(color: Colors.white70),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(color: theme.colorScheme.primary, width: 1.5),
            ),
            filled: true,
            fillColor: Colors.white.withValues(alpha: 0.05),
            contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
          ),
          style: const TextStyle(color: Colors.white, fontSize: 16),
          icon: Icon(Icons.arrow_drop_down_circle, color: theme.colorScheme.primary.withValues(alpha: 0.7)),
          value: _formData[field['name']],
          items: (field['options'] as List).map((option) {
            return DropdownMenuItem<dynamic>(
              value: option['value'],
              child: Text(option['label'].toString()),
            );
          }).toList(),
          onChanged: (value) {
            setState(() { _formData[field['name']] = value; });
          },
          onSaved: (value) {
            _formData[field['name']] = value;
          },
        ),
      );
    } else {
      return Padding(
        padding: const EdgeInsets.only(bottom: 20.0),
        child: TextFormField(
          style: const TextStyle(color: Colors.white, fontSize: 16),
          decoration: InputDecoration(
            labelText: field['label'],
            hintText: field['hint'],
            hintStyle: TextStyle(color: Colors.white.withValues(alpha: 0.3)),
            labelStyle: const TextStyle(color: Colors.white70),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(color: theme.colorScheme.primary, width: 1.5),
            ),
            filled: true,
            fillColor: Colors.white.withValues(alpha: 0.05),
            contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          validator: (value) {
            if (value == null || value.isEmpty) return 'Please enter ${field['label']}';
            if (double.tryParse(value) == null) return 'Please enter a valid number';
            return null;
          },
          onSaved: (value) {
            if (value != null) {
               final numValue = num.tryParse(value);
               _formData[field['name']] = numValue;
            }
          },
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final fields = widget.diseaseConfig['fields'] as List;
    final theme = Theme.of(context);

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text('${widget.diseaseConfig['name']} Assessment', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
        iconTheme: const IconThemeData(color: Colors.white),
        flexibleSpace: ClipRect(
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: Container(color: Colors.transparent),
          ),
        ),
      ),
      body: Stack(
        children: [
          // Ambient Background Gradients
          Positioned(
            top: 100,
            left: -50,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: theme.colorScheme.primary.withValues(alpha: 0.1),
                boxShadow: [BoxShadow(color: theme.colorScheme.primary.withValues(alpha: 0.1), blurRadius: 100)]
              ),
            ),
          ),
          SafeArea(
            child: _isLoading 
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const CircularProgressIndicator(color: Colors.white),
                      const SizedBox(height: 24),
                      Text('Running Explainable AI Models...', 
                        style: TextStyle(fontSize: 18, color: theme.colorScheme.primary, fontWeight: FontWeight.w600)
                      ),
                    ],
                  )
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 10),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const SizedBox(height: 10),
                        const Text('Clinical Metrics', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5)),
                        const SizedBox(height: 8),
                        const Text('Please input the required physiological parameters for the neural network.', style: TextStyle(color: Colors.white54, fontSize: 14)),
                        const SizedBox(height: 30),
                        
                        // Glassmorphism Form Container
                        ClipRRect(
                          borderRadius: BorderRadius.circular(24),
                          child: BackdropFilter(
                            filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                            child: Container(
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha: 0.02),
                                borderRadius: BorderRadius.circular(24),
                                border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
                              ),
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                children: fields.map((f) => _buildField(f)).toList(),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 120), // Space for bottom button
                      ],
                    ),
                  ),
                ),
          ),
        ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: _isLoading ? null : Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Container(
          width: double.infinity,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: theme.colorScheme.primary.withValues(alpha: 0.3),
                blurRadius: 20,
                offset: const Offset(0, 10),
              )
            ]
          ),
          child: ElevatedButton(
            onPressed: _submitForm,
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 20),
              backgroundColor: theme.colorScheme.primary,
              foregroundColor: Colors.white,
              elevation: 0,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            ),
            child: const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.auto_awesome, size: 24),
                SizedBox(width: 12),
                Text('Generate AI Analysis', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, letterSpacing: 0.5)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
