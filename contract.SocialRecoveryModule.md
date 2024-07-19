# SocialRecoveryModule
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/modules/SocialRecoveryModule/SocialRecoveryModule.sol)

**Inherits:**
[ISocialRecoveryModule](/src/modules/SocialRecoveryModule/ISocialRecoveryModule.sol/interface.ISocialRecoveryModule.md), [BaseModule](/src/modules/BaseModule.sol/abstract.BaseModule.md)

*Contract module that allows a group of guardians to collectively recover a wallet.
This is intended for scenarios where the wallet owner is unable to access their wallet.
The module adheres to the ISocialRecoveryModule interface and extends BaseModule for shared functionality.*


## State Variables
### NAME

```solidity
string public constant NAME = "True Social Recovery Module";
```


### VERSION

```solidity
string public constant VERSION = "0.0.1";
```


### _DOMAIN_SEPARATOR_TYPEHASH

```solidity
bytes32 private constant _DOMAIN_SEPARATOR_TYPEHASH = 0x8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f;
```


### _SOCIAL_RECOVERY_TYPEHASH

```solidity
bytes32 private constant _SOCIAL_RECOVERY_TYPEHASH = 0x333ef7ecc7b8a82065578df0879cefc36c32344d49afdf1e0370a60babe64feb;
```


### _FUNC_RESET_OWNER

```solidity
bytes4 private constant _FUNC_RESET_OWNER = bytes4(keccak256("resetOwner(address)"));
```


### _FUNC_RESET_OWNERS

```solidity
bytes4 private constant _FUNC_RESET_OWNERS = bytes4(keccak256("resetOwners(address[])"));
```


### walletRecoveryNonce

```solidity
mapping(address => uint256) walletRecoveryNonce;
```


### walletInitSeed

```solidity
mapping(address => uint256) walletInitSeed;
```


### walletGuardian

```solidity
mapping(address => GuardianInfo) internal walletGuardian;
```


### walletPendingGuardian

```solidity
mapping(address => PendingGuardianEntry) internal walletPendingGuardian;
```


### approvedRecords

```solidity
mapping(address => mapping(bytes32 => uint256)) approvedRecords;
```


### recoveryEntries

```solidity
mapping(address => RecoveryEntry) recoveryEntries;
```


### __seed

```solidity
uint128 private __seed;
```


## Functions
### authorized

Throws if the sender is not the wallet itself that authorized this module.


```solidity
modifier authorized(address _wallet);
```

### whenRecovery

Throws if there is no ongoing recovery request.


```solidity
modifier whenRecovery(address _wallet);
```

### whenNotRecovery

Throws if there is an ongoing recovery request.


```solidity
modifier whenNotRecovery(address _wallet);
```

### checkPendingGuardian

Modifier to check and apply pending guardian updates before executing a function.


```solidity
modifier checkPendingGuardian(address _wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet to check.|


### _init

*Internal function to initialize the wallet with guardians, threshold, and guardian hash.
This can set up both on-chain and off-chain (anonymous) guardians.*


```solidity
function _init(bytes calldata data) internal override;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`data`|`bytes`|Encoded data containing guardians, threshold, and guardian hash.|


### _deInit

*Internal function to de-initialize a wallet. This clears all recovery settings.*


```solidity
function _deInit() internal override;
```

### isInit

Checks if a wallet is initialized.


```solidity
function isInit(address _wallet) external view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|bool True if the wallet is initialized, false otherwise.|


### processGuardianUpdates

External function to process any pending guardian updates for a wallet.


```solidity
function processGuardianUpdates(address _wallet) external authorized(sender());
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which to process guardian updates.|


### _checkApplyGuardianUpdate

*Internal function to apply pending guardian updates after the delay period.*


```solidity
function _checkApplyGuardianUpdate(address _wallet) private;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet to update guardians for.|


### updatePendingGuardians

Submits a request to update the guardians for the caller's wallet.
This update is pending for a certain delay before being applied.


```solidity
function updatePendingGuardians(
    address[] calldata _guardians,
    uint256 _threshold,
    bytes32 _guardianHash,
    uint256 _pendingUntil
) external authorized(sender()) whenNotRecovery(sender()) checkPendingGuardian(sender());
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_guardians`|`address[]`|The list of new guardians to be set.|
|`_threshold`|`uint256`|The new threshold for guardian consensus.|
|`_guardianHash`|`bytes32`|The new guardian hash to be used for off-chain guardians.|
|`_pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### cancelSetGuardians

Allows a wallet or its current guardian to cancel a pending guardian update.

