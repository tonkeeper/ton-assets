# IStakeManager
[Git Source](https://github.com/TrueWallet/contracts/blob/db2e75cb332931da5fdaa38bec9e4d367be1d851/src/interfaces/IStakeManager.sol)

Manage deposits and stakes.
Deposit is just a balance used to pay for UserOperations (either by a paymaster or an account).
Stake is value locked for at least "unstakeDelay" by a paymaster.


## Functions
### getDepositInfo


```solidity
function getDepositInfo(address account) external view returns (DepositInfo memory info);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`info`|`DepositInfo`|- full deposit information of given account|


### balanceOf


```solidity
function balanceOf(address account) external view returns (uint256);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`uint256`|the deposit (for gas payment) of the account|


### depositTo

Add to the deposit of the given account


```solidity
function depositTo(address account) external payable;
```

### addStake

Add to the account's stake - amount and delay
any pending unstake is first cancelled.


```solidity
function addStake(uint32 _unstakeDelaySec) external payable;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_unstakeDelaySec`|`uint32`|the new lock duration before the deposit can be withdrawn.|


### unlockStake

Attempt to unlock the stake.
the value can be withdrawn (using withdrawStake) after the unstake delay.


```solidity
function unlockStake() external;
```

### withdrawStake

Withdraw from the (unlocked) stake.
must first call unlockStake and wait for the unstakeDelay to pass


```solidity
function withdrawStake(address payable withdrawAddress) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`withdrawAddress`|`address payable`|the address to send withdrawn value.|


### withdrawTo

Withdraw from the deposit.


```solidity
function withdrawTo(address payable withdrawAddress, uint256 withdrawAmount) external;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`withdrawAddress`|`address payable`|the address to send withdrawn value.|
|`withdrawAmount`|`uint256`|the amount to withdraw.|


## Events
### Deposited

```solidity
event Deposited(address indexed account, uint256 totalDeposit);
```

### Withdrawn

```solidity
event Withdrawn(address indexed account, address withdrawAddress, uint256 amount);
```

### StakeLocked
Emitted when stake or unstake delay are modified


```solidity
event StakeLocked(address indexed account, uint256 totalStaked, uint256 unstakeDelaySec);
```

### StakeUnlocked
Emitted once a stake is scheduled for withdrawal


```solidity
event StakeUnlocked(address indexed account, uint256 withdrawTime);
```

### StakeWithdrawn

```solidity
event StakeWithdrawn(address indexed account, address withdrawAddress, uint256 amount);
```

## Structs
### DepositInfo
*sizes were chosen so that (deposit,staked, stake) fit into one cell (used during handleOps)
and the rest fit into a 2nd cell.
112 bit allows for 10^15 eth
48 bit for full timestamp
32 bit allows 150 years for unstake delay*


```solidity
struct DepositInfo {
    uint112 deposit;
    bool staked;
    uint112 stake;
    uint32 unstakeDelaySec;
    uint48 withdrawTime;
}
```

### StakeInfo

```solidity
struct StakeInfo {
    uint256 stake;
    uint256 unstakeDelaySec;
}
```

