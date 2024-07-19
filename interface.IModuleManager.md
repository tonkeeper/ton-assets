# IModuleManager
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/interfaces/IModuleManager.sol)


## Functions
### addModule

Adds a new module to the wallet.

*Can only be called by the module.*

*Modules should be stored as a linked list.*


```solidity
function addModule(bytes calldata moduleAndData) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`moduleAndData`|`bytes`|Encoded module to be added and its associated initialization data.|


### removeModule

Removes a module from the wallet.

*Can only be called by the module.*


```solidity
function removeModule(address module) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`module`|`address`|Address of the module to be removed.|


### isAuthorizedModule

Checks if a module is authorized.


```solidity
function isAuthorizedModule(address module) external view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`module`|`address`|Address of the module to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|true If the module is authorized, false otherwise.|


### listModules

Returns the list of added modules and their supported function selectors.


```solidity
function listModules() external view returns (address[] memory modules, bytes4[][] memory selectors);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`modules`|`address[]`|An array of the addresses of the added modules.|
|`selectors`|`bytes4[][]`|A two-dimensional array containing the lists of supported function selectors for the corresponding modules.|


### executeFromModule

Can only be called by a added module.

*Allows a Module to execute a transaction.*


```solidity
function executeFromModule(address dest, uint256 value, bytes calldata data) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`dest`|`address`|Destination address of module transaction.|
|`value`|`uint256`|Ether value of module transaction.|
|`data`|`bytes`|Data payload of module transaction.|


## Events
### ModuleAdded
*Emitted when a new module is added.*


```solidity
event ModuleAdded(address indexed module);
```

### ModuleRemoved
*Emitted when a module is removed.*


```solidity
event ModuleRemoved(address indexed module);
```

### ModuleRemovedWithError
*Emitted when a module is removed with an error.*


```solidity
event ModuleRemovedWithError(address indexed module);
```

