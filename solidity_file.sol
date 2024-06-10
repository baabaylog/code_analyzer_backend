// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SampleContract {
    // State variable to store the owner of the contract
    address public owner;

    // Event to log the receipt of Ether
    event Received(address sender, uint256 amount);

    // Event to log fallback function calls
    event FallbackCalled(address sender, uint256 amount, bytes data);

    // Constructor to set the owner
    constructor() {
        owner = msg.sender;
    }

    // Function to receive Ether. `msg.data` must be empty
    receive() external payable {
        emit Received(msg.sender, msg.value);
    }

    // Fallback function is called when `msg.data` is not empty
    fallback() external payable {
        emit FallbackCalled(msg.sender, msg.value, msg.data);
    }

    // Function to withdraw Ether from the contract
    function withdraw(uint256 amount) external {
        require(msg.sender == owner, "Only the owner can withdraw");
        require(amount <= address(this).balance, "Insufficient balance");
        payable(owner).transfer(amount);
    }

    // Function to check the balance of the contract
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
