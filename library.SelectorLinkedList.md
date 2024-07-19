# SelectorLinkedList
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/libraries/SelectorLinkedList.sol)

This library provides utility functions to manage a linked list of selectors.


## State Variables
### SENTINEL_SELECTOR

```solidity
bytes4 internal constant SENTINEL_SELECTOR = 0x00000001;
```


### SENTINEL_UINT

```solidity
uint32 internal constant SENTINEL_UINT = 1;
```


## Functions
### isSafeSelector


```solidity
function isSafeSelector(bytes4 selector) internal pure returns (bool);
```

### onlySelector

*Modifier that checks if an selector is valid.*


```solidity
modifier onlySelector(bytes4 selector);
```

### add

Adds a selector to the linked list.


```solidity
function add(mapping(bytes4 => bytes4) storage self, bytes4 selector) internal onlySelector(selector);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|
|`selector`|`bytes4`|The selector to be added.|


### add


```solidity
function add(mapping(bytes4 => bytes4) storage self, bytes4[] memory selectors) internal;
```

### remove

Removes an address from the linked list.


```solidity
function remove(mapping(bytes4 => bytes4) storage self, bytes4 selector) internal;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|
|`selector`|`bytes4`|The address to be removed.|


### clear

Clears all selectors from the linked list.


```solidity
function clear(mapping(bytes4 => bytes4) storage self) internal;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|


### isExist

Checks if an selector exists in the linked list.


```solidity
function isExist(mapping(bytes4 => bytes4) storage self, bytes4 selector)
    internal
    view
    onlySelector(selector)
    returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|
|`selector`|`bytes4`|The selector to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|Returns true if the selector exists, false otherwise.|


### size

Returns the size of the linked list.


```solidity
function size(mapping(bytes4 => bytes4) storage self) internal view returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|Returns the size of the linked list.|


### isEmpty

Checks if the linked list is empty.


```solidity
function isEmpty(mapping(bytes4 => bytes4) storage self) internal view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|Returns true if the linked list is empty, false otherwise.|


### list

Returns a list of selectors from the linked list.


```solidity
function list(mapping(bytes4 => bytes4) storage self, bytes4 from, uint256 limit)
    internal
    view
    returns (bytes4[] memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`self`|`mapping(bytes4 => bytes4)`|The linked list mapping.|
|`from`|`bytes4`|The starting selector.|
|`limit`|`uint256`|The number of selectors to return.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes4[]`|Returns an array of selectors.|


## Errors
### InvalidSelector

```solidity
error InvalidSelector();
```

### SelectorAlreadyExists

```solidity
error SelectorAlreadyExists();
```

### SelectorNotExists

```solidity
error SelectorNotExists();
```

