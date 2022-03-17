from binance.client import Client
import config
import random
import datetime
import json
import sys

# arg from node js
Modality_aux = sys.argv[1]
number_of_exercises = sys.argv[2]
# print(Modality_aux, number_of_exercises)

# binance API connection
client = Client(config.API_KEY, config.API_SECRET)

# all pairs, for future uses
prices = client.get_all_tickers()

# a list where we will storage all binance USDT pairs
USDT_list = []


# invervals
# 1m, 3m, 5m, 15m, 30m
Scalping_interval = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE,
                     Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE]
# 1h,2h,4h
DayTrading_interval = [Client.KLINE_INTERVAL_1HOUR,
                       Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_4HOUR]
# 12h,1D,3D
Swing_interval = [Client.KLINE_INTERVAL_12HOUR,
                  Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_3DAY]
All_intervals = Scalping_interval+DayTrading_interval+Swing_interval
# TODO
# To be able to select which interval to use, instead of using a random one.



# Get all the symbols with the pair USDT
for i in prices:
    if "USDT" == i['symbol'][-4:]:
        USDT_list.append(i['symbol'])

Modality = ""
typeExercise = ""
# see the list of usdt
# print(USDT_list)

timeframes = []

while True:

    aux = 0

    while aux < int(number_of_exercises):

        if Modality_aux == "1":
            Modality = random.choice(Scalping_interval)
            typeExercise = "Scalping"
            # timeframes = ["1m", "3m", "5m", "15m", "30m"]
        elif Modality_aux == "2":
            Modality = random.choice(DayTrading_interval)
            typeExercise = "Intraday"
            # timeframes = ["1h","2h","4h"]
        elif Modality_aux == "3":
            Modality = random.choice(Swing_interval)
            typeExercise = "Swing"
            # timeframes = ["12h","1D","3D"]
        elif Modality_aux == "4":
            Dictionary = {"Scalping":random.choice(Scalping_interval), "Intraday":random.choice(DayTrading_interval), "Swing":random.choice(Swing_interval)}
            typeExercise = random.choice(list(Dictionary)) 
            Modality = Dictionary[typeExercise]
        # print("-----------------------\nThe server is generating a practice exercise...\n-----------------------")
        pair = random.choice(USDT_list)

        # min date for API binance data, but for some reason is better to use an older date, in this case 1 jan, 2014
        # 1 Aug, 17

        random_klines_of_a_pair = client.get_historical_klines(
            pair, Modality, "1 Jan, 2014")

        # we get the firts and the last candle available

        Firts_close_candle = float(random_klines_of_a_pair[0][4])
        Last_close_candle = float(random_klines_of_a_pair[-1:][0][4])

        Firts_date_pair = random_klines_of_a_pair[0][0]
        Last_date_pair = random_klines_of_a_pair[-1:][0][0]

        # random candle milliseconds in epoch time
        random_candle = random.randint(Firts_date_pair, Last_date_pair)

        # get the post and past random candles
        Past_candle_total = random.randint(Firts_date_pair, random_candle)
        Post_candle_total = random.randint(random_candle, Last_date_pair)

        # if you don't wanna know some data, like the date of the random candle comment the next lines.
        date_on_UTC = datetime.datetime.fromtimestamp(
            int(random_candle/1000))
        # print("Date of the random candle: ", date_on_UTC)

        # if you wanna know the date of the past and post candles
        date_on_UTC_past = datetime.datetime.fromtimestamp(
            int(Past_candle_total/1000))
        date_on_UTC_post = datetime.datetime.fromtimestamp(
            int(Post_candle_total/1000))
        # print("Date of the past candle: ", date_on_UTC_past)
        # print("Date of the post candle: ", date_on_UTC_post)

        # # Initial and final price of the pair.
        # print("Initial price of the pair: ", Firts_close_candle,
        #       "Final price of the pair: ",  Last_close_candle)

        # # Randomly chosen pair
        # print("Pair: ", pair)

        # % of the total move of the coin
        # Porcentage_of_move = ((Last_close_candle/Firts_close_candle)-1)*100
        # print(Porcentage_of_move)

        # data for the exercise
        past_klines_of_the_random_pair = client.get_historical_klines(
            pair, Modality, Past_candle_total, random_candle)
        post_klines_of_the_random_pair = client.get_historical_klines(
            pair, Modality, random_candle, Post_candle_total)

        past_candle_total_data = []
        post_candle_total_data = []

        newjson = {
            "candles": [],
            "position": {},
            "solutionCID": "",
            "timeframes": []
        }

        newjson_solution = {
            "candles": [],
            "datetime": "",
            "pair": "",
            "exchange": "",
            "outcome": 0
        }

        candles = []
        candles_solution = []

        # candle = {
        #     "time": 0,
        #     "low": 0,
        #     "high": 0,
        #     "open": 0,
        #     "close": 0,
        #     "volume": 0
        # }

        position = {
            "direction": "",
            "takeProfit": 0,
            "stopLoss": 0,
            "postBars": 0
        }

        solutionCID = ""

        # solution

        for TOHLC in past_klines_of_the_random_pair:
            # TIME, OPEN, HIGH, LOW, CLOSE, VOLUMEN
            past_candle_total_data.append(
                [TOHLC[0], TOHLC[1], TOHLC[2], TOHLC[3], TOHLC[4], TOHLC[5]])

        # TIME, LOW, HIGH, OPEN, CLOSE, VOLUME
        for TLHOCV in past_klines_of_the_random_pair:
            candle = {}
            candle["time"] = TLHOCV[0]
            candle["low"] = float(TLHOCV[3])
            candle["high"] = float(TLHOCV[2])
            candle["open"] = float(TLHOCV[1])
            candle["close"] =float(TLHOCV[4])
            candle["volume"] = float(TLHOCV[5])
            candles.append(candle)

        for TOHLC in post_klines_of_the_random_pair:
            # TIME, OPEN, HIGH, LOW, CLOSE, VOLUMEN
            post_candle_total_data.append(
                [TOHLC[0], TOHLC[1], TOHLC[2], TOHLC[3], TOHLC[4], TOHLC[5]])
        # TIME, LOW, HIGH, OPEN, CLOSE, VOLUME
        for TLHOCV in post_klines_of_the_random_pair:
            candle = {}
            candle["time"] = TLHOCV[0]
            candle["low"] = float(TLHOCV[3])
            candle["high"] = float(TLHOCV[2])
            candle["open"] = float(TLHOCV[1])
            candle["close"] = float(TLHOCV[4])
            candle["volume"] = float(TLHOCV[5])
            candles_solution.append(candle)

        len_past_candle_data = round(len(past_candle_total_data)*0.7)
        len_post_candle_data = round(len(post_candle_total_data)*0.3)

        past_candle_data = []
        post_candle_data = []

        aux_data = 0

        for TOHLC in past_candle_total_data:
            if aux_data < len_past_candle_data:
                past_candle_data.append(TOHLC)
                aux_data += 1

        aux_data_2 = 0
        for TOHLC in post_candle_total_data:
            if aux_data_2 < len_post_candle_data:
                post_candle_data.append(TOHLC)
                aux_data_2 += 1

        # we add this in the meantime since the data often does not have [0][4] IndexError: list index out of range
        try:
            Past_candle_close = past_candle_data[0][4]
            Post_candle_close = post_candle_data[-1:][0][4]
        except IndexError:
            continue

        # outcome maximo
        Outcome_real = ((float(Post_candle_close) /
                         float(Past_candle_close))-1)*100
        Outcome = round(abs(Outcome_real))  # 0.4 = 40%
        # 1 == true, is an exercise that does not seek to trick the practitioner, 0 is the opposite.
        binary_random = random.randint(0, 1)

        Take_profit = Outcome*round(random.random(), 2)
        Stop_lose = Take_profit*0.5  # TODO make this more uniform but random

        if Outcome_real >= 0 and binary_random == 1 or Outcome_real <= 0 and binary_random == 0:
            position = "long_position"
        else:
            position = "short_position"

        bars = len(past_candle_data) + len(post_candle_data) - \
            1  # to rest the reapeat central candle

        # timeframe
        if Modality_aux == 1:
            metadata_timeframe = str(Modality[0])
        else:
            metadata_timeframe = str(Modality).upper()

        # data_file["metadata"]["timeframe"] = metadata_timeframe

        position = {
            "direction": position,
            "takeProfit": round(Take_profit/100,3),
            "stopLoss": round(Stop_lose/100, 3),
            "postBars": bars
        }

        # writing the new json:
        newjson["candles"] = candles
        newjson["position"] = position
        newjson["solutionCID"] = "abcd"
        newjson["type"] = typeExercise
        # newjson["timeframes"] = timeframes
        newjson["timeframes"] = [metadata_timeframe]

        newjson_solution["candles"] = candles_solution
        newjson_solution["datetime"] = str(date_on_UTC)
        newjson_solution["outcome"] = Outcome
        newjson_solution["pair"] = pair
        # because we use binance apy, we just get data from this exchange.
        newjson_solution["exchange"] = "Binance"



        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

        # print(
        #     "The server is generating the exercise and solution files in json format.")
        with open('./exercises/e-'+str(suffix)+'.json', 'w') as outfile:
            json.dump(newjson, outfile)

        with open('./solutions/s-'+str(suffix)+'.json', 'w') as outfile:
            json.dump(newjson_solution, outfile)
        print('e-'+str(suffix)+'.json')
        print('s-'+str(suffix)+'.json')
        print(Outcome)
        aux += 1
        continue
    break

