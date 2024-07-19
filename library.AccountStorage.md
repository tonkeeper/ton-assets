# AccountStorage
[Git Source](https://github.com/TrueWallet/contracts/blob/db2e75cb332931da5fdaa38bec9e4d367be1d851/src/utils/AccountStorage.sol)


## State Variables
### ACCOUNT_SLOT

```solidity
bytes32 private constant ACCOUNT_SLOT = keccak256("truewallet.contracts.AccountStorage");
```


## Functions
### layout


```solidity
function layout() internal pure returns (Layout storage l);
```

## Structs
### RoleData

```solidity
struct RoleData {
    mapping(address => bool) members;
    bytes32 adminRole;
}
```

### Layout

```solidity
struct Layout {
    IEntryPoint entryPoint;
    mapping(address => address) owners;
    uint256[50] __gap_0;
    ILogicUpgradeControl.UpgradeLayout logicUpgrade;
    Initializable.InitializableLayout initializableLayout;
    uint256[50] __gap_1;
    mapping(bytes32 => RoleData) roles;
    mapping(bytes32 => EnumerableSet.AddressSet) roleMembers;
    uint256[50] __gap_2;
    uint64 executeAfter;
    uint16 threshold;
    address[] guardians;
    mapping(address => bool) isGuardian;
    mapping(bytes32 => bool) isExecuted;
    mapping(bytes32 => mapping(address => bool)) isConfirmed;
    uint256[50] __gap_3;
    mapping(address => address) modules;
    mapping(address => mapping(bytes4 => bytes4)) moduleSelectors;
    uint256[50] __gap_4;
}
```

