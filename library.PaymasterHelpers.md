# PaymasterHelpers
[Git Source](https://github.com/TrueWallet/contracts/blob/843930f01013ad22976a2d653f9d67aaa82d54f4/src/paymaster/PaymasterHelper.sol)


## Functions
### paymasterContext

*Encodes the paymaster context: paymasterId and gasPrice*


```solidity
function paymasterContext(UserOperation calldata op, PaymasterData memory data, uint256 gasPrice)
    internal
    pure
    returns (bytes memory context);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`op`|`UserOperation`|UserOperation object|
|`data`|`PaymasterData`|PaymasterData passed|
|`gasPrice`|`uint256`|effective gasPrice|


### _decodePaymasterData

*Decodes paymaster data assuming it follows PaymasterData*


```solidity
function _decodePaymasterData(UserOperation calldata op) internal pure returns (PaymasterData memory);
```

### _decodePaymasterContext

*Decodes paymaster context assuming it follows PaymasterContext*


```solidity
function _decodePaymasterContext(bytes memory context) internal pure returns (PaymasterContext memory);
```

