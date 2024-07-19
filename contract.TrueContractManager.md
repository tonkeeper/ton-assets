# TrueContractManager
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/registry/TrueContractManager.sol)

**Inherits:**
[ITrueContractManager](/src/registry/ITrueContractManager.sol/interface.ITrueContractManager.md), Ownable

This contract manages and verifies TrueContract modules

*It allows the owner to add or remove module contracts and check if a module is registered*


## State Variables
### _isTrueModule
*Mapping to store registered TrueContract modules*


```solidity
mapping(address module => bool) private _isTrueModule;
```


## Functions
### constructor


```solidity
constructor(address _owner);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_owner`|`address`|The address of the owner of this contract|


### add

Adds a list of modules to the registry

*Registers multiple module addresses as TrueModules. Permissioned to only the owner*


```solidity
function add(address[] calldata modules) external onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`modules`|`address[]`|Array of addresses of the modules to be added|


### remove

*Removes a list of modules from the registry. Permissioned to only the owner*


```solidity
function remove(address[] calldata modules) external onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`modules`|`address[]`|Array of addresses of the modules to be removed|


### isTrueModule

Checks if the address is a registered TrueModule


```solidity
function isTrueModule(address module) external view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`module`|`address`|Address of the module to be checked|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|bool Returns true if the provided address is a registered module, otherwise false|


## Errors
### TrueContractManager__NotContractProvided
*Emitted when an address provided is not a contract*


```solidity
error TrueContractManager__NotContractProvided();
```

### TrueContractManager__ContractAlreadyRegistered
*Emitted when attempting to register an already registered contract*


```solidity
error TrueContractManager__ContractAlreadyRegistered();
```

### TrueContractManager__ContractNotRegistered
*Emitted when attempting to remove a contract that is not registered*


```solidity
error TrueContractManager__ContractNotRegistered();
```

