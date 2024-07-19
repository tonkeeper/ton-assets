# ITruePaymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/paymaster/ITruePaymaster.sol)

**Inherits:**
[IPaymaster](/src/interfaces/IPaymaster.sol/interface.IPaymaster.md)


## Functions
### validatePaymasterUserOp

Payment validation: check if paymaster agree to pay.
Must verify sender is the entryPoint.
Revert to reject this request.
Note that bundlers will reject this method if it changes the state, unless the paymaster is trusted (whitelisted)
The paymaster pre-pays using its deposit, and receive back a refund after the postOp method returns.


```solidity
function validatePaymasterUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 maxCost)
    external
    returns (bytes memory context, uint256 validationData);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`userOp`|`UserOperation`|the user operation|
|`userOpHash`|`bytes32`|hash of the user's request data.|
|`maxCost`|`uint256`|the maximum cost of this transaction (based on maximum gas and gas price from userOp)|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`context`|`bytes`|value to send to a postOp zero length to signify postOp is not required.|
|`validationData`|`uint256`|the last block timestamp this operation is valid, or zero if it is valid indefinitely. Note that the validation code cannot use block.timestamp (or block.number) directly.|


### getStake

Get the Paymaster stake on the entryPoint, which is used for DDOS protection.


```solidity
function getStake() external view returns (uint112);
```

### getDeposit

Get the Paymaster deposit on the entryPoint, which is used to pay for gas.


```solidity
function getDeposit() external view returns (uint112);
```

### deposit

Add a deposit for this paymaster to the entryPoint.


```solidity
function deposit() external payable;
```

### addStake

Add to the account's stake - amount and delay.


```solidity
function addStake(uint32 _unstakeDelaySeconds) external payable;
```

