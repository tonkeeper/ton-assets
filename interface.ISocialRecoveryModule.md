# ISocialRecoveryModule
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/SocialRecoveryModule/ISocialRecoveryModule.sol)

*If a user is already in a recovery process, they cannot change guardians.
If a user starts the recovery process while guardians are being changed, the change of guardians will be canceled.*


## Functions
### getGuardians

Fetch the guardians set for a given wallet


```solidity
function getGuardians(address wallet) external returns (address[] memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet for which guardians are being fetched|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`address[]`|An array of guardian addresses|


### updatePendingGuardians

Begin the process to update guardians, changes are effective after a waiting period

*Begin the process of updating guardians. The change becomes effective after 2 days.*


```solidity
function updatePendingGuardians(
    address[] calldata guardians,
    uint256 threshold,
    bytes32 guardianHash,
    uint256 pendingUntil
) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`guardians`|`address[]`|List of new guardian addresses|
|`threshold`|`uint256`|The new threshold of guardians required|
|`guardianHash`|`bytes32`|Hash related to the new set of guardians|
|`pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### cancelSetGuardians

Cancel the process of updating guardians


```solidity
function cancelSetGuardians(address wallet) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet for which the process is being canceled|


### approveRecovery

A single guardian approves the recovery process


```solidity
function approveRecovery(address wallet, address[] calldata newOwners, uint256 pendingUntil) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet being recovered|
|`newOwners`|`address[]`|The new owner(s) of the wallet post recovery|
|`pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### batchApproveRecovery

Multiple guardians approve a recovery process

*A function where multiple guardians can approve a recovery.
If over half the guardians confirm, there's a 2-day waiting period.
If all guardians confirm, the recovery is executed immediately.*


```solidity
function batchApproveRecovery(
    address wallet,
    address[] calldata newOwner,
    uint256 signatureCount,
    bytes memory signatures,
    uint256 pendingUntil
) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet being recovered|
|`newOwner`|`address[]`|The new owner(s) of the wallet post recovery|
|`signatureCount`|`uint256`|The count of signatures from guardians|
|`signatures`|`bytes`|The actual signatures from the guardians|
|`pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### executeRecovery

Execute the recovery process for a wallet


```solidity
function executeRecovery(address wallet) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet being recovered|


### cancelRecovery

Cancel an ongoing recovery process for a wallet


```solidity
function cancelRecovery(address wallet) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`wallet`|`address`|The address of the wallet for which the recovery process is being canceled|


## Events
### AnonymousGuardianRevealed
Emitted when guardians for a wallet are revealed without disclosing their identity


```solidity
event AnonymousGuardianRevealed(address indexed wallet, address[] indexed guardians, bytes32 guardianHash);
```

### ApproveRecovery
Emitted when a guardian approves a recovery


```solidity
event ApproveRecovery(address indexed wallet, address indexed guardian, bytes32 indexed recoveryHash);
```

### BatchApproveRecovery
Emitted when a batch approval for a wallet recovery is processed.


```solidity
event BatchApproveRecovery(
    address indexed wallet,
    address[] indexed newOwners,
    uint256 signatureCount,
    bytes signatures,
    bytes32 indexed recoveryHash
);
```

### PendingRecovery
Indicates a recovery process is pending and waiting for approval or execution


```solidity
event PendingRecovery(address indexed wallet, address[] indexed newOwners, uint256 nonce, uint256 executeAfter);
```

### SocialRecoveryExecuted
Indicates a recovery process has been executed successfully


```solidity
event SocialRecoveryExecuted(address indexed wallet, address[] indexed newOwners);
```

### SocialRecoveryCanceled
Indicates a recovery process has been canceled


```solidity
event SocialRecoveryCanceled(address indexed wallet, uint256 nonce);
```

## Errors
### SocialRecovery__Unauthorized
*Throws when an operation is attempted by an unauthorized entity.*


```solidity
error SocialRecovery__Unauthorized();
```

### SocialRecovery__NoOngoingRecovery
*Throws when an operation related to an ongoing recovery is attempted, but no recovery is in progress.*


```solidity
error SocialRecovery__NoOngoingRecovery();
```

### SocialRecovery__OngoingRecovery
*Throws when an operation that requires no ongoing recovery is attempted, but a recovery is currently in progress.*


```solidity
error SocialRecovery__OngoingRecovery();
```

### SocialRecovery__OnchainGuardianConfigError
*Throws when there's an attempt to set an anonymous guardian alongside an on-chain guardian.*


```solidity
error SocialRecovery__OnchainGuardianConfigError();
```

### SocialRecovery__AnonymousGuardianConfigError
*Throws when there's a configuration error related to anonymous guardians.*


```solidity
error SocialRecovery__AnonymousGuardianConfigError();
```

### SocialRecovery__InvalidThreshold
*Throws when the threshold is not within the valid range.*


```solidity
error SocialRecovery__InvalidThreshold();
```

### SocialRecovery__NoPendingGuardian
*Throws when no pending guardian is set.*


```solidity
error SocialRecovery__NoPendingGuardian();
```

### SocialRecovery__InvalidGuardianList
*Throws when not valid guardian list is provided.*


```solidity
error SocialRecovery__InvalidGuardianList();
```

### SocialRecovery__InvalidGuardianHash
*Throws when not valid guardian hash is provided.*


```solidity
error SocialRecovery__InvalidGuardianHash();
```

### SocialRecovery__OwnersEmpty
*Throws when the list of owners is empty.*


```solidity
error SocialRecovery__OwnersEmpty();
```

### SocialRecovery__RecoveryPeriodStillPending
*Throws when recovery period still pending.*


```solidity
error SocialRecovery__RecoveryPeriodStillPending();
```

### SocialRecovery__NotEnoughApprovals
*Thrown if there are not enough approvals from guardians to proceed with a recovery operation.*


```solidity
error SocialRecovery__NotEnoughApprovals();
```

### SocialRecovery__AnonymousGuardianNotRevealed
*Thrown if an anonymous guardian has not been revealed when required.*


```solidity
error SocialRecovery__AnonymousGuardianNotRevealed();
```

### SocialRecovery__OnlyWalletItselfCanCancelRecovery
*Thrown if any entity other than the wallet itself attempts to cancel a recovery process.*


```solidity
error SocialRecovery__OnlyWalletItselfCanCancelRecovery();
```

