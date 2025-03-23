// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {Challenge} from "../src/Challenge.sol";
import {Create2Factory} from "../src/factory.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    Challenge public challenge;
    Create2Factory public factory;

    address[4] public signers = [
        0xa24b3f601C29a9d26af5C151D172ea716a23dF1c,
        0x7AD65DFcF42e961Ba3E7d59fa4368590A65d87f2,
        0x900C6A8295c23A1e031B39604fD14789028B1899,
        0xEA5511ec9df4aE6FE20e2480d7E60CfCe2556F01
        ];
    
    function run() public {
        vm.startBroadcast();

        challenge = new Challenge(signers);
        console.log("Challenge deployed at :", address(challenge));
        factory = new Create2Factory();

        vm.stopBroadcast();
    }
}
