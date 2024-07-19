# Exec
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/utils/Exec.sol)

Utility functions helpful when making different kinds of contract calls in Solidity.


## Functions
### call


```solidity
function call(address to, uint256 value, bytes memory data, uint256 txGas) internal returns (bool success);
```

### staticcall


```solidity
function staticcall(address to, bytes memory data, uint256 txGas) internal view returns (bool success);
```

### delegateCall


```solidity
function delegateCall(address to, bytes memory data, uint256 txGas) internal returns (bool success);
```

### getReturnData


```solidity
function getReturnData(uint256 maxLen) internal pure returns (bytes memory returnData);
```

### revertWithData


```solidity
function revertWithData(bytes memory returnData) internal pure;
```

### callAndRevert


```solidity
function callAndRevert(address to, bytes memory data, uint256 maxLen) internal;
```

