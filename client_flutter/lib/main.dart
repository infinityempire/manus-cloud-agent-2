import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const apiBaseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://10.0.2.2:8000');

void main() {
  runApp(const ManusApp());
}

class ManusApp extends StatelessWidget {
  const ManusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Manus Client',
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _output = '';

  Future<void> _checkHealth() async {
    setState(() => _output = 'בודק...');
    try {
      final res = await http
          .get(Uri.parse('$apiBaseUrl/health'))
          .timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        setState(() => _output = 'הכל תקין');
      } else if (res.statusCode >= 500) {
        setState(() => _output = 'שגיאת שרת זמנית, נסה שוב.');
      } else {
        setState(() => _output = 'שגיאה: ${res.statusCode}');
      }
    } on TimeoutException {
      setState(() => _output = 'תם הזמן לבקשה, נסה שוב.');
    } on SocketException {
      setState(() => _output = 'תקלה בחיבור, בדוק רשת ונסה שוב.');
    } catch (_) {
      setState(() => _output = 'שגיאת שרת זמנית, נסה שוב.');
    }
  }

  Future<void> _getStatus() async {
    setState(() => _output = 'מבקש סטטוס...');
    try {
      final res = await http
          .get(Uri.parse('$apiBaseUrl/status'))
          .timeout(const Duration(seconds: 5));
      if (res.statusCode == 200) {
        final data = json.decode(res.body) as Map<String, dynamic>;
        setState(() => _output =
            'גרסה: ' '${data['version']}, PID: ${data['pid']}\nPython: ${data['python']}\nPlatform: ${data['platform']}');
      } else if (res.statusCode >= 500) {
        setState(() => _output = 'שגיאת שרת זמנית, נסה שוב.');
      } else {
        setState(() => _output = 'שגיאה: ${res.statusCode}');
      }
    } on TimeoutException {
      setState(() => _output = 'תם הזמן לבקשה, נסה שוב.');
    } on SocketException {
      setState(() => _output = 'תקלה בחיבור, בדוק רשת ונסה שוב.');
    } catch (_) {
      setState(() => _output = 'שגיאת שרת זמנית, נסה שוב.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manus Client')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _checkHealth,
              child: const Text('בדוק בריאות'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _getStatus,
              child: const Text('קבל סטטוס'),
            ),
            const SizedBox(height: 24),
            Text(_output, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
