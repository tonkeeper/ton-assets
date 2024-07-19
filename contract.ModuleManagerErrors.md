# ModuleManagerErrors
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/common/Errors.sol)


## Errors
### CallerMustBeModule
Throws when the caller of a function must be a module but is not.


```solidity
error CallerMustBeModule();
```

### ModuleAddressEmpty
Throws when the address of the module is required but not provided.


```solidity
error ModuleAddressEmpty();
```

### ModuleExecuteFromModuleRecursive
Throws when a module tries to recursively call `executeFromModule`.


```solidity
error ModuleExecuteFromModuleRecursive();
```

### ModuleNotAuthorized
Throws when a module is not authorized to perform a specific operation.


```solidity
error ModuleNotAuthorized();
```

### ModuleAuthorized
Throws when a module is already authorized for a specific operation.


```solidity
error ModuleAuthorized();
```

### ModuleNotSupportInterface
Throws when a module does not support the expected interface.


```solidity
error ModuleNotSupportInterface();
```

### ModuleSelectorsEmpty
Throws when the selectors of a module are required but not provided.


```solidity
error ModuleSelectorsEmpty();
```