*Reverts if there is no pending guardian update or if the caller is not authorized.*

*Applies any pending guardian update before proceeding to cancel the next one.*


```solidity
function cancelSetGuardians(address _wallet) external authorized(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which the pending update is to be cancelled.|


### revealAnonymousGuardians

Reveal the anonymous guardians of a wallet.

*Reverts if the list of guardians is not sorted or the guardian hash doesn't match.*


```solidity
function revealAnonymousGuardians(address _wallet, address[] calldata _guardians, bytes32 _salt)
    public
    authorized(_wallet)
    checkPendingGuardian(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which to reveal guardians.|
|`_guardians`|`address[]`|The array of guardian addresses.|
|`_salt`|`bytes32`|The salt used to hash the anonymous guardian list.|


### approveRecovery

Approve a wallet recovery process initiated by guardians.

*Reverts if no new owners are provided or the caller is not authorized.*


```solidity
function approveRecovery(address _wallet, address[] memory _newOwners, uint256 _pendingUntil)
    external
    authorized(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet undergoing recovery.|
|`_newOwners`|`address[]`|The proposed new array of owner addresses.|
|`_pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### _pendingRecovery

Initiates a new pending recovery process for a given wallet, setting new owners and a future timestamp for execution.


```solidity
function _pendingRecovery(address _wallet, address[] memory _newOwners, uint256 _nonce, uint256 _pendingUntil)
    private;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet undergoing recovery.|
|`_newOwners`|`address[]`|An array of addresses that will be the new owners of the wallet after recovery.|
|`_nonce`|`uint256`|The nonce associated with the recovery process, ensuring the recovery action is unique.|
|`_pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### executeRecovery

Executes a pending recovery operation if all conditions are met.

*This function will revert if the guardian hash is set and there are guardians present,
if the recovery period is still pending, or if there are not enough guardian approvals.
It delegates the actual execution to the `_executeRecovery` internal function.*


```solidity
function executeRecovery(address _wallet) external whenRecovery(_wallet) authorized(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which to execute the recovery operation.|


### _executeRecovery

*Internal function to execute recovery, updating the nonce and transferring ownership.*


```solidity
function _executeRecovery(address _wallet, address[] memory _newOwners) private;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet undergoing recovery.|
|`_newOwners`|`address[]`|The array of new owner addresses to set for the wallet.|


### cancelRecovery

Cancels the ongoing recovery process for a wallet.

*Can only be called by the wallet itself, reverts if the caller is not the wallet.*


```solidity
function cancelRecovery(address _wallet) external authorized(_wallet) whenRecovery(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which to cancel recovery.|


### batchApproveRecovery

Batch approval process for wallet recovery with signatures from guardians.

*Handles both pending and immediate recovery executions based on signatures count.*


```solidity
function batchApproveRecovery(
    address _wallet,
    address[] calldata _newOwners,
    uint256 _signatureCount,
    bytes memory _signatures,
    uint256 _pendingUntil
) external authorized(_wallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet undergoing recovery.|
|`_newOwners`|`address[]`|The proposed new array of owner addresses.|
|`_signatureCount`|`uint256`|The number of signatures provided.|
|`_signatures`|`bytes`|Concatenated signatures from the guardians.|
|`_pendingUntil`|`uint256`|Seconds after the current block until which the update is pending.|


### _newSeed

*Increment and get the new seed for wallet initialization.
The seed is used to uniquely identify the wallet's initialization state.*


```solidity
function _newSeed() private returns (uint128);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint128`|uint128 The incremented seed value.|


### inited

*Internal function to check if a wallet has been initialized.*


```solidity
function inited(address _wallet) internal view override returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|bool True if the wallet has a non-zero initialization seed, indicating it's been initialized.|


### getAnonymousGuardianHash

Generates a hash of the guardians.

*This hash is used to compare against the stored hash for validation.*


```solidity
function getAnonymousGuardianHash(address[] calldata _guardians, bytes32 _salt) public pure returns (bytes32);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_guardians`|`address[]`|Array of guardians' addresses.|
|`_salt`|`bytes32`|Salt value.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes32`|The calculated keccak256 hash of the encoded guardians and salt.|


### getRecoveryEntry

Retrieves the wallet's current ongoing recovery request.


```solidity
function getRecoveryEntry(address _wallet) public view returns (RecoveryEntry memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`RecoveryEntry`|request The wallet's current recovery request|


### getRecoveryApprovals

Retrieves the guardian approval count for this particular recovery request at current nonce.


```solidity
function getRecoveryApprovals(address _wallet, address[] memory _newOwners)
    public
    view
    returns (uint256 approvalCount);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|
|`_newOwners`|`address[]`|The new owners' addresses.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`approvalCount`|`uint256`|The wallet's current recovery request|


### hasGuardianApproved

Retrieves specific guardian approval status a particular recovery request at current nonce.


```solidity
function hasGuardianApproved(address _guardian, address _wallet, address[] calldata _newOwners)
    public
    view
    returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_guardian`|`address`|The guardian.|
|`_wallet`|`address`|The target wallet.|
|`_newOwners`|`address[]`|The new owners' addresses.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|approvalCount The wallet's current recovery request|


### guardiansCount

Counts the number of active guardians for a wallet.


```solidity
function guardiansCount(address _wallet) public view returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|The number of active guardians for a wallet.|


### getGuardians

Get the active guardians for a wallet.


```solidity
function getGuardians(address _wallet) public view returns (address[] memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`address[]`|the list of active guardians for a wallet.|


### getGuardiansHash

*Retrieves the wallet guardian hash.*


```solidity
function getGuardiansHash(address _wallet) public view returns (bytes32);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes32`|guardianHash.|


### isGuardian

Checks if an address is a guardian for a wallet.


```solidity
function isGuardian(address _wallet, address _guardian) public view returns (bool);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|
|`_guardian`|`address`|The address to check.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bool`|`true` if the address is a guardian for the wallet otherwise `false`.|


### threshold

*Retrieves the wallet threshold count.*


```solidity
function threshold(address _wallet) public view returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|Threshold count.|


### nonce

Get the module nonce for a wallet.


```solidity
function nonce(address _wallet) public view returns (uint256);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The target wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|The nonce for this wallet.|


### pendingGuardian

Retrieves the pending guardian update details for a specified wallet.


```solidity
function pendingGuardian(address _wallet) public view returns (uint256, uint256, bytes32, address[] memory);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet for which to retrieve pending guardian details.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|pendingUntil The timestamp until which the update is pending.|
|`<none>`|`uint256`|threshold The new threshold to be set after the update.|
|`<none>`|`bytes32`|guardianHash The new guardian hash to be set after the update.|
|`<none>`|`address[]`|guardians The list of new guardians to be set after the update.|


### checkNSignatures

*Reference from gnosis safe validation.*

*Validates a set of signatures for a given hash, ensuring they are from guardians.*


```solidity
function checkNSignatures(address _wallet, bytes32 _dataHash, uint256 _signatureCount, bytes memory _signatures)
    public;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_wallet`|`address`|The address of the wallet to check signatures for.|
|`_dataHash`|`bytes32`|The hash of the data the signatures should correspond to.|
|`_signatureCount`|`uint256`|The number of signatures to validate.|
|`_signatures`|`bytes`|Concatenated signatures to be split and checked.|


### signatureSplit

Make sure to perform a bounds check for @param _pos, to avoid out of bounds access on @param _signatures

*Divides bytes signature into `uint8 v, bytes32 r, bytes32 s`.*


```solidity
function signatureSplit(bytes memory _signatures, uint256 _pos) internal pure returns (uint8 v, bytes32 r, bytes32 s);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_signatures`|`bytes`|concatenated rsv signatures|
|`_pos`|`uint256`|which signature to read. A prior bounds check of this parameter should be performed, to avoid out of bounds access|


### getChainId

*Returns the chain id used by this contract.*


```solidity
function getChainId() public view returns (uint256);
```

### domainSeparator

Calculates and returns the domain separator for the contract, which is used in EIP-712 typed data signing.

*The domain separator is a unique hash for the domain that includes the contract's name, version, chain ID, and address,
used to prevent signature replay attacks across different domains.*


```solidity
function domainSeparator() public view returns (bytes32);
```

### encodeSocialRecoveryData

*Returns the bytes that are hashed to be signed by guardians.*


```solidity
function encodeSocialRecoveryData(address _wallet, address[] memory _newOwners, uint256 _nonce)
    public
    view
    returns (bytes memory);
```

### getSocialRecoveryHash

*Generates the recovery hash that should be signed by the guardian to authorize a recovery.*


```solidity
function getSocialRecoveryHash(address _wallet, address[] memory _newOwners, uint256 _nonce)
    public
    view
    returns (bytes32);
```

### requiredFunctions

Returns the required function selectors for the smart contract interface.

*These function selectors are used for interface validation.*


```solidity
function requiredFunctions() external pure returns (bytes4[] memory);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes4[]`|selectors An array of bytes4 representing the required function signatures.|


