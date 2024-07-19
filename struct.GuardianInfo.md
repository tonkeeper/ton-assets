# GuardianInfo
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/SocialRecoveryModule/ISocialRecoveryModule.sol)

This contract allows wallet owners to set guardians for their wallets
and use these guardians for recovery purposes.


```solidity
struct GuardianInfo {
    mapping(address => address) guardians;
    uint256 threshold;
    bytes32 guardianHash;
}
```

