// Author : K.L.M 
// Difficulty : Medium

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Challenge {

    bool public solved = false;
    uint8 public constant STEPS = 10;
    
    mapping(address => uint8) public playerProgress;

    function takeStep(bool choice) public {
        require(!solved, "Challenge already solved!");
        require(playerProgress[msg.sender] < STEPS, "You have already won!");

        bool correctChoice = isSafe(msg.sender, playerProgress[msg.sender]);

        if (choice == correctChoice) {
            playerProgress[msg.sender]++;

            if (playerProgress[msg.sender] == STEPS) {
                solved = true;
            }
        } else {
            playerProgress[msg.sender] = 0; 
        }
    }

    function isSafe(address _player, uint8 step) internal view returns (bool) {
        bytes32 hash = keccak256(abi.encodePacked(_player, step, address(this)));
        return uint8(hash[0]) % 2 == 0;
    }

    function isSolved() public view returns (bool) {
        return solved;
    }
}
