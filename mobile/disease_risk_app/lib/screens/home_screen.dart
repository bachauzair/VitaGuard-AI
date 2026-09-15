import 'package:flutter/material.dart';
import 'dart:ui';
import '../api_service.dart';
import '../main.dart';
import '../l10n/app_localizations.dart';
import 'input_screen.dart';
import 'history_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<dynamic> _diseases = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadDiseases();
  }

  Future<void> _loadDiseases() async {
    try {
      final diseases = await ApiService.fetchDiseases(lang: appLocale.value.languageCode);
      setState(() {
        _diseases = diseases;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  IconData _getIconForDisease(String id) {
    switch (id) {
      case 'diabetes': return Icons.bloodtype_outlined;
      case 'heart': return Icons.favorite_border;
      case 'kidney': return Icons.water_drop_outlined;
      case 'liver': return Icons.local_hospital_outlined;
      default: return Icons.health_and_safety_outlined;
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text(l10n.appTitle, style: const TextStyle(fontWeight: FontWeight.w600, letterSpacing: 1.2)),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language, color: Colors.white),
            onSelected: (String code) {
              appLocale.value = Locale(code);
              _loadDiseases();
            },
            itemBuilder: (BuildContext context) => <PopupMenuEntry<String>>[
              const PopupMenuItem<String>(value: 'en', child: Text('English')),
              const PopupMenuItem<String>(value: 'es', child: Text('Español')),
              const PopupMenuItem<String>(value: 'fr', child: Text('Français')),
              const PopupMenuItem<String>(value: 'ur', child: Text('اردو')),
            ],
          ),
          IconButton(
            icon: const Icon(Icons.history, color: Colors.white),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const HistoryScreen()),
              );
            },
          ),
        ],
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
            top: -100,
            right: -50,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.15),
                boxShadow: [BoxShadow(color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.15), blurRadius: 100)]
              ),
            ),
          ),
          Positioned(
            bottom: -50,
            left: -100,
            child: Container(
              width: 400,
              height: 400,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Theme.of(context).colorScheme.secondary.withValues(alpha: 0.1),
                boxShadow: [BoxShadow(color: Theme.of(context).colorScheme.secondary.withValues(alpha: 0.1), blurRadius: 100)]
              ),
            ),
          ),
          SafeArea(child: _buildBody()),
        ],
      ),
    );
  }

  Widget _buildBody() {
    final l10n = AppLocalizations.of(context)!;

    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
              const SizedBox(height: 16),
              Text('Connection Error', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 8),
              Text(_error!, textAlign: TextAlign.center, style: const TextStyle(color: Colors.white54)),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: () {
                  setState(() { _isLoading = true; _error = null; });
                  _loadDiseases();
                },
                icon: const Icon(Icons.refresh),
                label: const Text('Retry Connection'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).colorScheme.surface,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              )
            ],
          ),
        ),
      );
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 20),
          Text(
            l10n.selectDiagnostics,
            style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5),
          ),
          const SizedBox(height: 8),
          Text(
            l10n.chooseModel,
            style: const TextStyle(fontSize: 15, color: Colors.white70, height: 1.4),
          ),
          const SizedBox(height: 32),
          Expanded(
            child: GridView.builder(
              physics: const BouncingScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
                childAspectRatio: 0.70,
              ),
              itemCount: _diseases.length,
              itemBuilder: (context, index) {
                final disease = _diseases[index];
                return _buildGlassCard(context, disease, index);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGlassCard(BuildContext context, dynamic disease, int index) {
    // Generate subtle gradient variations based on index
    final colors = [
      [const Color(0xFF38BDF8), const Color(0xFF0EA5E9)], // Cyan
      [const Color(0xFFF43F5E), const Color(0xFFE11D48)], // Rose
      [const Color(0xFFA855F7), const Color(0xFF9333EA)], // Purple
      [const Color(0xFF10B981), const Color(0xFF059669)], // Emerald
    ];
    final colorPair = colors[index % colors.length];

    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: Container(
        decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.03),
            borderRadius: BorderRadius.circular(24),
            border: Border.all(color: Colors.white.withValues(alpha: 0.1), width: 1.5),
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => InputScreen(diseaseConfig: disease)),
                );
              },
              highlightColor: Colors.white.withValues(alpha: 0.05),
              splashColor: colorPair[0].withValues(alpha: 0.2),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(colors: colorPair, begin: Alignment.topLeft, end: Alignment.bottomRight),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(color: colorPair[0].withValues(alpha: 0.4), blurRadius: 12, offset: const Offset(0, 4))
                        ]
                      ),
                      child: Icon(_getIconForDisease(disease['id']), size: 32, color: Colors.white),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      disease['name'],
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16, color: Colors.white, letterSpacing: 0.5),
                    ),
                    const SizedBox(height: 8),
                    Expanded(
                      child: Text(
                        disease['description'],
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 12, color: Colors.white54, height: 1.3),
                        maxLines: 3,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
    );
  }
}
