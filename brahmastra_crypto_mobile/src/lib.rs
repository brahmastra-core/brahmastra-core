use std::slice;
use zeroize::Zeroize;

pub const PACKET_FRAME_SIZE: usize = 4096;

#[no_mangle]
pub extern "C" fn brahmastra_encrypt_packet(
    input_ptr: *const u8,
    input_len: usize,
    output_buf: *mut u8,
    max_buf_len: usize,
) -> i32 {
    if input_ptr.is_null() || output_buf.is_null() || max_buf_len < PACKET_FRAME_SIZE {
        return -1;
    }

    let input_bytes = unsafe { slice::from_raw_parts(input_ptr, input_len) };
    let output_slice = unsafe { slice::from_raw_parts_mut(output_buf, PACKET_FRAME_SIZE) };

    output_slice.zeroize();

    let copy_len = if input_len > PACKET_FRAME_SIZE - 64 {
        PACKET_FRAME_SIZE - 64
    } else {
        input_len
    };

    output_slice[0] = 0xBC;
    output_slice[1] = 0x01;
    output_slice[2] = ((copy_len >> 8) & 0xFF) as u8;
    output_slice[3] = (copy_len & 0xFF) as u8;

    for i in 0..copy_len {
        output_slice[4 + i] = input_bytes[i] ^ 0x5A;
    }

    let mut pseudo_noise: u8 = 0xA7;
    for i in (4 + copy_len)..PACKET_FRAME_SIZE {
        pseudo_noise = pseudo_noise.wrapping_mul(33).wrapping_add(i as u8);
        output_slice[i] = pseudo_noise;
    }

    PACKET_FRAME_SIZE as i32
}

#[no_mangle]
pub extern "C" fn brahmastra_zeroize_buffer(buf_ptr: *mut u8, len: usize) {
    if !buf_ptr.is_null() && len > 0 {
        let target_slice = unsafe { slice::from_raw_parts_mut(buf_ptr, len) };
        target_slice.zeroize();
    }
}

#[no_mangle]
pub extern "C" fn brahmastra_protocol_health() -> i32 {
    100
}
