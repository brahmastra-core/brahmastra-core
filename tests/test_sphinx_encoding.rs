#[cfg(test)]
mod tests {
    const ALPHA_SIZE: usize = 32;
    const BETA_SIZE: usize = 160;
    const GAMMA_SIZE: usize = 16;
    const DELTA_SIZE: usize = 816;
    const TOTAL_SPHINX_SIZE: usize = 1024;

    #[derive(Debug, PartialEq, Eq)]
    struct RustSphinxPacket {
        alpha: [u8; ALPHA_SIZE],
        beta: [u8; BETA_SIZE],
        gamma: [u8; GAMMA_SIZE],
        delta: [u8; DELTA_SIZE],
    }

    impl RustSphinxPacket {
        fn to_bytes(&self) -> Vec<u8> {
            let mut bytes = Vec::with_capacity(TOTAL_SPHINX_SIZE);
            bytes.extend_from_slice(&self.alpha);
            bytes.extend_from_slice(&self.beta);
            bytes.extend_from_slice(&self.gamma);
            bytes.extend_from_slice(&self.delta);
            bytes
        }

        fn from_bytes(raw: &[u8]) -> Result<Self, &'static str> {
            if raw.len() != TOTAL_SPHINX_SIZE {
                return Err("Invalid Sphinx packet size: Must be exactly 1024 bytes");
            }
            let mut alpha = [0u8; ALPHA_SIZE];
            let mut beta = [0u8; BETA_SIZE];
            let mut gamma = [0u8; GAMMA_SIZE];
            let mut delta = [0u8; DELTA_SIZE];

            alpha.copy_from_slice(&raw[..32]);
            beta.copy_from_slice(&raw[32..192]);
            gamma.copy_from_slice(&raw[192..208]);
            delta.copy_from_slice(&raw[208..1024]);

            Ok(RustSphinxPacket { alpha, beta, gamma, delta })
        }
    }

    #[test]
    fn test_sphinx_packet_fixed_size_invariant() {
        let pkt = RustSphinxPacket {
            alpha: [0x11; ALPHA_SIZE],
            beta: [0x22; BETA_SIZE],
            gamma: [0x33; GAMMA_SIZE],
            delta: [0x44; DELTA_SIZE],
        };
        let encoded = pkt.to_bytes();
        assert_eq!(encoded.len(), TOTAL_SPHINX_SIZE);

        let decoded = RustSphinxPacket::from_bytes(&encoded).expect("Decoding failed");
        assert_eq!(pkt, decoded);
    }

    #[test]
    fn test_sphinx_packet_rejects_malformed_size() {
        let short_packet = vec![0u8; 512];
        let result = RustSphinxPacket::from_bytes(&short_packet);
        assert!(result.is_err());
    }
}
