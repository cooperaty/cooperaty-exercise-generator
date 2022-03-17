import { SignerWallet, SolanaProvider } from "@saberhq/solana-contrib";
import { Commitment, ConfirmOptions, Connection } from "@solana/web3.js";
import { WalletAdapter } from '../@types/types'
import { TrainerSDK } from "./trainer";
// import fs from 'fs';


// const keypair = Keypair.generate();
// const publickey = String(keypair.publicKey)
// const secretkey = String(keypair.secretKey)

// const cidAux = "bafkreieivicgumpo6igyqmsnrhunsnqkne5aed23pzlekbnglfingxg6te"

// const datenow = Date.now()
// // eslint-disable-next-line @typescript-eslint/restrict-plus-operands
// fs.writeFileSync("./keys/"+datenow+".txt", publickey +"\n"+ secretkey);

export async function sdkConnection(wallet: SignerWallet | WalletAdapter){
  const connection = new Connection('https://api.google.devnet.solana.com', 'processed' as Commitment)
  const sdk = TrainerSDK.init(getProvider(connection, wallet));
  await sdk.getAirdrop({})
  return sdk
}

const getProvider = (
  connection: Connection,
  wallet: SignerWallet | WalletAdapter
) => {
  return SolanaProvider.init({
    connection,
    wallet,
    opts: connection.commitment as ConfirmOptions,
  })
}

