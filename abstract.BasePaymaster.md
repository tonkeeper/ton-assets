# BasePaymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/843930f01013ad22976a2d653f9d67aaa82d54f4/src/paymaster/BasePaymaster.sol)

**Inherits:**
[IPaymaster](/src/interfaces/IPaymaster.sol/interface.IPaymaster.md), Owned

Helper class for creating a paymaster.
provides helper methods for staking.
validates that the postOp is called only by the entryPoint

Based on Paymaster in: https://github.com/eth-infinitism/account-abstraction


## State Variables
### entryPoint

```solidity
IEntryPoint public entryPoint;
```


## Functions
### onlyEntryPoint

Validate that only the entryPoint is able to call a method


```solidity
modifier onlyEntryPoint();
```

### constructor


```solidity
constructor(address _entryPoint, address _owner) Owned(_owner);
```

### getStake

Get the total paymaster stake on the entryPoint


```solidity
function getStake() public view returns (uint112);
```

### getDeposit

Get the total paymaster deposit on the entryPoint


```solidity
function getDeposit() public view returns (uint112);
```

### setEntryPoint

Set the entrypoint contract, restricted to onlyOwner


```solidity
function setEntryPoint(address _newEntryPoint) external onlyOwner;
```

### validatePaymasterUserOp

payment validation: check if paymaster agrees to pay.
Must verify sender is the entryPoint.
Revert to reject this request.
Note that bundlers will reject this method if it changes the state, unless the paymaster is trusted (whitelisted)
The paymaster pre-pays using its deposit, and receive back a refund after the postOp method returns.


```solidity
function validatePaymasterUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 maxCost)
    external
    override
    onlyEntryPoint
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
|`validationData`|`uint256`|signature and time-range of this operation, encoded the same as the return value of validateUserOperation <20-byte> sigAuthorizer - 0 for valid signature, 1 to mark signature failure, otherwise, an address of an "authorizer" contract. <6-byte> validUntil - last timestamp this operation is valid. 0 for "indefinite" <6-byte> validAfter - first timestamp this operation is valid Note that the validation code cannot use block.timestamp (or block.number) directly.|


### _validatePaymasterUserOp


```solidity
function _validatePaymasterUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 maxCost)
    internal
    virtual
    returns (bytes memory context, uint256 validationData);
```

### postOp

Post-operation handler.
Must verify sender is the entryPoint


```solidity
function postOp(PostOpMode mode, bytes calldata context, uint256 actualGasCost) external override onlyEntryPoint;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`mode`|`PostOpMode`|enum with the following options: opSucceeded - user operation succeeded. opReverted  - user op reverted. still has to pay for gas. postOpReverted - user op succeeded, but caused postOp (in mode=opSucceeded) to revert. Now this is the 2nd call, after user's op was deliberately reverted.|
|`context`|`bytes`|- the context value returned by validatePaymasterUserOp|
|`actualGasCost`|`uint256`|- actual gas used so far (without this postOp call).|


### _postOp


```solidity
function _postOp(PostOpMode mode, bytes calldata context, uint256 actualGasCost) internal virtual;
```

### addStake

Add stake for this paymaster to the entryPoint. Used to allow the paymaster to operate and prevent DDOS


```solidity
function addStake(uint32 unstakeDelaySeconds) external payable onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`unstakeDelaySeconds`|`uint32`|- the unstake delay for this paymaster. Can only be increased.|


### unlockStake

Unlock paymaster stake


```solidity
function unlockStake() external onlyOwner;
```

### withdrawStake

Withdraw paymaster stake, after having unlocked


```solidity
function withdrawStake(address payable to) external onlyOwner;
```

### deposit

Add a deposit for this paymaster to the EntryPoint. Deposit is used to pay user gas fees


```solidity
function deposit() external payable virtual;
```

### withdrawTo

Withdraw paymaster deposit to an address


```solidity
function withdrawTo(address payable to, uint256 amount) external virtual;
```

## Events
### UpdateEntryPoint

```solidity
event UpdateEntryPoint(address indexed newEntryPoint, address indexed oldEntryPoint);
```

## Errors
### InvalidEntryPoint
*Reverts in case not valid entryPoint*


```solidity
error InvalidEntryPoint(address sender);
```

