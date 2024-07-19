# TokenManager
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/base/TokenManager.sol)

**Inherits:**
[OwnerAuth](/src/authority/OwnerAuth.sol/abstract.OwnerAuth.md), [WalletErrors](/src/common/Errors.sol/contract.WalletErrors.md)

This abstract contract defines a set of functionalities to manage various types of token transfers,
including ETH, ERC20, ERC721, and ERC1155 tokens. It ensures that only the owner can initiate the transfers.


## Functions
### authorized

*Ensures that the function can only be called by the contract owner.*


```solidity
modifier authorized();
```

### transferETH

Transfer ETH out of the wallet.


```solidity
function transferETH(address payable to, uint256 amount) external authorized;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`to`|`address payable`|The recipient's payable address.|
|`amount`|`uint256`|The amount of ETH to transfer.|


### transferERC20

Transfer ERC20 tokens out of the wallet.


```solidity
function transferERC20(address token, address to, uint256 amount) external authorized;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`token`|`address`|The ERC20 token contract address.|
|`to`|`address`|The recipient's address.|
|`amount`|`uint256`|The amount of tokens to transfer.|


### transferERC721

Transfer ERC721 tokens out of the wallet.


```solidity
function transferERC721(address collection, uint256 tokenId, address to) external authorized;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`collection`|`address`|The ERC721 token collection contract address.|
|`tokenId`|`uint256`|The unique token ID to transfer.|
|`to`|`address`|The recipient's address.|


### transferERC1155

Transfer ERC1155 tokens out of the wallet.


```solidity
function transferERC1155(address collection, uint256 tokenId, address to, uint256 amount) external authorized;
```
**Parameters**

|Name|Type|Description|
|----|----|-----------|
|`collection`|`address`|The ERC1155 token collection contract address.|
|`tokenId`|`uint256`|The unique token ID to transfer.|
|`to`|`address`|The recipient's address.|
|`amount`|`uint256`|The amount of the token type to transfer.|


## Events
### TransferredETH
Emitted when ETH is transferred out of the wallet.


```solidity
event TransferredETH(address indexed to, uint256 amount);
```

### TransferredERC20
Emitted when ERC20 tokens are transferred out of the wallet.


```solidity
event TransferredERC20(address token, address indexed to, uint256 amount);
```

### TransferredERC721
Emitted when ERC721 tokens are transferred out of the wallet.


```solidity
event TransferredERC721(address indexed collection, uint256 indexed tokenId, address indexed to);
```

### TransferredERC1155
Emitted when ERC1155 tokens are transferred out of the wallet.


```solidity
event TransferredERC1155(address indexed collection, uint256 indexed tokenId, uint256 amount, address indexed to);
```

