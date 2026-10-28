#[derive(Debug, PartialEq, Eq)]
pub enum CoreError {
    MemoryCorruption,
    TimingAnomaly,
    InvalidConstraint,
    CryptoVerificationFailure,
}
