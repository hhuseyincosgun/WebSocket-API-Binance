# Data sending RDS 
# ('2024-07-27 21:34:00', 68917.01, 69100.0, 68912.0, 68970.7, 69.91806)


import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.enums import *
from datetime import datetime
import aiomysql
import config

async def write_to_rds(data):
    conn = await aiomysql.connect(
        host=config.RDS_HOST,
        user=config.RDS_USER,
        password=config.RDS_PASSWORD,
        db=config.RDS_DB
    )
    
    async with conn.cursor() as cur:
        insert_stmt = """
            INSERT INTO kline_data (event_time, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        await cur.execute(insert_stmt, data)
        await conn.commit()
    
    conn.close()

async def main():
    # Initialize the Binance client
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # Create a kline socket for the BTCUSDT trading pair with a 1-minute interval
    ks = bm.kline_socket('BTCUSDT', interval=KLINE_INTERVAL_1MINUTE)

    # Open the kline socket and process incoming messages
    async with ks as stream:
        while True:
            res = await stream.recv()
            # Check if the kline is closed
            if res['k']['x']:
                # Extract kline data
                kline = res['k']
                open_time = kline['t']
                open_price = float(kline['o'])
                high_price = float(kline['h'])
                low_price = float(kline['l'])
                close_price = float(kline['c'])
                volume = float(kline['v'])

                # Convert the timestamp to a readable format
                event_time = datetime.fromtimestamp(open_time / 1000).strftime('%Y-%m-%d %H:%M:%S')

                # Prepare the data for RDS insertion
                data = (event_time, open_price, high_price, low_price, close_price, volume)
                
                # Write the data to RDS
                await write_to_rds(data)

                # Print the latest kline data
                print(data)

    # Close the Binance client
    await client.close_connection()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
