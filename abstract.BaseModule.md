# BaseModule
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/BaseModule.sol)

**Inherits:**
[IModule](/src/interfaces/IModule.sol/interface.IModule.md), [ModuleManagerErrors](/src/common/Errors.sol/contract.ModuleManagerErrors.md)


## Functions
### walletInit

Initializes the module for the sender's wallet with provided data.

*Only authorized and not previously initialized modules can perform this action.*


```solidity
function walletInit(bytes calldata data) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`data`|`bytes`|Initialization data.|


### walletDeInit

De-initializes the module for the sender's wallet.

*Only not authorized and previously initialized modules can perform this action.*


```solidity
function walletDeInit() external;
```

### inited

Checks if the module is initialized for a given wallet.


```solidity
function inited(address wallet) internal view virtual returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|Address of the wallet to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|true if the module is initialized for the wallet, false otherwise.|


### _init

Initializes the module with provided data.

*Implementation should be provided by derived contracts.*


```solidity
function _init(bytes calldata data) internal virtual;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`data`|`bytes`|Initialization data.|


### _deInit

De-initializes the module.

*Implementation should be provided by derived contracts.*


```solidity
function _deInit() internal virtual;
```

### sender

Retrieves the sender of the current transaction.


```solidity
function sender() internal view returns (address);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`address`|address of the sender.|


### supportsInterface

Checks if the contract implements a given interface.


```solidity
function supportsInterface(bytes4 interfaceId) external pure override returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`interfaceId`|`bytes4`|The interface identifier, as specified by ERC-165.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|true if the contract implements `interfaceId` and `interfaceId` is not 0xffffffff, false otherwise.|


## Events
### ModuleInit
*Emitted when a module is initialized for a wallet.*


```solidity
event ModuleInit(address indexed wallet);
```

### ModuleDeInit
*Emitted when a module is de-initialized for a wallet.*


```solidity
event ModuleDeInit(address indexed wallet);
```

