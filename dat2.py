import pickle

with open('data.pkl', mode='wb') as file:
    ans = 'y'
    data = []
    while ans == 'y':
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        data.append([name, age, city])
        ans = input("Do you want to add another record? (y/n): ").lower()
        if ans != 'y':
            print("Exiting...")
    pickle.dump(data, file)
    print("Data written to data.pkl")
with open('data.pkl', mode='rb') as file:
    data = pickle.load(file)
    print("Data with age incremented by 10:")
    print(['Name', 'Age', 'City'])  # Print header
    for record in data:
        incremented_age = record[1] + 10 # Increment age by 10
        print([record[0], incremented_age, record[2]])  