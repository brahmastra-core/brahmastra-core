import 'dart:typed_data';
import 'package:flutter/material.dart';

void main() {
  runApp(const BrahmastraApp());
}

class BrahmastraApp extends StatelessWidget {
  const BrahmastraApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Brahmastra',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F141C),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00E676),
          secondary: Color(0xFF00B0FF),
          surface: Color(0xFF1A222D),
        ),
      ),
      home: const RootNavigationContainer(),
    );
  }
}

class RootNavigationContainer extends StatefulWidget {
  const RootNavigationContainer({super.key});

  @override
  State<RootNavigationContainer> createState() => _RootNavigationContainerState();
}

class _RootNavigationContainerState extends State<RootNavigationContainer> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    SovereignChatScreen(),
    SecureVaultScreen(),
    DharmaDashboardScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        backgroundColor: const Color(0xFF141B24),
        selectedIndex: _currentIndex,
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.shield_outlined),
            selectedIcon: Icon(Icons.shield, color: Color(0xFF00E676)),
            label: 'Mesh Chat',
          ),
          NavigationDestination(
            icon: Icon(Icons.lock_outline),
            selectedIcon: Icon(Icons.lock, color: Color(0xFF00E676)),
            label: 'Vault',
          ),
          NavigationDestination(
            icon: Icon(Icons.account_balance_wallet_outlined),
            selectedIcon: Icon(Icons.account_balance_wallet, color: Color(0xFF00E676)),
            label: 'Dharma 80/20',
          ),
        ],
      ),
    );
  }
}

class SovereignChatScreen extends StatelessWidget {
  const SovereignChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Brahmastra Mesh (Offline Active)'),
        backgroundColor: const Color(0xFF141B24),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 16.0),
            child: Icon(Icons.lock, color: Color(0xFF00E676)),
          )
        ],
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            color: const Color(0xFF1A222D),
            child: const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.wifi_tethering, size: 16, color: Color(0xFF00E676)),
                SizedBox(width: 8),
                Text('Direct Device-to-Device Mesh | 4096-Byte Sphinx Enforced',
                    style: TextStyle(fontSize: 12, color: Colors.white70)),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: const [
                ChatBubble(
                  message: 'Local Offline Mesh Initialized. No cellular network required.',
                  isMe: false,
                  nodeId: 'Peer-Node-A',
                ),
                ChatBubble(
                  message: '4096-Byte Lattice Packet padded and verified with Zeroize memory guard.',
                  isMe: true,
                  nodeId: 'Local-Owner',
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: 'Type sovereign message...',
                      filled: true,
                      fillColor: const Color(0xFF1A222D),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.send, color: Color(0xFF00E676)),
                  onPressed: () {},
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}

class ChatBubble extends StatelessWidget {
  final String message;
  final bool isMe;
  final String nodeId;

  const ChatBubble({super.key, required this.message, required this.isMe, required this.nodeId});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isMe ? const Color(0xFF005938) : const Color(0xFF1E293B),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          crossAxisAlignment: isMe ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            Text(nodeId, style: const TextStyle(fontSize: 10, color: Colors.white54)),
            const SizedBox(height: 4),
            Text(message, style: const TextStyle(color: Colors.white)),
          ],
        ),
      ),
    );
  }
}

class SecureVaultScreen extends StatelessWidget {
  const SecureVaultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Secure with Brahmastra'),
        backgroundColor: const Color(0xFF141B24),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Card(
              color: Color(0xFF1A222D),
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Icon(Icons.enhanced_encryption, size: 48, color: Color(0xFF00E676)),
                    SizedBox(height: 12),
                    Text('Post-Quantum Local Vault',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    SizedBox(height: 8),
                    Text('Encrypt Aadhaar, Land Deeds & Private Records without cloud access.',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 12, color: Colors.white70)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00E676),
                foregroundColor: Colors.black,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              icon: const Icon(Icons.add_moderator),
              label: const Text('ENCRYPT NEW DOCUMENT (FHE LOCK)',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              onPressed: () {},
            ),
          ],
        ),
      ),
    );
  }
}

class DharmaDashboardScreen extends StatelessWidget {
  const DharmaDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dharma 80/20 Welfare Dashboard'),
        backgroundColor: const Color(0xFF141B24),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFF1A222D),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF00E676).withOpacity(0.3)),
              ),
              child: const Column(
                children: [
                  Text('80% Public Welfare Automated Split',
                      style: TextStyle(fontSize: 14, color: Colors.white70)),
                  SizedBox(height: 12),
                  Text('VERIFIED TRANSPARENCY',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF00E676))),
                  SizedBox(height: 8),
                  Text('Direct Benefit Verification Active (ZKP Driven)',
                      style: TextStyle(fontSize: 12, color: Colors.white54)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
