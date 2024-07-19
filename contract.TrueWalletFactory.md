# TrueWalletFactory
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/wallet/TrueWalletFactory.sol)

**Inherits:**
Ownable, Pausable, [WalletErrors](/src/common/Errors.sol/contract.WalletErrors.md)

A factory contract for deploying and managing TrueWallet smart contracts using CREATE2 and CREATE3 for deterministic addresses.

*This contract allows for the creation of TrueWallet instances with predictable addresses.*


## State Variables
### walletImplementation
Address of the wallet implementation contract.


```solidity
address public immutable walletImplementation;
```


### entryPoint
Address of the entry point contract.


```solidity
address public immutable entryPoint;
```


## Functions
### constructor

*Initializes the factory with the wallet implementation and entry point addresses.*


```solidity
constructor(address _walletImpl, address _owner, address _entryPoint) Pausable();
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_walletImpl`|`address`|Address of the wallet implementation contract.|
|`_owner`|`address`|Address of the owner of this factory contract.|
|`_entryPoint`|`address`|Address of the entry point contract.|


### createWallet

Deploy a new TrueWallet smart contract using CREATE3.


```solidity
function createWallet(bytes memory _initializer, bytes32 _salt) external whenNotPaused returns (TrueWallet proxy);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_initializer`|`bytes`|Initialization data for the new wallet.|
|`_salt`|`bytes32`|A unique salt value used in the CREATE3 operation for deterministic address generation.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`proxy`|`TrueWallet`|The address of the newly created TrueWallet contract.|


### getWalletAddress

Computes the deterministic address for a potential wallet deployment using CREATE3.

*This doesn't deploy the wallet, just calculates its address using the provided salt.*


```solidity
function getWalletAddress(bytes32 _salt) public view returns (address proxy);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_salt`|`bytes32`|A unique salt value used in the CREATE3 operation for deterministic address generation.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`proxy`|`address`|The address of the wallet that would be created using the provided salt.|


### getInitializer

Constructs the initializer payload for wallet creation.

*This function prepares the data required to initialize a new wallet, encoding it for the constructor.*


```solidity
function getInitializer(address _entryPoint, address _walletOwner, bytes[] calldata _modules)
    public
    pure
    returns (bytes memory initializer);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_entryPoint`|`address`|The address of the EntryPoint contract for the new wallet.|
|`_walletOwner`|`address`|The owner address for the new wallet.|
|`_modules`|`bytes[]`|Array of initial module addresses with respective init data for the wallet.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`initializer`|`bytes`|The encoded initializer payload.|


### proxyCode

Returns the proxy's creation code.

*This public function is used to access the creation code of the TrueWalletProxy contract.*


```solidity
function proxyCode() external pure returns (bytes memory);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes`|A byte array representing the proxy's creation code.|


### _proxyCode

*Provides the low-level creation code used by the `proxyCode` function.*


```solidity
function _proxyCode() private pure returns (bytes memory);
```
**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`bytes`|The creation code of the TrueWalletProxy contract.|


### deposit

Deposit funds into the EntryPoint associated with the factory.


```solidity
function deposit() public payable;
```

### withdrawTo

Withdraw funds from the EntryPoint.


```solidity
function withdrawTo(address payable _withdrawAddress, uint256 _withdrawAmount) public onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_withdrawAddress`|`address payable`|The address to send withdrawn funds to.|
|`_withdrawAmount`|`uint256`|The amount of funds to withdraw.|


### addStake

*Add to the account's stake - amount and delay any pending unstake is first cancelled.*


```solidity
function addStake(uint32 _unstakeDelaySec) external payable onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_unstakeDelaySec`|`uint32`|the new lock duration before the deposit can be withdrawn.|


### unlockStake

*Unlock staked funds from the EntryPoint contract.*


```solidity
function unlockStake() external onlyOwner;
```

### withdrawStake

*Withdraw unlocked staked funds from the EntryPoint contract.*


```solidity
function withdrawStake(address payable _withdrawAddress) external onlyOwner;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`_withdrawAddress`|`address payable`|The address to send withdrawn funds to.|


### pause

Pause the factory to prevent new wallet creation.


```solidity
function pause() public onlyOwner;
```

### unpause

Resume operations and allow new wallet creation.


```solidity
function unpause() public onlyOwner;
```

## Events
### TrueWalletCreation
Event emitted when a new TrueWallet is created.


```solidity
event TrueWalletCreation(TrueWallet wallet);
```

