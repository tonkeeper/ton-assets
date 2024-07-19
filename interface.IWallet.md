# IWallet
[Git Source](https://github.com/TrueWallet/contracts/blob/3a8d1f53b9460a762889129a9214639685ad5b95/src/wallet/IWallet.sol)

**Inherits:**
[IAccount](/src/interfaces/IAccount.sol/interface.IAccount.md), [IModuleManager](/src/interfaces/IModuleManager.sol/interface.IModuleManager.md), [IOwnerManager](/src/interfaces/IOwnerManager.sol/interface.IOwnerManager.md)


## Functions
### entryPoint

Entrypoint connected to the wallet


```solidity
function entryPoint() external view returns (address);
```

### nonce

Get the nonce on the wallet


```solidity
function nonce() external view returns (uint256);
```

### execute

Method called by the entryPoint to execute a userOperation


```solidity
function execute(address target, uint256 value, bytes calldata payload) external;
```

### executeBatch

Method called by the entryPoint to execute a userOperation with a sequence of transactions


```solidity
function executeBatch(address[] calldata target, uint256[] calldata value, bytes[] calldata payload) external;
```

### isValidSignature

Verifies that the signer is the owner of the signing contract


```solidity
function isValidSignature(bytes32 messageHash, bytes memory signature) external view returns (bytes4);
```

