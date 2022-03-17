// import { ExerciseData } from './programs/trainer';
import { PythonShell } from 'python-shell';
const editJsonFile = require("edit-json-file");
import { store } from './storage'
import { dynamic } from 'set-interval-async'
import {sdkConnection} from './sdk'
const { setIntervalAsync: setIntervalAsyncD } = dynamic
import fs from 'fs';

import { Keypair } from "@solana/web3.js";
import { SignerWallet } from "@saberhq/solana-contrib";



// arg we receive after the node started, with <modality> <number of exersice>
// modality 1:scalping, 2:intraday, 3:Swing, 4:Random.
const args = process.argv.slice(2)
if (args.length !== 2) {
    console.error(`usage: ${process.argv[0]} ${process.argv[1]} <modality> <number of exersice>`)
    process.exit(1)
}
// for the wallet
const keypair = Keypair.generate();
const publickey = String(keypair.publicKey)
const secretkey = String(keypair.secretKey)
const wallet = new SignerWallet(keypair)

const datenow = Date.now()
// eslint-disable-next-line @typescript-eslint/restrict-plus-operands
fs.writeFileSync("./keys/"+datenow+".txt", publickey +"\n"+ secretkey);

const [modality, numberExercise] = args

let options = {
    pythonOptions: ['-u'],
    // modality and number of exersice
    args: [modality, numberExercise]
};


async function Main() {
    const sdk = await sdkConnection(wallet)
    async function CreateExercises(options) {
        // run the script, to generate the exercises
        PythonShell.run('script.py', options, async function (err, results) {
            let exercises = results
        
            // array of solution cids
            let cidsS = []
            // array of exercise cids
            let cidsE = []
            if (err) throw err;
            console.log('The script has generated the exercises successfully and the storage in IPFS has started + deploy in the devnet.');
            for (let i = 0; i < exercises.length; i = i + 3) {
                let fileNameE = './exercises/' + exercises[i]
                let fileNameS = './solutions/' + exercises[i + 1]

                // for listenExercise uncomment
                // let outcome =  exercises[i + 2]

                // We upload the solution to NFTStorage and we get the cid
                let file = editJsonFile(fileNameE)
                const CidSolutionStoraged = await store(fileNameS)
                cidsS.push(CidSolutionStoraged)
                
                // we save this of the solution to rewrite the exercise json
                file.set('solutionCID', CidSolutionStoraged)
                file.save();
                
                // we save the cid of the exercise for futures uses
                const CidExerciseStoraged = await store(fileNameE)
                cidsE.push(CidExerciseStoraged)
                
                // we create the exercises in the devnet, change the validations_capacity = 1, for testing purposes.
                const exercise = await sdk.createExercise(CidExerciseStoraged,1);
                console.log("✅ Done", exercise);


                // const exercisesFind = await sdk.getFilteredExercises({cid:CidExerciseStoraged});
                // console.log("✅ Done", exercisesFind);

                // // listenExercise
                // const exercisePubkey = await sdk.getExerciseAddress(CidExerciseStoraged);
                // if (!exercisePubkey) console.error("Exercise not found");
                // console.log(`🚀 Listening exercise with outcome ${outcome}...`);
                // sdk.onExerciseChange(
                //     exercisePubkey,
                //     async (exercise: ExerciseData | null) => {
                //       console.log("🔔 Exercise changed", exercise);
                //       if (!exercise) console.error("✅ Done");
                //       if (exercise?.account?.sealed) {
                //         console.log(`🚀 Checking exercise with outcome ${outcome}...`);
                //         await sdk.addOutcome(exercise, outcome);
                //         await sdk.checkAllValidations(exercise);
                //       }
                //     }
                // );

                // // closeExercise
                // console.log("🚀 Close exercise...");
                // if (exercise?.length !== 1) console.error("Exercise not found");
                // const trainer = await sdk.closeExercise(exercise[0]);
                // console.log("✅ Done", trainer);
                // break;
        
            }
            console.log('The exercises were successfully stored in IPFS storage with the CIDs\n', cidsE)
            console.log('solution Cids\n',cidsS);

        });
    }
    // main(options)
    // to make the node forever if we want to do it
    // every how many seconds you want exercises to be generated, a recommendation is use 300000ms, 5 minutes.
    setIntervalAsyncD(
        () => CreateExercises(options),
        30000
      )
    

}


Main()



