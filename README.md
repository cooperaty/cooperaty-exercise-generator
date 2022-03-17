# Cooperaty exercise generator
Ok, now the exercises generator is working, later i'll upload a better and more compleate readme.
For now the exercise generator, create the `json` files, upload the `JSONs` to `nft.storage` and then with the `CIDs` of the exercises, we create the exercises in the `DevNet` of Solana.

This code must be reviewed and cleaned, use at your own risk.

It would only be necessary to implement listenExercise.

## Running the generator locally

1. Install python 3.7+ (<https://www.python.org/downloads/>), and Git (<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>)
2. Run `git clone https://github.com/cooperaty/cooperaty-exercise-generator && cd cooperaty-exercise-generator` to get the exercise generator source code.
3. Config the API and API Secret for Binance (<https://www.binance.com/es/support/faq/c-6>) on `config.py`, to get the data.
4. Config the APIs from nft.storage on `storage.ts`, and the api key from TRAINER_PROGRAM_ID on `constants.ts`.
5. `npm install` to install the node modules.
6. `npm run build` to build the program.
7. `npm start` to run the exercise generator.
8. The json files, from the exercises will be save in `./exercises`, `./solutions` and `./key ` from the wallet.

-------------
Old readme

------------------
Uses:

- [Python](https://www.python.org/)
- Linting with [flake8](https://flake8.pycqa.org/en/latest/)
- Formatting with [Prettier](https://prettier.io/)
- Linting, typechecking and formatting on by default using [`husky`](https://github.com/typicode/husky) for commit hooks

## Running the generator locally

1. Install python 3.7+ (<https://www.python.org/downloads/>), and Git (<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>)
2. Run `git clone https://github.com/cooperaty/cooperaty-ui.git && cd cooperaty-ui` to get the exercise generator source code
3. Config the API and API Secret for Binance (<https://www.binance.com/es/support/faq/c-6>) on config.py, to get the data.
4. Run `Ctrl` + `Alt` + `N` to run the code on Windows.

## TODO

- [ ] Make this much more efficient.
- [ ] Look for a better API with more historial.
- [ ] To be able to select which interval to use, instead of using a random one.
- [ ] Make encrypting more efficient.
- [ ] Better name the created files and create a folder for them.
- [ ] Change the generation of the sclaping and day trading exercises.
- [ ] Change the number of prediction candlesticks.
- [ ] IPFS integration
- [ ] Solana integration
- [ ] Generate noised past candles
- [ ] Send the exercise (configuration, the noised past candles and encrypted candles) to IPFS
- [ ] Get the exercise's CID from IPFS
- [ ] Send the exercise's CID to the program (CreateExercise)
- [ ] Activate thread that sends the outcome to the program (CheckExercise) after X time
- [ ] fix "line too long (88 > 79 characters)" flake8 problems
