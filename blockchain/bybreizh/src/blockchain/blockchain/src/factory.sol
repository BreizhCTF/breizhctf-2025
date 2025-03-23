// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// 0xad4967EA626502f0b8F89dc172F2BAa13397f1e2 address of the contract factory with first nonce

contract Create2Factory {
    event Deployed(address addr);
    function deploy(uint256 amount, bytes32 salt, bytes memory bytecode) public payable returns (address addr) {
        require(address(this).balance >= amount, "Fonds insuffisants");
        assembly {
            addr := create2(amount, add(bytecode, 0x20), mload(bytecode), salt)
        }
        require(addr != address(0), "Echec du deploiement");
        emit Deployed(addr);
    }
    function computeAddress(bytes32 salt, bytes32 bytecodeHash) public view returns (address) {
        return address(uint160(uint256(keccak256(abi.encodePacked(
            bytes1(0xff),
            address(this),
            salt,
            bytecodeHash
        )))));
    }
}
