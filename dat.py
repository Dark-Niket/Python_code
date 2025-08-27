import csv

# Data collection and writing to CSV
with open('data.csv', mode='w', newline='') as file:
    p = csv.writer(file)
    p.writerow(['Name', 'Age', 'City'])
    ans = 'y'
    while ans == 'y':
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        p.writerow([name, age, city])
        ans = input("Do you want to add another record? (y/n): ").lower()
        if ans != 'y':
            print("Exiting...")
    print("Data written to data.csv")

# Reading and displaying age incremented by 10
with open('data.csv', mode='r', newline='') as file:
    q = csv.reader(file)
    p = list(q)
    print("Data with age incremented by 10:")
    print(p[0])  # Print header
    for i in range(1, len(p)):
        # Convert age to int, add 10, then convert back to string for display
        incremented_age = int(p[i][1]) + 10
        print([p[i][0], incremented_age, p[i][2]])