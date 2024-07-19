# OwnerManagerErrors
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/common/Errors.sol)


## Errors
### NoOwner
*Throws when an operation requires an owner but none exist.*


```solidity
error NoOwner();
```

### CallerMustBeSelfOfModule
*Throws when the caller must be the contract itself or one of its modules.*


```solidity
error CallerMustBeSelfOfModule();
```

