# SecurityControlModule
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/SecurityControlModule/SecurityControlModule.sol)

**Inherits:**
[BaseModule](/src/modules/BaseModule.sol/abstract.BaseModule.md)

*A module that provides enhanced security controls for adding and removing modules and executing specific functions on a initialized wallet.*


## State Variables
### trueContractManager
*The contract manager that checks if a module is trusted.*


```solidity
ITrueContractManager public immutable trueContractManager;
```


### basicInitialized
*Mapping to track whether a basic initialization has been done for each wallet address.*


```solidity
mapping(address => bool) public basicInitialized;
```


### fullInitialized
*Mapping to track whether a full initialization has been done for each wallet address.*


```solidity
mapping(address => bool) public fullInitialized;
```


### walletInitSeed
*Mapping to track initialization state for wallets.*


```solidity
mapping(address wallet => uint256 seed) public walletInitSeed;
```


### __seed
*Internal seed for generating unique values.*


```solidity
uint256 private __seed = 0;
```


## Functions
### constructor


```solidity
constructor(ITrueContractManager trueContractManagerAddress);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`trueContractManagerAddress`|`ITrueContractManager`|The address of the TrueContractManager registry.|


### fullInit

Completes the full initialization of the module.

*This function should be called after the basic initialization has been done via `_init`.
It finalizes the module setup by assigning a unique seed to the `walletInitSeed` mapping for the caller.
This function can only be called once for each wallet to prevent re-initialization.*


```solidity
function fullInit() external;
```

### fullInitAndAddModule

Completes the full initialization and adds a module to the target wallet address.

*This function finalizes the initialization by setting `fullInitialized` to true and assigns a new seed.
Only allows adding a module to the target contract after the full initialization is complete.*


```solidity
function fullInitAndAddModule(address target, bytes calldata data) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`target`|`address`|The address of the target contract where the module is to be added.|
|`data`|`bytes`|The function data to be executed, including the module to be added.|


### execute

Executes a specific function on the target address.


```solidity
function execute(address target, bytes calldata data) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`target`|`address`|The address of the target contract.|
|`data`|`bytes`|The function data to be executed.|


### _execute

*Internal function to execute a call to a target address.*


```solidity
function _execute(address target, bytes calldata data) internal;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`target`|`address`|The address of the target contract.|
|`data`|`bytes`|The function data to be executed.|


### _preExecute

*Verifies the provided data for valid function execution.*


```solidity
function _preExecute(address target, bytes calldata data) internal view;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`target`|`address`|The target contract's address.|
|`data`|`bytes`|The function data.|


### _authorized

*Verifies if the caller is authorized to interact with the target.*


```solidity
function _authorized(address target) internal view;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`target`|`address`|The target wallet address.|


### inited

Checks if a wallet is initialized.


```solidity
function inited(address wallet) internal view override returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|bool True if the wallet is initialized, false otherwise.|


### _init

Internal function for basic initialization of the module.

*This function sets the initial state for the module associated with the caller.
It should be invoked only once as part of the module's setup process.
The function checks if the basic initialization for the caller (`_sender`) has already been completed to prevent re-initialization.
The `data` parameter is not currently used but can be utilized for future extensions or additional initialization parameters.*


```solidity
function _init(bytes calldata data) internal override;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`data`|`bytes`|Additional initialization data; currently unused.|


### _deInit

*De-initializes the module for a wallet.*


```solidity
function _deInit() internal override;
```

### _newSeed

*Generates a new unique seed value.*


```solidity
function _newSeed() private returns (uint256);
```

### requiredFunctions

Provides the list of required functions that this module supports.


```solidity
function requiredFunctions() external pure override returns (bytes4[] memory);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes4[]`|bytes4[] Array of function selectors.|


## Events
### Execute
An event emitted when a function execution is successful.


```solidity
event Execute(address target, bytes data, address sender);
```

## Errors
### SecurityControlModule__InvalidModule
*Throws when a module is not recognized as a trusted module.*


```solidity
error SecurityControlModule__InvalidModule();
```

### SecurityControlModule__InvalidOwner
*Throws when the caller is not the owner of the target wallet.*


```solidity
error SecurityControlModule__InvalidOwner();
```

### SecurityControlModule__NotInitialized
*Throws when the module is not initialized for a particular wallet.*


```solidity
error SecurityControlModule__NotInitialized();
```

### SecurityControlModule__UnableSelfRemove
*Throws when there's an attempt to remove this module itself.*


```solidity
error SecurityControlModule__UnableSelfRemove();
```

### SecurityControlModule__UnsupportedSelector
*Throws when a function selector is unsupported.*


```solidity
error SecurityControlModule__UnsupportedSelector(bytes4 selector);
```

### SecurityControlModule__ExecuteError
*Throws when there's an issue executing a function.*


```solidity
error SecurityControlModule__ExecuteError(address target, bytes data, address sender, bytes returnData);
```

### SecurityControlModule__BasicInitAlreadyDone
*Throws when attempting to redo the basic initialization for a wallet that has already been initialized.*


```solidity
error SecurityControlModule__BasicInitAlreadyDone();
```

### SecurityControlModule__BasicInitNotDone
*Throws when attempting operations requiring basic initialization that hasn't been completed for a wallet.*


```solidity
error SecurityControlModule__BasicInitNotDone();
```

### SecurityControlModule__FullInitAlreadyDone
*Throws when attempting to redo the full initialization for a wallet that has already completed full initialization.*


```solidity
error SecurityControlModule__FullInitAlreadyDone();
```

### SecurityControlModule__InvalidInitState
*Throws when the initialization state is invalid.*


```solidity
error SecurityControlModule__InvalidInitState();
```

