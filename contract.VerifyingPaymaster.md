# VerifyingPaymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/paymaster/VerifyingPaymaster.sol)

**Inherits:**
[ITruePaymaster](/src/paymaster/ITruePaymaster.sol/interface.ITruePaymaster.md), Ownable

A paymaster that uses external service to decide whether to pay for the UserOp.
The paymaster trusts an external signer to sign the transaction.
The calling user must pass the UserOp to that external signer first, which performs
whatever off-chain verification before signing the UserOp.
Note that this signature is NOT a replacement for the account-specific signature:
- the paymaster checks a signature to agree to PAY for GAS.
- the account checks a signature to prove identity and account ownership.


## State Variables
### entryPoint

```solidity
IEntryPoint public entryPoint;
```


### verifyingSigner

```solidity
address public immutable verifyingSigner;
```


### VALID_TIMESTAMP_OFFSET

```solidity
uint256 private constant VALID_TIMESTAMP_OFFSET = 20;
```


### SIGNATURE_OFFSET

```solidity
uint256 private constant SIGNATURE_OFFSET = 84;
```


### senderNonce

```solidity
mapping(address => uint256) public senderNonce;
```


## Functions
### onlyEntryPoint

Validate that only the entryPoint is able to call a method


```solidity
modifier onlyEntryPoint();
```

### constructor


```solidity
constructor(IEntryPoint _entryPoint, address _verifyingSigner, address _owner);
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

Verify our external signer signed this request.
the "paymasterAndData" is expected to be the paymaster and a signature over the entire request params
paymasterAndData[:20] : address(this)
paymasterAndData[20:84] : abi.encode(validUntil, validAfter)
paymasterAndData[84:] : signature


```solidity
function validatePaymasterUserOp(UserOperation calldata userOp, bytes32, uint256 requiredPreFund)
    external
    returns (bytes memory context, uint256 validationData);
```

### getHash

Return the hash we're going to sign off-chain (and validate on-chain)
this method is called by the off-chain service, to sign the request.
it is called on-chain from the validatePaymasterUserOp, to validate the signature.
note that this signature covers all fields of the UserOperation, except the "paymasterAndData",
which will carry the signature itself.


```solidity
function getHash(UserOperation calldata userOp, uint48 validUntil, uint48 validAfter) public view returns (bytes32);
```

### parsePaymasterAndData


```solidity
function parsePaymasterAndData(bytes calldata paymasterAndData)
    public
    pure
    returns (uint48 validUntil, uint48 validAfter, bytes calldata signature);
```

### pack


```solidity
function pack(UserOperation calldata userOp) internal pure returns (bytes memory ret);
```

### postOp

Handler for charging the sender (smart wallet) for the transaction after it has been paid for by the paymaster


```solidity
function postOp(PostOpMode mode, bytes calldata context, uint256 actualGasCost) external onlyEntryPoint;
```

### addStake

Add stake for this paymaster to the EntryPoint. Used to allow the paymaster to operate and prevent DDOS


```solidity
function addStake(uint32 _unstakeDelaySeconds) external payable onlyOwner;
```

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
function deposit() external payable;
```

### withdraw

Withdraw paymaster deposit to an address


```solidity
function withdraw(address payable to, uint256 amount) external onlyOwner;
```

### withdrawAll

Withdraw all paymaster deposit to an address


```solidity
function withdrawAll(address payable to) external onlyOwner;
```

## Events
### UpdateEntryPoint

```solidity
event UpdateEntryPoint(address indexed _newEntryPoint, address indexed _oldEntryPoint);
```

## Errors
### InvalidEntryPoint
*Reverts in case not valid entryPoint or owner*


```solidity
error InvalidEntryPoint();
```

