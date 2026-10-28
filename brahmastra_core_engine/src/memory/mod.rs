use zeroize::{Zeroize, ZeroizeOnDrop};

#[derive(Zeroize, ZeroizeOnDrop)]
pub struct SensitiveKey {
    pub key_bytes: [u8; 32],
}

impl SensitiveKey {
    pub fn new(raw_bytes: [u8; 32]) -> Self {
        Self {
            key_bytes: raw_bytes,
        }
    }

    pub fn expose_key(&self) -> &[u8; 32] {
        &self.key_bytes
    }
}