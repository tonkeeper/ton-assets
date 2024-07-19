# PendingGuardianEntry
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/SocialRecoveryModule/ISocialRecoveryModule.sol)


```solidity
struct PendingGuardianEntry {
    uint256 pendingUntil;
    uint256 threshold;
    bytes32 guardianHash;
    address[] guardians;
}
```

