# TrueWalletProxy
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/wallet/TrueWalletProxy.sol)

**Inherits:**
[Upgradeable](/src/utils/Upgradeable.sol/abstract.Upgradeable.md)

A proxy contract that forwards calls to an implementation contract.

*This proxy uses the EIP-1967 standard for storage slots.*


## Functions
### constructor

Initializes the proxy with the address of the initial implementation contract.


```solidity
constructor(address logic);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`logic`|`address`|Address of the initial implementation.|


### fallback

Fallback function which forwards all calls to the implementation contract.

*Uses delegatecall to ensure the context remains within the proxy.*


```solidity
fallback() external payable;
```

