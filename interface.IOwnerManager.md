# IOwnerManager
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/interfaces/IOwnerManager.sol)

Interface for managing ownership in a contract


## Functions
### isOwner

Checks if the given address is an owner


```solidity
function isOwner(address addr) external view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`addr`|`address`|Address to be checked|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|bool Returns true if the address is an owner, otherwise false|


### addOwner

Adds a single owner to the contract


```solidity
function addOwner(address owner) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`owner`|`address`|Address of the new owner to be added|


### addOwners

Adds multiple owners to the contract


```solidity
function addOwners(address[] calldata owners) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`owners`|`address[]`|Array of addresses of the new owners to be added|


### resetOwner

Resets the ownership of the contract to a single owner


```solidity
function resetOwner(address newOwner) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`newOwner`|`address`|Address of the new owner|


### resetOwners

Resets the ownership of the contract to multiple owners


```solidity
function resetOwners(address[] calldata newOwners) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`newOwners`|`address[]`|Array of addresses to set as the new owners|


### removeOwner

Removes a specific owner from the contract


```solidity
function removeOwner(address owner) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`owner`|`address`|Address of the owner to be removed|


### listOwner

Returns a list of all owners


```solidity
function listOwner() external returns (address[] memory owners);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`owners`|`address[]`|Array of owner addresses|


## Events
### OwnerAdded
*Emitted when a new owner is added*


```solidity
event OwnerAdded(address indexed owner);
```

**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`owner`|`address`|Address of the new owner added|

### OwnerRemoved
*Emitted when an existing owner is removed*


```solidity
event OwnerRemoved(address indexed owner);
```

**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`owner`|`address`|Address of the owner removed|

### OwnerCleared
*Emitted when all owners are cleared and reset*


```solidity
event OwnerCleared();
```

