// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IKey {
    function Key() external view returns (string memory);
}

contract Challenge {

    address public owner = 0xa24b3f601C29a9d26af5C151D172ea716a23dF1c;
    address public keyContract = 0xDbCA158868a2701A82Fa2C7748038363eEFE07cf;
    address[4] public authorizedSigners;
    bool public unlocked;
    bool public solved = false;

    mapping(bytes32 => bool) public usedSignatures;

    event VaultUnlocked(address indexed by);
    event VaultDestroyed(address indexed by);

    constructor(address[4] memory _signers) {
        for (uint i = 0; i < _signers.length; i++) {
            authorizedSigners[i] = _signers[i];
        }
        unlocked = false;
    }

    function authenticate(
        bytes32 hash,
        uint8 v1, bytes32 r1, bytes32 s1,
        uint8 v2, bytes32 r2, bytes32 s2
    ) public {
        require(!unlocked, "Vault already unlocked");
        require(msg.sender == owner, "Only owner can unlock the vault");

        string memory key = IKey(keyContract).Key();
        require(
            keccak256(abi.encodePacked("Normandie4ever")) == keccak256(abi.encodePacked(key)), 
            "Invalid Key contract"
        );

        require(abi.encodePacked(v1, r1, s1).length == 65, "Signature 1 must be 65 bytes");
        require(abi.encodePacked(v2, r2, s2).length == 65, "Signature 2 must be 65 bytes");

        bytes32 sig1Hash = keccak256(abi.encodePacked(v1, r1, s1));
        bytes32 sig2Hash = keccak256(abi.encodePacked(v2, r2, s2));

        require(!usedSignatures[sig1Hash], "Signature 1 already used");
        require(!usedSignatures[sig2Hash], "Signature 2 already used");

        require(sig1Hash != sig2Hash, "Identical signatures not allowed");

        usedSignatures[sig1Hash] = true;
        usedSignatures[sig2Hash] = true;

        address signer1 = _recoverSigner(hash, v1, r1, s1);
        address signer2 = _recoverSigner(hash, v2, r2, s2);

        require(_isAuthorized(signer1), "Signer1 not authorized");
        require(_isAuthorized(signer2), "Signer2 not authorized");

        unlocked = true;
        emit VaultUnlocked(msg.sender);
    }

    function destroyVault(address emergencyAddr) public {
        // No self destruct but imagine it was here :))
        require(unlocked, "Vault is locked");
        emit VaultDestroyed(msg.sender);
        payable(emergencyAddr).transfer(address(this).balance);
        solved = true;
    }

    function isSolved() public view returns (bool) {
        return solved;
    }

    function _isAuthorized(address signer) internal view returns (bool) {
        for (uint i = 0; i < authorizedSigners.length; i++) {
            if (authorizedSigners[i] == signer) {
                return true;
            }
        }
        return false;
    }

    function _recoverSigner(bytes32 hash, uint8 v, bytes32 r, bytes32 s) internal pure returns (address) {
        return ecrecover(hash, v, r, s);
    }
}
