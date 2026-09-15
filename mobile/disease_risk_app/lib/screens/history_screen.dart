import 'package:flutter/material.dart';
import 'dart:ui';
import '../services/history_service.dart';
import 'package:intl/intl.dart';
import 'result_screen.dart';
import '../l10n/app_localizations.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<Map<String, dynamic>> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final history = await HistoryService.getHistory();
    setState(() {
      _history = history;
      _isLoading = false;
    });
  }

  Future<void> _clearHistory() async {
    await HistoryService.clearHistory();
    _loadHistory();
  }

  Color _getRiskColor(String riskLevel) {
    if (riskLevel.toLowerCase().contains('high')) return const Color(0xFFF43F5E);
    if (riskLevel.toLowerCase().contains('medium') || riskLevel.toLowerCase().contains('moderate')) return const Color(0xFFF59E0B);
    return const Color(0xFF10B981);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text(l10n.history, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_sweep),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  backgroundColor: theme.colorScheme.surface,
                  title: const Text('Clear History?', style: TextStyle(color: Colors.white)),
                  content: const Text('This will permanently delete all past assessments.', style: TextStyle(color: Colors.white70)),
                  actions: [
                    TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
                    TextButton(
                      onPressed: () {
                        Navigator.pop(context);
                        _clearHistory();
                      },
                      child: Text(l10n.clearHistory, style: const TextStyle(color: Colors.redAccent)),
                    ),
                  ],
                )
              );
            },
          )
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
          Positioned(
            top: 100,
            right: -50,
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
                ? const Center(child: CircularProgressIndicator(color: Colors.white))
                : _history.isEmpty
                    ? Center(
                        child: Text(
                          l10n.noHistory,
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.white54, fontSize: 16),
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                        itemCount: _history.length,
                        itemBuilder: (context, index) {
                          final item = _history[index];
                          final date = DateTime.parse(item['timestamp']);
                          final formattedDate = DateFormat('MMM d, yyyy • h:mm a').format(date);
                          final riskColor = _getRiskColor(item['risk_level']);

                          return Container(
                            margin: const EdgeInsets.only(bottom: 16),
                            decoration: BoxDecoration(
                              color: Colors.white.withValues(alpha: 0.03),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
                            ),
                            child: ListTile(
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => ResultScreen(
                                      diseaseName: item['disease'],
                                      resultData: {
                                        'risk_level': item['risk_level'],
                                        'confidence_percentage': item['confidence'],
                                        'top_factors': item['top_factors'],
                                      },
                                      isFromHistory: true,
                                    ),
                                  ),
                                );
                              },
                              contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                              leading: Container(
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: riskColor.withValues(alpha: 0.1),
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(Icons.history, color: riskColor),
                              ),
                              title: Text(item['disease'], style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const SizedBox(height: 4),
                                  Text(formattedDate, style: const TextStyle(color: Colors.white54, fontSize: 12)),
                                  const SizedBox(height: 4),
                                  Text('${l10n.aiConfidence}: ${item['confidence']}%', style: const TextStyle(color: Colors.white70, fontSize: 13)),
                                ],
                              ),
                              trailing: Text(
                                item['risk_level'].toUpperCase(),
                                style: TextStyle(color: riskColor, fontWeight: FontWeight.bold, fontSize: 14),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}
