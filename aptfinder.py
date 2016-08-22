from __future__ import generators
import pandas as pd
import random
import sqlite3
from math import sqrt,cos,sin,pi,atan2

class Find_Apt_Challenge(object):
    def importdata(self):
        print("Import apartments-6.csv file into Panda dataframe and sqlite3 database......")
        csvfile = "apartments-6.csv"
        # csvfile = "apartment02.csv"
        df = pd.read_csv(csvfile)
        df = df.rename(columns={c: c.replace(' ', '_') for c in df.columns}) # Replace space with "_",re from columns
        conn = sqlite3.connect("maindata.db")
        tblname ="apartments06"
        df.to_sql(tblname, conn, if_exists='append', index=False)
        conn.close()
        print("Table apartments06 have",len(df)," records")
        return df

    def solution_one(self,df):
        points =[]
        for i in range(len(df["Latitude"])):
            points.append((df["Latitude"][i],df["Longitude"][i]))
        # print points[:10]
        closest_points =self.get_min_distance(points)
        farthest_points =self.get_max_distance(points)
        closest_distance = self.getDistanceInMile(closest_points)
        firstpair_close = closest_points[0]
        secondpair_colse = closest_points[1]
        #find the apartments ids
        conn = sqlite3.connect("maindata.db")
        mydataf01 =pd.read_sql_query(
                "SELECT Id from apartments06 where Latitude = ? AND Longitude = ?"
        ,conn,params=[firstpair_close[0],firstpair_close[1]])

        close_apt01 = mydataf01.iloc[0,0]
        mydataf02 =pd.read_sql_query(
                "SELECT Id from apartments06 where Latitude = ? AND Longitude = ?"
        ,conn,params=[secondpair_colse[0],secondpair_colse[1]])

        close_apt02 = mydataf02.iloc[0,0]

        firstpair_far = farthest_points[0]
        secondpair_far = farthest_points[1]
        mydataf03 =pd.read_sql_query(
                "SELECT Id from apartments06 where Latitude = ? AND Longitude = ?"
        ,conn,params=[firstpair_far[0],firstpair_far[1]])

        far_apt01 = mydataf03.iloc[0,0]
        mydataf04 =pd.read_sql_query(
                "SELECT Id from apartments06 where Latitude = ? AND Longitude = ?"
        ,conn,params=[secondpair_far[0],secondpair_far[1]])

        far_apt02 = mydataf04.iloc[0,0]


        farthest_distance = self.getDistanceInMile(farthest_points)
        conn.close()
        print("Answer to question 1:")
        print("     Closest apartments ID:",close_apt01,"  ",close_apt02,"\n     ",closest_points,"\n     Minimum distance in miles:","{0:.2f}".format(round(closest_distance,2))," miles")
        print("\n     Farthest apartments:",far_apt01,"  ",far_apt02,"\n     ",farthest_points,"\n     Maximum distance in miles:","{0:.2f}".format(round(farthest_distance,2))," miles")

    def solution_two_three(self,df):
        conn = sqlite3.connect("maindata.db")
        min_rent = min(df["Price"])
        max_rent = max(df["Price"])
        sel_rent =random.randint(min_rent,max_rent)
        mydataf =pd.read_sql_query(
                "SELECT COUNT(Id) as total_number from apartments06 where Price <= ? AND Amenities LIKE \"%Granite Countertops%\""
        ,conn,params=[sel_rent])
        num_apts = mydataf.iloc[0,0]
        print("")
        print("Answer to question 2:")
        print("     Minimum rent:",min_rent)
        print("     Maximum rent:",max_rent)
        print("     Randomly selected rent:", sel_rent)
        print("     Total number of apartments that price equal or lower than $",sel_rent," and has Granite Countertops: ",num_apts)

        mydataf03 =pd.read_sql_query(
            "SELECT * ,Price*1.0/Square_footage as Price_per_square from apartment03 where Amenities LIKE \"%Central Air%\" and Amenities LIKE \"%|%|%|%\" ORDER BY Price_per_square LIMIT 1",conn)
        apt_id = mydataf03.loc[0,'Id']
        min_per_squarefeet = mydataf03.loc[0,'Price_per_square']
        print("\nAnswer to question 3:")
        print("     Apartment Id which has central air and lowest per sqare feet price:", apt_id)
        print("     Apartment per square feet price:$","{0:.2f}".format(round(min_per_squarefeet,2)))
        conn.close()

    def getDistanceInMile(self,point_pairs):
        R = 3959; # Radius of the earth in mile
        lat1 = point_pairs[0][0]
        lon1 = point_pairs[0][1]
        lat2 = point_pairs[1][0]
        lon2 = point_pairs[1][1]
        dLat = self.deg2rad(lat2-lat1)  # deg2rad below
        dLon = self.deg2rad(lon2-lon1)
        a = sin(dLat/2) * sin(dLat/2) + cos(self.deg2rad(lat1)) * cos(self.deg2rad(lat2)) *sin(dLon/2) * sin(dLon/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = R * c # Distance in mile
        return d

    def deg2rad(self,deg):
        return deg * (pi/180)

    # convex hull (Graham scan by x-coordinate) and diameter of a set of points
    def orientation(self,p,q,r):
        '''Return positive if p-q-r are clockwise, neg if ccw, zero if colinear.'''
        return (q[1]-p[1])*(r[0]-p[0]) - (q[0]-p[0])*(r[1]-p[1])

    def convex_hulls(self,Points):
        '''Andrew's Monotone Chain to find upper and lower convex hulls of a set of 2d points.'''
        U = []
        L = []
        Points.sort()
        for p in Points:
            while len(U) > 1 and self.orientation(U[-2],U[-1],p) <= 0: U.pop()
            while len(L) > 1 and self.orientation(L[-2],L[-1],p) >= 0: L.pop()
            U.append(p)
            L.append(p)
        return U,L

    def rotatingCalipers(self, Points):
        '''Given upper convex hull and lower convex hull, yields the sequence
    of pairs of points which are corresponding angles by comparing edge slope.'''
        U,L = self.convex_hulls(Points)
        i = 0
        j = len(L) - 1
        while i < len(U) - 1 or j > 0:
            yield U[i],L[j]
            # if all the way through one side of hull, advance the other side
            if i == len(U) - 1: j -= 1
            elif j == 0: i += 1

            # still points left on both lists, compare slopes of next hull edges
            # being careful to avoid divide-by-zero in slope calculation
            elif (U[i+1][1]-U[i][1])*(L[j][0]-L[j-1][0]) > \
                    (L[j][1]-L[j-1][1])*(U[i+1][0]-U[i][0]):
                i += 1
            else: j -= 1

    def get_max_distance(self,Points):
        '''Given a list of 2d points, returns the pair that's farthest apart.'''
        diam,pair = max([((p[0]-q[0])**2 + (p[1]-q[1])**2, (p,q))
                         for p,q in self.rotatingCalipers(Points)])
        return pair

    def nearest_dot(self,s):
        '''Given a list of 2d points, returns the pair that's closest'''
        length = len(s)
        left = s[0:int(length/2)]
        right = s[int(length/2):]
        mid_x = (left[-1][0]+right[0][0])/2.0

        if len(left) > 2: lmin = self.nearest_dot(left)    #nearest dot on left side
        else:   lmin = left
        if len(right) > 2:   rmin = self.nearest_dot(right)   #nearest dot on right side
        else:   rmin = right

        if len(lmin) >1: dis_l = self.get_distance(lmin)
        else: dis_l = float("inf")
        if len(rmin) >1: dis_2 = self.get_distance(rmin)
        else: dis_2 = float("inf")

        d = min(dis_l, dis_2)   #nearest dot bbtw left and right

        mid_min=[]
        for i in left:
            if mid_x-i[0]<=d :   #if distance btw middle line and left side <=d
                for j in right:
                    if abs(i[0]-j[0])<=d and abs(i[1]-j[1])<=d:     #if right side dots exist btw i(d,2d)
                        if self.get_distance((i,j))<=d: mid_min.append([i,j])   #if dis(i,j) <d,append to mid_min
        if mid_min:   #if mid_min not empty
            dic=[]
            for i in mid_min:
                dic.append({self.get_distance(i):i})
            dic.sort(key=lambda x: x.keys())
            v = list(dic[0].values())  #cast dict_values to list
            return v[0]
        elif dis_l>dis_2:
            return rmin
        else:
            return lmin


    # distance btw 2 points
    def get_distance(self,min):
        return sqrt((min[0][0]-min[1][0])**2 + (min[0][1]-min[1][1])**2)

    def get_min_distance(self,s):
        sortedpoints = sorted(s)
        nearest_dots = self.nearest_dot(sortedpoints)
        return nearest_dots

mydf = Find_Apt_Challenge().importdata()
Find_Apt_Challenge().solution_one(mydf)
Find_Apt_Challenge().solution_two_three(mydf)





