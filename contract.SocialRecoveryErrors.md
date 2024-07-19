# SocialRecoveryErrors
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/common/Errors.sol)


## Errors
### InvalidOwner
Throws when an invalid owner address is provided or detected.


```solidity
error InvalidOwner();
```

### InvalidGuardian
Throws when an invalid guardian address is provided or detected.


```solidity
error InvalidGuardian();
```

### InvalidThreshold
Throws when an invalid threshold value is provided or detected.


```solidity
error InvalidThreshold();
```

### ZeroAddressForGuardianProvided
Throws when a zero address is provided where a guardian address is required.


```solidity
error ZeroAddressForGuardianProvided();
```

### DuplicateGuardianProvided
Throws when a duplicate guardian address is provided.


```solidity
error DuplicateGuardianProvided();
```

### RecoveryAlreadyExecuted
Throws when a recovery operation has already been executed.


```solidity
error RecoveryAlreadyExecuted();
```

### RecoveryNotEnoughConfirmations
Throws when there are not enough confirmations for a recovery operation.


```solidity
error RecoveryNotEnoughConfirmations();
```

### RecoveryPeriodStillPending
Throws when the recovery period is still pending.


```solidity
error RecoveryPeriodStillPending();
```

### RecoveryNotInitiated
Throws when attempting to execute a recovery operation that has not been initiated.


```solidity
error RecoveryNotInitiated();
```

