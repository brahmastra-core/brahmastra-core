import 'dart:async';
import 'dart:collection';
import 'dart:convert';
import 'dart:typed_data';

class MeshPacket {
  final String packetId;
  final String senderNodeId;
  final Uint8List payload4096;
  final int hopCount;
  final int timestamp;

  MeshPacket({
    required this.packetId,
    required this.senderNodeId,
    required this.payload4096,
    this.hopCount = 0,
    required this.timestamp,
  });

  Map<String, dynamic> toMap() => {
    'id': packetId,
    'sender': senderNodeId,
    'hops': hopCount,
    'time': timestamp,
    'data': base64Encode(payload4096),
  };
}

class BrahmastraMeshRouter {
  final Set<String> _seenPacketIds = {};
  final Queue<MeshPacket> _storeAndForwardBuffer = Queue<MeshPacket>();
  final StreamController<MeshPacket> _inboundController = StreamController<MeshPacket>.broadcast();

  Stream<MeshPacket> get onPacketReceived => _inboundController.stream;

  bool ingestPacket(MeshPacket packet) {
    if (_seenPacketIds.contains(packet.packetId)) {
      return false; // Prevent network replay loops
    }

    _seenPacketIds.add(packet.packetId);
    if (_seenPacketIds.length > 5000) {
      _seenPacketIds.remove(_seenPacketIds.first);
    }

    _inboundController.add(packet);
    return true;
  }

  void bufferForForwarding(MeshPacket packet) {
    if (_storeAndForwardBuffer.length >= 256) {
      _storeAndForwardBuffer.removeFirst();
    }
    _storeAndForwardBuffer.addLast(packet);
  }

  List<MeshPacket> flushPendingPackets() {
    final list = _storeAndForwardBuffer.toList();
    _storeAndForwardBuffer.clear();
    return list;
  }
}
