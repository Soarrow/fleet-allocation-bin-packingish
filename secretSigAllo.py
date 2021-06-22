import fleet
import bin
import pandas as pd

#read in excel spreadsheet ... need mapping of player to their fleets for future allocation ... 
#might also need to clean the numbers

final_table_names = ['Name (in-game)', 'Fleet 1 Power ', 'Fleet 2 Power ', 'Fleet 3 Power ']
df = pd.read_csv('fleetSheet.csv')
df = df.drop(columns=[col for col in df if col not in final_table_names])
df = df.replace(',','', regex=True)

dict = {
    'Name (in-game)': 'Name',
    'Fleet 1 Power ': 'Fleet1Pow',
    'Fleet 2 Power ': 'Fleet2Pow',
    'Fleet 3 Power ': 'Fleet3Pow'
}

df.rename(columns=dict, inplace=True)

columns_to_convert = ['Fleet1Pow', 'Fleet2Pow', 'Fleet3Pow']

df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

fleets = []    #list of fleets
total_power = 0    #keeping track of total fleet power
systems = [6065, 6131, 6063, 6130, 6061] #number of systems we want to protect

#create commander objects
for row in df.itertuples():
    temp1 = fleet.fleet()
    temp2 = fleet.fleet()
    temp3 = fleet.fleet()

    temp1.name = row[1]
    temp2.name = row[1]
    temp3.name = row[1]

    temp1.power = row[2]
    temp1.fleetNum = 1

    temp2.power = row[3]
    temp2.fleetNum = 2

    temp3.power = row[4]
    temp3.fleetNum = 3

    # temp.fleetPow1 = row[2]
    # temp.fleetPow2 = row[3]
    # temp.fleetPow2 = row[4]
    # temp.totalPow = row[2] + row[3] + row[4]
    total_power += row[2] + row[3] + row[4]
    fleets.append(temp1)
    fleets.append(temp2)
    fleets.append(temp3)

#was just checking if things were being read in correctly
# for fleet in fleets:
#     print(fleet.name, fleet.power, fleet.fleetNum)


#tabulate total power and divide by n nodes to get the limit for each system
art_system_limit = total_power/5 #where 5 is the number of systems we're trying to defend (might need to consider rounding it in the future)
print(art_system_limit)

#create bins
bins = []
for system in systems:
    temp_bin = bin.bin()
    temp_bin.limit = art_system_limit
    temp_bin.number = system
    bins.append(temp_bin)

#fill buckets based on the "limit" ... might be called bin packing
#once we have the assignments randomly associate each group to a system
#sort fleets by power ... first-fit decreasing
fleets.sort(key = lambda x: x.power, reverse=True)

for fleet in fleets:
    print(fleet.name, fleet.power, fleet.fleetNum)

print()

contains = False

iter = 0
while(len(fleets) != 0): #while there are still fleets in the list continue
    print("================")
    print("iteration: ", iter)

    for fleet in fleets:
        print(fleet.name, fleet.fleetNum)
        for bin in bins:
            print("2", contains)
            if(len(bin.fleets) == 0): #if the bin is empty just assign it

                print("Assigned:", fleet.name, fleet.fleetNum, "to bin", bin.number)

                bin.fleets.append(fleet)
                bin.limit = bin.limit-fleet.power
                print("new bin limit is", bin.number, bin.limit)
                break
            
            elif(fleet.power < bin.limit):
                for assignedFleet in bin.fleets:
                    print("new", assignedFleet.name, bin.number)
                    if(assignedFleet.name == fleet.name): #if the commander name is found in the bin move onto the next bin
                        print("newnew", assignedFleet.name)
                        print("newnew", fleet.name)
                        contains = True
                        break
                print(contains)
                if contains == True: #in the case that the bin does contain the commander we skip the loop otherwise we add it
                    contains = False
                    print("skipped bin", bin.number)
                    continue #this should move us onto the next bin
                elif contains == False: #if contains is still false i.e. the commander was not already assigned into this bin then we assign
                    bin.fleets.append(fleet)
                    bin.limit = bin.limit-fleet.power
                    print("Assigned:", fleet.name, fleet.fleetNum, "to bin", bin.number)
                    print("new bin limit is", bin.number, bin.limit)
                    break

            elif (fleet.power > bin.limit): #move onto next bin
                continue

        print("removed", fleet.name, fleet.fleetNum)
        fleets.remove(fleet)
        iter += 1
        print()
        # print(len(fleets))
        break

print()

total = 0
for bin in bins:
    print("System", bin.number)
    for assigned in bin.fleets:
        print(assigned.name, "Fleet Number", assigned.fleetNum)
        total += assigned.power
    
    print("Total Power", total)
    total = 0
    print()