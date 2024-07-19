# Upgradeable
[Git Source](https://github.com/TrueWallet/contracts/blob/5a052bc82f5ecbfdc3b7fb992a66fa5b770bcc4b/src/utils/Upgradeable.sol)

*This abstract contract provides a basic framework for upgradeable contracts using the EIP-1967 standard.
It includes functionality to get and set the implementation address, and to upgrade the contract.
EIP-1967 is a standard for handling proxy contracts and their implementation addresses in a predictable manner.*


## State Variables
### _IMPLEMENTATION_SLOT
*Storage slot with the address of the current implementation.
This is the keccak-256 hash of "eip1967.proxy.implementation" subtracted by 1, and is
validated in the constructor.*


```solidity
bytes32 internal constant _IMPLEMENTATION_SLOT = 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
```


### _BITMASK_ADDRESS
*@dev The mask of the lower 160 bits for addresses.*


```solidity
uint256 private constant _BITMASK_ADDRESS = (1 << 160) - 1;
```


### _UPGRADED_EVENT_SIGNATURE
*The `Upgraded` event signature is given by: `keccak256(bytes("Upgraded(address)"))`.*


```solidity
bytes32 private constant _UPGRADED_EVENT_SIGNATURE = 0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b;
```


## Functions
### _getImplementation

*Returns the current implementation address.*


```solidity
function _getImplementation() internal view returns (address implementation);
```

### _setImplementation

*Stores a new address in the EIP1967 implementation slot.*


```solidity
function _setImplementation(address newImplementation) private;
```

### _setImplementationUnsafe

*Stores a new address in the EIP1967 implementation slot.*


```solidity
function _setImplementationUnsafe(address newImplementation) private;
```

### _upgradeTo

*Perform implementation upgrade
Emits an {Upgraded} event.*


```solidity
function _upgradeTo(address newImplementation) internal;
```

### _upgradeToUnsafe

*Perform implementation upgrade
Emits an {Upgraded} event.*


```solidity
function _upgradeToUnsafe(address newImplementation) internal;
```

### _upgradeToAndCall

*Perform implementation upgrade with additional setup call.
Emits an {Upgraded} event.*


```solidity
function _upgradeToAndCall(address newImplementation, bytes memory data) internal;
```

