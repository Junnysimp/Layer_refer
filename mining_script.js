import fs from 'fs/promises';
import log from './utils/logger.js';
import { delay } from './utils/helper.js';
import LayerEdge from './utils/socket.js';

// Parse command-line arguments
const args = process.argv.slice(2);
const walletAddress = args[1]; // Get the wallet address from the --wallet argument

if (!walletAddress) {
  log.error("Wallet address is required. Usage: node mining_script.js --wallet <wallet_address>");
  process.exit(1);
}

async function runMining(walletAddress) {
  try {
    // Read wallets from wallets.json
    const wallets = JSON.parse(await fs.readFile("wallets.json", "utf-8"));

    // Find the wallet with the matching address
    const wallet = wallets.find(w => w.address === walletAddress);
    if (!wallet) {
      log.error(`Wallet ${walletAddress} not found in wallets.json`);
      return;
    }

    const { privateKey } = wallet;

    // Start mining for the wallet
    const socket = new LayerEdge(null, privateKey); // Pass null for proxy if not needed
    log.info(`Processing Wallet Address: ${walletAddress}`);
    log.info(`Checking Node Status for: ${walletAddress}`);
    const isRunning = await socket.checkNodeStatus();

    if (isRunning) {
      log.info(`Wallet ${walletAddress} is running - trying to claim node points...`);
      await socket.stopNode();
    }

    log.info(`Trying to reconnect node for Wallet: ${walletAddress}`);
    await socket.connectNode();

    log.info(`Checking Node Points for Wallet: ${walletAddress}`);
    await socket.checkNodePoints();
  } catch (error) {
    log.error(`Error Processing wallet ${walletAddress}:`, error.message);
  }
}

// Run the mining process
runMining(walletAddress);
