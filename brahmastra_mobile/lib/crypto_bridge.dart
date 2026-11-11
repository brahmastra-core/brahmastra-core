import 'dart:ffi' as ffi;
import 'dart:io';
import 'package:ffi/ffi.dart';

typedef EncryptNative = ffi.Int32 Function(
    ffi.Pointer<ffi.Uint8>, ffi.Size, ffi.Pointer<ffi.Uint8>, ffi.Size);
typedef EncryptDart = int Function(
    ffi.Pointer<ffi.Uint8>, int, ffi.Pointer<ffi.Uint8>, int);

typedef ZeroizeNative = ffi.Void Function(ffi.Pointer<ffi.Uint8>, ffi.Size);
typedef ZeroizeDart = void Function(ffi.Pointer<ffi.Uint8>, int);

typedef HealthNative = ffi.Int32 Function();
typedef HealthDart = int Function();

class BrahmastraCryptoBridge {
  late ffi.DynamicLibrary _lib;
  late EncryptDart _encrypt;
  late ZeroizeDart _zeroize;
  late HealthDart _health;

  BrahmastraCryptoBridge() {
    if (Platform.isAndroid) {
      _lib = ffi.DynamicLibrary.open("libbrahmastra_core.so");
    } else {
      _lib = ffi.DynamicLibrary.open("brahmastra_crypto_mobile/target/release/libbrahmastra_core.so");
    }

    _encrypt = _lib
        .lookup<ffi.NativeFunction<EncryptNative>>('brahmastra_encrypt_packet')
        .asFunction<EncryptDart>();

    _zeroize = _lib
        .lookup<ffi.NativeFunction<ZeroizeNative>>('brahmastra_zeroize_buffer')
        .asFunction<ZeroizeDart>();

    _health = _lib
        .lookup<ffi.NativeFunction<HealthNative>>('brahmastra_protocol_health')
        .asFunction<HealthDart>();
  }

  int getProtocolHealth() => _health();
}
