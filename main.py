'''
Notes:
> This was made by Bradley McInenerney Fri, Sep 2019 for his loving girlfriend Sabrina
> This is ONLY AN ESTIMATION based on how and when you decide to mention things in your notes
> Keep in mind you may only take notes of some things when you are feeling down
  even if they may not make you down all the time. Because of the accuracy of the notes
  may not be accurate enough to draw any conusive data from.
'''

# SETTINGS
file = "Daylio-export.csv"
important_words = ["brad", "jake", "relax", "eat|ate", "family", "mum", "train"]
decimal_points = 2

mood_values = ["depressed", "bad", "okay/mix of both good and bad ",
               "good", "happy/elated"]

# END SETTINGS, PLEASE DO NOT SOUCH BELOW HERE UNLESS YOU KNOW WHAT YOU ARE DOING
import csv
from effect import Effect

def mood_value(mood):
    return (1/(len(mood_values)-1))*mood_values.index(mood)

def avg(data, name, reversed=False):
    total = 0
    count = 0
    for e in data:
        if (e.name == name) != reversed:
            total += e.score
            count += 1
    try:
        return total/count
    except ZeroDivisionError:
        return -1

def print_avgs(data, prefix=""):
    used = []
    output = []
    longest = 0

    for d in data:
        if d.name not in used:
            used.append(d.name)
            output.append(Effect(d.name, avg(data, d.name) - avg(data, d.name, True)))
            if len(d.name) > longest: longest = len(d.name)

    output.sort()

    for d in output:
        adj = "more"
        if d.score < 0: adj = "less"
        spacer = ' '*(longest-len(d.name))
        print(prefix + d.name + spacer + " makes you " +
             ("{0:."+str(decimal_points)+"f}").format(abs(d.score)*100) +
              "% " + adj + " happy")


def fill_data(activity_data, note_data):
    # Open csv
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        first = True
        for row in readCSV:
            # Skip top row
            if first:
                first = False
                continue

            # Name data
            mood       = row[4]
            activities = row[5].split(" | ")
            notes      = row[6]

            # Add activities
            for e in activities:
                if not e: continue
                e = e.lower()
                activity_data.append(Effect(e, mood_value(mood)))

            # Add notes
            note_words = notes.lower().split(" ")
            for i in important_words:
                for j in i.split("|"):
                    j = j.lower()
                    if j in note_words:
                        note_data.append(Effect(j, mood_value(mood)))

def main():
    # Get data
    act_dat = []
    not_dat = []
    fill_data(act_dat, not_dat)

    # Print data
    print("Activities:")
    print_avgs(act_dat, "\t")

    print("Notes:")
    print_avgs(not_dat, "\t")

    input("\nEnd of output. Press enter to close.")

if __name__ == "__main__":
    main()
