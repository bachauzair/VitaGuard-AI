import 'package:flutter/material.dart';
import 'dart:ui';
import 'package:fl_chart/fl_chart.dart';
import '../services/history_service.dart';
import '../l10n/app_localizations.dart';

class ResultScreen extends StatefulWidget {
  final Map<String, dynamic> resultData;
  final String diseaseName;
  final bool isFromHistory;

  const ResultScreen({
    super.key, 
    required this.resultData, 
    required this.diseaseName,
    this.isFromHistory = false,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {

  @override
  void initState() {
    super.initState();
    _saveResult();
  }

  Future<void> _saveResult() async {
    if (!widget.isFromHistory) {
      await HistoryService.saveResult(widget.diseaseName, widget.resultData);
    }
  }

  Color _getRiskColor(String riskLevel) {
    if (riskLevel.toLowerCase().contains('high')) return const Color(0xFFF43F5E); // Rose
    if (riskLevel.toLowerCase().contains('medium') || riskLevel.toLowerCase().contains('moderate')) return const Color(0xFFF59E0B); // Amber
    return const Color(0xFF10B981); // Emerald
  }

  IconData _getRiskIcon(String riskLevel) {
    if (riskLevel.toLowerCase().contains('high')) return Icons.warning_rounded;
    if (riskLevel.toLowerCase().contains('medium') || riskLevel.toLowerCase().contains('moderate')) return Icons.shield_outlined;
    return Icons.check_circle_outline_rounded;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final String riskLevel = widget.resultData['risk_level'] ?? 'Unknown';
    final double confidence = widget.resultData['confidence_percentage']?.toDouble() ?? 0.0;
    final List<dynamic> topFactors = widget.resultData['top_factors'] ?? [];
    final Color riskColor = _getRiskColor(riskLevel);

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text('${widget.diseaseName} Assessment', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
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
          // Dynamic Risk Color Background Ambient Glow
          Positioned(
            top: 50,
            left: 0,
            right: 0,
            child: Center(
              child: Container(
                width: 300,
                height: 300,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: riskColor.withValues(alpha: 0.15),
                  boxShadow: [BoxShadow(color: riskColor.withValues(alpha: 0.15), blurRadius: 100)]
                ),
              ),
            ),
          ),
          SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Risk Indicator Glass Card
                  ClipRRect(
                    borderRadius: BorderRadius.circular(32),
                    child: BackdropFilter(
                      filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 20),
                        decoration: BoxDecoration(
                          color: riskColor.withValues(alpha: 0.05),
                          borderRadius: BorderRadius.circular(32),
                          border: Border.all(color: riskColor.withValues(alpha: 0.3), width: 1.5),
                          boxShadow: [
                            BoxShadow(color: riskColor.withValues(alpha: 0.1), blurRadius: 40, offset: const Offset(0, 10))
                          ]
                        ),
                        child: Column(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(20),
                              decoration: BoxDecoration(
                                color: riskColor.withValues(alpha: 0.1),
                                shape: BoxShape.circle,
                              ),
                              child: Icon(_getRiskIcon(riskLevel), size: 60, color: riskColor),
                            ),
                            const SizedBox(height: 24),
                            Text(
                              riskLevel.toUpperCase(),
                              style: TextStyle(
                                fontSize: 32,
                                fontWeight: FontWeight.w900,
                                color: riskColor,
                                letterSpacing: 1.5,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha: 0.05),
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Text(
                                '${l10n.aiConfidence}: ${confidence.toStringAsFixed(1)}%',
                                style: const TextStyle(fontSize: 14, color: Colors.white70, fontWeight: FontWeight.w600),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 40),
                  
                  // Explainable AI Section
                  const Text(
                    'AI Explainability Analysis',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'SHAP values breakdown showing exact metrics that drove this prediction.',
                    style: TextStyle(fontSize: 14, color: Colors.white54, height: 1.4),
                  ),
                  const SizedBox(height: 24),

                  ...topFactors.map((factor) {
                    final String name = factor['name'];
                    final String direction = factor['direction']; 
                    final double impact = factor['impact']?.toDouble() ?? 0.0;
                    
                    final isIncreasing = direction == 'increasing';
                    final impactColor = isIncreasing ? const Color(0xFFF43F5E) : const Color(0xFF10B981);
                    final impactIcon = isIncreasing ? Icons.trending_up : Icons.trending_down;
                    
                    return Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.03),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                        leading: Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: impactColor.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(impactIcon, color: impactColor),
                        ),
                        title: Text(name, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                        subtitle: Padding(
                          padding: const EdgeInsets.only(top: 4.0),
                          child: Text('Impact Factor: ${impact.toStringAsFixed(4)}', style: const TextStyle(color: Colors.white54)),
                        ),
                        trailing: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              isIncreasing ? 'Drives Risk Up' : 'Drives Risk Down',
                              style: TextStyle(color: impactColor, fontWeight: FontWeight.w600, fontSize: 13),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                  const SizedBox(height: 40),
                  
                  // SHAP Bar Chart
                  Text(
                    l10n.visualImpact,
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Magnitude and direction of clinical factors.',
                    style: TextStyle(fontSize: 14, color: Colors.white54, height: 1.4),
                  ),
                  const SizedBox(height: 24),
                  if (topFactors.isNotEmpty)
                    Container(
                      height: 250,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.03),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
                      ),
                      child: BarChart(
                        BarChartData(
                          alignment: BarChartAlignment.spaceAround,
                          maxY: topFactors.map((e) => e['impact'].toDouble()).reduce((a, b) => a > b ? a : b) * 1.2,
                          barTouchData: BarTouchData(enabled: false),
                          titlesData: FlTitlesData(
                            show: true,
                            bottomTitles: AxisTitles(
                              sideTitles: SideTitles(
                                showTitles: true,
                                getTitlesWidget: (double value, TitleMeta meta) {
                                  final index = value.toInt();
                                  if (index >= 0 && index < topFactors.length) {
                                    // Shorten long names for the chart
                                    String name = topFactors[index]['name'].toString();
                                    if (name.length > 8) name = name.substring(0, 8) + '...';
                                    return Padding(
                                      padding: const EdgeInsets.only(top: 8.0),
                                      child: Text(name, style: const TextStyle(color: Colors.white70, fontSize: 10)),
                                    );
                                  }
                                  return const Text('');
                                },
                              ),
                            ),
                            leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          ),
                          gridData: const FlGridData(show: false),
                          borderData: FlBorderData(show: false),
                          barGroups: topFactors.asMap().entries.map((entry) {
                            final index = entry.key;
                            final factor = entry.value;
                            final double impact = factor['impact'].toDouble();
                            final isIncreasing = factor['direction'] == 'increasing';
                            return BarChartGroupData(
                              x: index,
                              barRods: [
                                BarChartRodData(
                                  toY: impact,
                                  color: isIncreasing ? const Color(0xFFF43F5E) : const Color(0xFF10B981),
                                  width: 20,
                                  borderRadius: BorderRadius.circular(4),
                                )
                              ],
                            );
                          }).toList(),
                        ),
                      ),
                    ),

                  const SizedBox(height: 40),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.popUntil(context, (route) => route.isFirst);
                    },
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      backgroundColor: Colors.white.withValues(alpha: 0.1),
                      foregroundColor: Colors.white,
                      elevation: 0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                        side: BorderSide(color: Colors.white.withValues(alpha: 0.2)),
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.refresh),
                        const SizedBox(width: 8),
                        Text(l10n.startNew, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
