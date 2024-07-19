# UserOperationLib
[Git Source](https://github.com/TrueWallet/contracts/blob/db2e75cb332931da5fdaa38bec9e4d367be1d851/src/interfaces/UserOperation.sol)


## Functions
### getSender


```solidity
function getSender(UserOperation calldata userOp) internal pure returns (address);
```

### gasPrice


```solidity
function gasPrice(UserOperation calldata userOp) internal view returns (uint256);
```

### pack


```solidity
function pack(UserOperation calldata userOp) internal pure returns (bytes memory ret);
```

### hash


```solidity
function hash(UserOperation calldata userOp) internal pure returns (bytes32);
```

### min


```solidity
function min(uint256 a, uint256 b) internal pure returns (uint256);
```

