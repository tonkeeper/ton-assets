# IPaymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/interfaces/IPaymaster.sol)

The interface exposed by a paymaster contract, who agrees to pay the gas for user's operations.
A paymaster must hold a stake to cover the required entrypoint stake and also the gas for the transaction.


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
|`validationData`|`uint256`|signature and time-range of this operation, encoded the same as the return value of validateUserOperation <20-byte> sigAuthorizer - 0 for valid signature, 1 to mark signature failure, otherwise, an address of an "authorizer" contract. <6-byte> validUntil - last timestamp this operation is valid. 0 for "indefinite" <6-byte> validAfter - first timestamp this operation is valid Note that the validation code cannot use block.timestamp (or block.number) directly.|


### postOp

Post-operation handler.
Must verify sender is the entryPoint


```solidity
function postOp(PostOpMode mode, bytes calldata context, uint256 actualGasCost) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`mode`|`PostOpMode`|enum with the following options: opSucceeded - user operation succeeded. opReverted  - user op reverted. still has to pay for gas. postOpReverted - user op succeeded, but caused postOp (in mode=opSucceeded) to revert. Now this is the 2nd call, after user's op was deliberately reverted.|
|`context`|`bytes`|- the context value returned by validatePaymasterUserOp|
|`actualGasCost`|`uint256`|- actual gas used so far (without this postOp call).|


## Enums
### PostOpMode

```solidity
enum PostOpMode {
    opSucceeded,
    opReverted,
    postOpReverted
}
```

