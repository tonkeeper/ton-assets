# IWalletFactory
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/interfaces/IWalletFactory.sol)

Interface for the WalletFactory contract responsible for deploying and managing smart wallets.


## Functions
### createWallet

Deploy a smart wallet with specified entryPoint and walletOwner.

*If no initCode is passed, the function returns the CREATE2 computed address.*


```solidity
function createWallet(address entryPoint, address walletOwner, bytes[] calldata modules, bytes32 salt)
    external
    returns (TrueWallet);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`entryPoint`|`address`|The address of the EntryPoint contract.|
|`walletOwner`|`address`|The address of the wallet owner.|
|`modules`|`bytes[]`|An array of modules with init data to be associated with the wallet.|
|`salt`|`bytes32`|A unique salt for CREATE2 deployment.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`TrueWallet`|The address of the newly created TrueWallet contract.|


### getWalletAddress

Computes the address of a smart wallet using CREATE2, deterministically.


```solidity
function getWalletAddress(address entryPoint, address walletOwner, bytes[] calldata modules, bytes32 salt)
    external
    view
    returns (address);
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`entryPoint`|`address`|The address of the EntryPoint contract.|
|`walletOwner`|`address`|The address of the wallet owner.|
|`modules`|`bytes[]`|An array of modules with init data to be associated with the wallet.|
|`salt`|`bytes32`|A unique salt for CREATE2 deployment.|

**Returns**

|Name|Type|Description|
|----|----|-----------|
|`<none>`|`address`|The computed wallet address.|


