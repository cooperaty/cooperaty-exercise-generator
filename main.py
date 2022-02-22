import config
import random
import datetime
import json
# import crypto
# import solana
import rsa
# import base58
import base64

from binance.client import Client

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

# TODO
# To be able to select which interval to use, instead of using a random one.

# we get a random interval
Random_Scalping_interval = random.choice(Scalping_interval)
Random_DayTrading_interval = random.choice(DayTrading_interval)
Random_Swing_interval = random.choice(Swing_interval)

# Get all the symbols with the pair USDT
for i in prices:
    if "USDT" == i['symbol'][-4:]:
        USDT_list.append(i['symbol'])

Modality = ""

# see the list of usdt
# print(USDT_list)

while True:

    option = input(
        "-----------------------\nWhat do you want to do:\n1. Generate practice exercise \n0. Exit\n-----------------------\n")

    if option == "0":
        print("The server has finished generating practice exercises.")
        break
    elif option == "1":

        number_of_exercises = input(
            "-----------------------\nNumber of exercises: ")
        Modality_aux = input(
            "-----------------------\nChoose a modality:\n1. Scalping\n2. DayTrading\n3. Swing\n-----------------------\n")

        if Modality_aux == "1":
            Modality = Random_Scalping_interval

        elif Modality_aux == "2":
            Modality = Random_DayTrading_interval

        elif Modality_aux == "3":
            Modality = Random_Swing_interval

        aux = 0

        while aux < int(number_of_exercises):

            # data JSON
            data_file = {"data": {"past": {"t": [], "c": [], "o": [], "h": [], "l": [], "v": []}, "post": {"t": [], "c": [], "o": [], "h": [], "l": [], "v": []}}, "metadata": {
                "position": {"direction": "", "takeProfit": 0, "stopLoss": 0, "bars": 10}, "timeframe": "", "solution": {"datatime": "", "pair": "", "outcome": ""}}}

            data_past_t = []
            data_past_c = []
            data_past_o = []
            data_past_h = []
            data_past_l = []
            data_past_v = []

            data_post_t = []
            data_post_c = []
            data_post_o = []
            data_post_h = []
            data_post_l = []
            data_post_v = []

            metadata_position_direction = ""
            metadata_position_takeProfit = 0
            metadata_position_stopLoss = 0
            metadata_position_bars = 0

            metadata_timeframe = ""
            metadata_solution_datatime = ""
            metadata_solution_pair = ""
            metadata_solution_outcome = ""

            print("-----------------------\nThe server is generating a practice exercise...\n-----------------------")
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
            print("Date of the random candle: ", date_on_UTC)

            # if you wanna know the date of the past and post candles
            date_on_UTC_past = datetime.datetime.fromtimestamp(
                int(Past_candle_total/1000))
            date_on_UTC_post = datetime.datetime.fromtimestamp(
                int(Post_candle_total/1000))
            print("Date of the past candle: ", date_on_UTC_past)
            print("Date of the post candle: ", date_on_UTC_post)

            # Initial and final price of the pair.
            print("Initial price of the pair: ", Firts_close_candle,
                  "Final price of the pair: ",  Last_close_candle)

            # Randomly chosen pair
            print("Pair: ", pair, "\n-----------------------")

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

            for TOHLC in past_klines_of_the_random_pair:
                # TIME, OPEN, HIGH, LOW, CLOSE, VOLUMEN
                past_candle_total_data.append(
                    [TOHLC[0], TOHLC[1], TOHLC[2], TOHLC[3], TOHLC[4], TOHLC[5]])

            for TOHLC in past_klines_of_the_random_pair:
                # TIME, OPEN, HIGH, LOW, CLOSE, VOLUMEN
                post_candle_total_data.append(
                    [TOHLC[0], TOHLC[1], TOHLC[2], TOHLC[3], TOHLC[4], TOHLC[5]])

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

            Past_candle_close = past_candle_data[0][4]
            Post_candle_close = post_candle_data[-1:][0][4]

            # outcome maximo
            Outcome_real = ((float(Post_candle_close) /
                            float(Past_candle_close))-1)*100
            Outcome = abs(Outcome_real)  # 0.4 = 40%
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

            # RSA for encrypting
            (pubkey, privkey) = rsa.newkeys(512)
            f = open('pubkey'+str(Outcome)+'.txt', 'w')
            f.write(str(pubkey))
            f.close()

            f = open('privkey'+str(Outcome)+'.txt', 'w')
            f.write(str(privkey))
            f.close()

            for i in past_candle_data:
                data_past_t.append(i[0])
                data_past_c.append(i[1])
                data_past_o.append(i[2])
                data_past_h.append(i[3])
                data_past_l.append(i[4])
                data_past_v.append(i[5])

            data_file["data"]["past"]["t"] = data_past_t
            data_file["data"]["past"]["c"] = data_past_c
            data_file["data"]["past"]["o"] = data_past_o
            data_file["data"]["past"]["h"] = data_past_h
            data_file["data"]["past"]["l"] = data_past_l
            data_file["data"]["past"]["v"] = data_past_v

            # encrypt this data
            for i in post_candle_data:
                data_post_t.append(str(base64.b64encode(
                    rsa.encrypt((str(i[0]).encode('utf8')), pubkey))))
                data_post_c.append(str(base64.b64encode(
                    rsa.encrypt((str(i[1]).encode('utf8')), pubkey))))
                data_post_o.append(str(base64.b64encode(
                    rsa.encrypt((str(i[2]).encode('utf8')), pubkey))))
                data_post_h.append(str(base64.b64encode(
                    rsa.encrypt((str(i[3]).encode('utf8')), pubkey))))
                data_post_l.append(str(base64.b64encode(
                    rsa.encrypt((str(i[4]).encode('utf8')), pubkey))))
                data_post_v.append(str(base64.b64encode(
                    rsa.encrypt((str(i[5]).encode('utf8')), pubkey))))

            data_file["data"]["post"]["t"] = data_post_t
            data_file["data"]["post"]["c"] = data_post_c
            data_file["data"]["post"]["o"] = data_post_o
            data_file["data"]["post"]["h"] = data_post_h
            data_file["data"]["post"]["l"] = data_post_l
            data_file["data"]["post"]["v"] = data_post_v

            #
            metadata_position_direction = position
            metadata_position_takeProfit = Take_profit
            metadata_position_stopLoss = Stop_lose
            metadata_position_bars = bars

            data_file["metadata"]["position"]["direction"] = metadata_position_direction
            data_file["metadata"]["position"]["takeProfit"] = metadata_position_takeProfit
            data_file["metadata"]["position"]["stopLoss"] = metadata_position_stopLoss
            data_file["metadata"]["position"]["bars"] = metadata_position_bars

            # timeframe
            if Modality_aux == 1:
                metadata_timeframe = str(Modality[0])
            else:
                metadata_timeframe = str(Modality).upper()

            data_file["metadata"]["timeframe"] = metadata_timeframe

            # encrypt this data
            metadata_solution_datatime = rsa.encrypt(
                (str(date_on_UTC).encode('utf8')), pubkey)
            metadata_solution_pair = rsa.encrypt(
                (str(pair).encode('utf8')), pubkey)
            metadata_solution_outcome = rsa.encrypt(
                (str(Outcome).encode('utf8')), pubkey)

            data_file["metadata"]["solution"]["datatime"] = str(
                base64.b64encode(metadata_solution_datatime))
            data_file["metadata"]["solution"]["pair"] = str(
                base64.b64encode(metadata_solution_pair))
            data_file["metadata"]["solution"]["outcome"] = str(
                base64.b64encode(metadata_solution_outcome))

            print("The server is generating the json file.")
            with open('data'+str(Outcome)+'.json', 'w') as outfile:
                json.dump(data_file, outfile)

            aux += 1
            continue
            # print(data_random_pair)
    else:
        print("Choose a valid option...")
        continue
