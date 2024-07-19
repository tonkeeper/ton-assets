# AddressLinkedList
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/libraries/AddressLinkedList.sol)

This library provides utility functions to manage a linked list of addresses.


## State Variables
### SENTINEL_ADDRESS

```solidity
address internal constant SENTINEL_ADDRESS = address(1);
```


### SENTINEL_UINT

```solidity
uint160 internal constant SENTINEL_UINT = 1;
```


## Functions
### onlyAddress

*Modifier that checks if an address is valid.*


```solidity
modifier onlyAddress(address addr);
```

### add

Adds an address to the linked list.


```solidity
function add(mapping(address => address) storage self, address addr) internal onlyAddress(addr);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|
|`addr`|`address`|The address to be added.|


### remove

Removes an address from the linked list.


```solidity
function remove(mapping(address => address) storage self, address addr) internal;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|
|`addr`|`address`|The address to be removed.|


### tryRemove

Tries to remove an address from the linked list.


```solidity
function tryRemove(mapping(address => address) storage self, address addr) internal returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|
|`addr`|`address`|The address to be removed.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|Returns true if removal is successful, false otherwise.|


### clear

Clears all addresses from the linked list.


```solidity
function clear(mapping(address => address) storage self) internal;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|


### isExist

Checks if an address exists in the linked list.


```solidity
function isExist(mapping(address => address) storage self, address addr)
    internal
    view
    onlyAddress(addr)
    returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|
|`addr`|`address`|The address to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|Returns true if the address exists, false otherwise.|


### size

Returns the size of the linked list.


```solidity
function size(mapping(address => address) storage self) internal view returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|Returns the size of the linked list.|


### isEmpty

Checks if the linked list is empty.


```solidity
function isEmpty(mapping(address => address) storage self) internal view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|Returns true if the linked list is empty, false otherwise.|


### list

Returns a list of addresses from the linked list.


```solidity
function list(mapping(address => address) storage self, address from, uint256 limit)
    internal
    view
    returns (address[] memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(address => address)`|The linked list mapping.|
|`from`|`address`|The starting address.|
|`limit`|`uint256`|The number of addresses to return.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`address[]`|Returns an array of addresses.|


## Errors
### InvalidAddress

```solidity
error InvalidAddress();
```

### AddressAlreadyExists

```solidity
error AddressAlreadyExists();
```

### AddressNotExists

```solidity
error AddressNotExists();
```

