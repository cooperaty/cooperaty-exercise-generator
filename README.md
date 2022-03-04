# Cooperaty exercise generator

Uses:

- [Python](https://www.python.org/)
- Linting with [flake8](https://flake8.pycqa.org/en/latest/)
- Formatting with [Prettier](https://prettier.io/)

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
