import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'l10n/app_localizations.dart';
import 'screens/home_screen.dart';

final ValueNotifier<Locale> appLocale = ValueNotifier(const Locale('en'));

void main() {
  runApp(const DiseaseRiskApp());
}

class DiseaseRiskApp extends StatelessWidget {
  const DiseaseRiskApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<Locale>(
      valueListenable: appLocale,
      builder: (context, locale, child) {
        return MaterialApp(
          title: 'VitaGuard AI',
          debugShowCheckedModeBanner: false,
          locale: locale,
          localizationsDelegates: AppLocalizations.localizationsDelegates,
          supportedLocales: AppLocalizations.supportedLocales,
          themeMode: ThemeMode.dark,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0F172A), // Deep Slate
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF38BDF8), // Vibrant Light Blue
          secondary: Color(0xFF818CF8), // Indigo
          surface: Color(0xFF1E293B), // Slate 800
          background: Color(0xFF0F172A),
        ),
        fontFamily: 'Roboto',
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: true,
        ),
      ),
      home: const HomeScreen(),
        );
      },
    );
  }
}
