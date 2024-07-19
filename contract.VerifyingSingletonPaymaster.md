# VerifyingSingletonPaymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/843930f01013ad22976a2d653f9d67aaa82d54f4/src/paymaster/VerifyingSingletonPaymaster.sol)

**Inherits:**
[BasePaymaster](/src/paymaster/BasePaymaster.sol/abstract.BasePaymaster.md), ReentrancyGuard

That this signature is NOT a replacement for wallet signature:
- The paymaster signs to agree to PAY for GAS.
- The wallet signs to prove identity and wallet ownership.

*The paymaster trusts an external signer to sign the transaction.
The calling user must pass the UserOp to that external signer first, which performs whatever
off-chain verification before signing the UserOp.*


## State Variables
### unaccountedEPGasOverhead
*Gas used in EntryPoint._handlePostOp() method (including this#postOp() call)*


```solidity
uint256 private unaccountedEPGasOverhead;
```


### paymasterIdBalances

```solidity
mapping(address => uint256) public paymasterIdBalances;
```


### verifyingSigner

```solidity
address public verifyingSigner;
```


## Functions
### constructor


```solidity
constructor(address _entryPoint, address _owner, address _verifyingSigner) payable BasePaymaster(_entryPoint, _owner);
```

### getBalance

*Get the current deposit for paymasterId (Dapp Depositor address)*


```solidity
function getBalance(address paymasterId) external view returns (uint256 balance);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`paymasterId`|`address`|dapp identifier|


### depositeFor

*Add a deposit for this paymaster and given paymasterId (Dapp Depositor address), used for paying for transaction fees*


```solidity
function depositeFor(address paymasterId) external payable nonReentrant;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`paymasterId`|`address`|dapp identifier for which deposit is being made|


### deposit

*Override the default implementation*


```solidity
function deposit() public payable override;
```

### withdrawTo

*Withdraws the specified amount of gas tokens from the paymaster's balance and transfers them to the specified address*


```solidity
function withdrawTo(address payable withdrawAddress, uint256 amount) public override nonReentrant;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`withdrawAddress`|`address payable`|The address to which the gas tokens should be transferred|
|`amount`|`uint256`|The amount of gas tokens to withdraw|


### setSigner

*Set a new verifying signer address*


```solidity
function setSigner(address newVerifyingSigner) external onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`newVerifyingSigner`|`address`|The new address to be set as the verifying signer|


### setUnaccountedEPGasOverhead

*Set a new unaccountedEPGasOverhead*


```solidity
function setUnaccountedEPGasOverhead(uint256 newValue) external onlyOwner;
```

### getHash

That this signature covers all fields of the UserOperation, except the "paymasterAndData",
which will carry the signature itself.

*This method is called by the off-chain service, to sign the request.
It is called on-chain from the validatePaymasterUserOp, to validate the signature.*


```solidity
function getHash(UserOperation calldata userOp, address paymasterId) public view returns (bytes32);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes32`|hash we're going to sign off-chain (and validate on-chain)|


### _validatePaymasterUserOp

*Verify that an external signer signed the paymaster data of a user operation.
The paymaster data is expected to be the paymaster and a signature over the entire request parameters.*


```solidity
function _validatePaymasterUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 requiredPreFund)
    internal
    override
    returns (bytes memory context, uint256 validationData);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`userOp`|`UserOperation`|The UserOperation struct that represents the current user operation.|
|`userOpHash`|`bytes32`|The hash of the UserOperation struct.|
|`requiredPreFund`|`uint256`|The required amount of pre-funding for the paymaster.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`context`|`bytes`|A context string returned by the entry point after successful validation.|
|`validationData`|`uint256`|An integer returned by the entry point after successful validation.|


### _postOp

*Executes the paymaster's payment conditions*


```solidity
function _postOp(PostOpMode mode, bytes calldata context, uint256 actualGasCost) internal virtual override;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`mode`|`PostOpMode`|tells whether the op succeeded, reverted, or if the op succeeded but cause the postOp to revert|
|`context`|`bytes`|payment conditions signed by the paymaster in `validatePaymasterUserOp`|
|`actualGasCost`|`uint256`|amount to be paid to the entry point in wei|


## Events
### EPGasOverheadChanged

```solidity
event EPGasOverheadChanged(uint256 indexed oldValue, uint256 indexed newValue);
```

### VerifyingSingerChanged

```solidity
event VerifyingSingerChanged(address indexed oldSinger, address indexed newSigner, address indexed actor);
```

### GasDeposited

```solidity
event GasDeposited(address indexed paymasterId, uint256 indexed value);
```

### GasWithdraw

```solidity
event GasWithdraw(address indexed paymasterId, address indexed to, uint256 indexed value);
```

### GasBalanceDeducted

```solidity
event GasBalanceDeducted(address indexed paymasterId, uint256 indexed change);
```

## Errors
### EntryPointCannotBeZero

```solidity
error EntryPointCannotBeZero();
```

### OwnerAddressCannotBeZero

```solidity
error OwnerAddressCannotBeZero();
```

### VerifyingSignerCannotBeZero

```solidity
error VerifyingSignerCannotBeZero();
```

### PaymasterIdCannotBeZero

```solidity
error PaymasterIdCannotBeZero();
```

### DepositeCannotBeZero

```solidity
error DepositeCannotBeZero();
```

### CanNotWithdrawToZeroAddress

```solidity
error CanNotWithdrawToZeroAddress();
```

### InsufficientBalance

```solidity
error InsufficientBalance(uint256 amount, uint256 balance);
```

### InvalidPaymasterSignatureLength

```solidity
error InvalidPaymasterSignatureLength(uint256 sigLength);
```

