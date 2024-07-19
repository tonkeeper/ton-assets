# Paymaster
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/paymaster/Paymaster.sol)

**Inherits:**
[ITruePaymaster](/src/paymaster/ITruePaymaster.sol/interface.ITruePaymaster.md), Ownable


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
constructor(address _entryPoint, address _owner);
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

Validates that the paymaster will pay for the user transaction. Custom checks can be performed here, to ensure for example
that the user has sufficient funds to pay for the transaction. It could just return an empty context and deadline to allow
all transactions by everyone to be paid for through this paymaster.


```solidity
function validatePaymasterUserOp(UserOperation calldata userOp, bytes32 userOpHash, uint256 maxCost)
    external
    pure
    override
    returns (bytes memory context, uint256 validationData);
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

