Find apartment project:
the Python code has been written and run in pyhton 3.x.

Based on the apartments in `apartments-6.csv`, answer the following questions:

        1. Which two apartments are closest to each other? Which two are farthest
        from each other? Please include the apartment ids and each of the
        distances in miles rounded to two decimal places.

        2. Find the min and max rents. Choose a random integer in that
        range (inclusive), then find the number of apartments at that
        price or less that have Granite Countertops.

        3. A friend wants an apartment with Central Air and at least
        three other amenities. Which apartment fulfilling these criteria
        has the lowest price per square foot and what is it, rounded to the
        nearest cent?

To answer the questions, run python file aptfinder.py, the following is the running result:
       C:\Users\ling\AppData\Local\Programs\Python\Python35-32\python.exe C:/Users/ling/PycharmProjects/problem_coding/apartment_finder/aptfinder.py
        Import apartments-6.csv file into Panda dataframe and sqlite3 database......
        Table apartments06 have 1000  records
        Answer to question 1:
             Closest apartments ID: 402    138 
              [(42.377070000000003, -71.084560999999994), (42.377111999999997, -71.084468999999999)] 
             Minimum distance in miles: 0.01  miles
        
             Farthest apartments: 998    329 
              ((42.414687000000001, -71.057045000000002), (42.315367999999999, -71.152349000000001)) 
             Maximum distance in miles: 8.41  miles
        
        Answer to question 2:
             Minimum rent: 756
             Maximum rent: 5308
             Randomly selected rent: 2360
             Total number of apartments that price equal or lower than $ 2360  and has Granite Countertops:  3173
        
        Answer to question 3:
             Apartment Id which has central air and lowest per sqare feet price: 1016
             Apartment per square feet price:$ 0.65
        
        Process finished with exit code 0


Referenc file: "maximumdistance.docx
