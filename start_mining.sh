#!/bin/bash
# start_mining.sh

# Get the wallet address from the command line argument
WALLET_ADDRESS=$1

# Check if the wallet address is provided
if [ -z "$WALLET_ADDRESS" ]; then
  echo "Error: Wallet address is required."
  exit 1
fi

# Run the Node.js mining script
node mining_script.js --wallet "$WALLET_ADDRESS"
