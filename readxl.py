import pandas as pd
import numpy as np

covid = pd.read_csv('coviddeaths.csv')
weo2 = pd.read_csv('7-col_WEO.csv', encoding='cp1252')

#COVID
covid_daily = covid[["cases", "deaths", "countriesAndTerritories"]]
covid_total = covid_daily.groupby(["countriesAndTerritories"], as_index= False).agg("sum")
print(covid_total.tail(10))
# covid_total.to_csv("covid_totals_no_population.csv")

covid_pop = covid[["countriesAndTerritories", "popData2019", "countryterritoryCode"]]
covid_population = covid_pop.groupby(["countriesAndTerritories"], as_index= False).agg("min")
# covid_population.to_csv("covid_population.csv")
covid_population['Death rate'] = covid_total["deaths"] / covid_total["cases"]

#concatenate
covid_totals = pd.concat([covid_total, covid_population], axis=1, join='outer')
covid_totals.to_csv("covid_totals_2.csv")

#Reorganization of columns in the official dataset
weo2_19 = weo2[["ISO", "Country", "Subject Descriptor", "2019"]]
weo2_20 = weo2[["ISO", "Country", "Subject Descriptor", "2020"]]

def recolumnize(csv, num):

    descriptors = ["General government net lending/borrowing",
                   "Gross domestic product per capita, constant prices", "Gross domestic product, constant prices",
                   "Gross domestic product, current prices", "Inflation, average consumer prices", "Inflation, end of period consumer prices"]

    df_final = csv.loc[csv["Subject Descriptor"] == "Current account balance"]
    df_final["Current account balance"] = df_final[str(num)]
    df_final = df_final[["ISO", "Country", "Current account balance"]]
    for desc in descriptors:
        df = csv.loc[csv["Subject Descriptor"] == desc]
        df_final[desc] = df[str(num)].values

    return df_final
rec_19 = recolumnize(weo2_19, 2019)
rec_20 = recolumnize(weo2_20, 2020)

#get rid of territories that are not present in the official dataset by comparing country codes
s = weo2["ISO"]
for code in covid_totals["countryterritoryCode"]:
    if((code in s.values) == False):
        covid_totals = covid_totals[covid_totals.countryterritoryCode != code]

t = covid_totals["countryterritoryCode"]
for code in rec_19["ISO"]:
    if((code in t.values) == False):
        rec_19 = rec_19[rec_19.ISO != code]

for code in rec_20["ISO"]:
    if((code in t.values) == False):
        rec_20 = rec_20[rec_20.ISO != code]

# covid_totals.to_csv("covid_totals_new.csv")
rec_19.to_csv("result_2019.csv")
rec_20.to_csv("result_2020.csv")

#----------------TFR DATASET---------------------#

#Reorganization of columns in the TFR dataset

csv = pd.read_csv("rawTFRdata.csv", encoding = 'cp1252')

df_final = csv[["Country Code", "Country Name"]]
df_final = df_final.groupby(["Country Name"], as_index= False).agg("min")
df_final.reset_index()
for num in range(1960, 2017):
    df = csv.loc[csv["Year"] == num]
    df.reset_index()

    #default zeros to make column
    df_final[str(num)] = pd.Series(np.zeros(len(df_final["Country Code"])))


    # get rid of territories that are not present in the official dataset by comparing country codes
    t = df["Country Code"]
    #checks each country code overall, if no year present, set to NaN, otherwise enter value
    i = 0
    success = 0
    for code in df_final["Country Code"]:
        if ((code in t.values)):
            df_final[str(num)].at[df_final[str(num)].index[i]] = float(df["Value"].values[success])
            success += 1
        else:
            df_final[str(num)].at[df_final[str(num)].index[i]] = "NaN"
        i += 1

print(df_final.head(10))
tfr_full = df_final
tfr_full.to_csv("TFRfull_2.csv")

res_19 = pd.read_csv("alldata_2019.csv")

s = res_19["ISO"]
for code in tfr_full["Country Code"]:
    if((code in s.values) == False):
        tfr_full = tfr_full[tfr_full["Country Code"] != code]

tfr_full.to_csv("TFRabridged.csv")