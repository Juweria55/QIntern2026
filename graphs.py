import csv
import matplotlib.pyplot as plt


# read the data from csv
results = []

with open("result.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        results.append(row)

normal_results = []
real_results = []
dummy_results = []


for row in results:
    if row["Mode"] == "normal":
        normal_results.append(row)
    elif row["Mode"] == "real":
        real_results.append(row)
    elif row["Mode"] == "dummy":
        dummy_results.append(row)

# function to get the value from results


def get_values(data, column):

    values = []

    for row in data:
        values.append(float(row[column])
                      )

    return values
# message sizes


normal_sizes = get_values(normal_results, "Message Length")
real_sizes = get_values(real_results, "Message Length")
dummy_sizes = get_values(dummy_results, "Message Length")

# graph 1 : message size vs execution time

plt.figure()

plt.plot(
    normal_sizes,
    get_values(normal_results, "Total Time"),
    marker="o",
    label="Normal"
)

plt.plot(
    real_sizes,
    get_values(real_results, "Total Time"),
    marker="o",
    label="Real"
)


plt.plot(
    dummy_sizes,
    get_values(dummy_results, "Total Time"),
    marker="o",
    label="Dummy"
)

plt.xlabel("Message Length")
plt.ylabel("Total Execution Time(seconds)")

plt.title("Message Length vs Total Execution Time")

plt.legend()
plt.grid(True)

plt.savefig("message_vs_total_time.png")

plt.show()


# Graph 2: message size vs bb84 time

plt.figure()

plt.plot(
    normal_sizes,
    get_values(normal_results, "BB84 Time"),
    marker="o",
    label="Normal"
)

plt.plot(
    real_sizes,
    get_values(real_results, "BB84 Time"),
    marker="o",
    label="Real"
)


plt.plot(
    dummy_sizes,
    get_values(dummy_results, "BB84 Time"),
    marker="o",
    label="Dummy"
)

plt.xlabel("Message Length")
plt.ylabel("BB84 Execution Time(seconds)")

plt.title("Message Length vs BB84 Execution Time")

plt.legend()
plt.grid(True)

plt.savefig("message_vs_BB84 _time.png")

plt.show()

# graph 3: message size vs session key length


plt.figure()

plt.plot(
    normal_sizes,
    get_values(normal_results, "Session Key Length"),
    marker="o",
    label="Normal"
)

plt.plot(
    real_sizes,
    get_values(real_results, "Session Key Length"),
    marker="o",
    label="Real"
)


plt.plot(
    dummy_sizes,
    get_values(dummy_results, "Session Key Length"),
    marker="o",
    label="Dummy"
)

plt.xlabel("Message Length")
plt.ylabel("Session Key Length")

plt.title("Message Length vs Session Key Execution Time")

plt.legend()
plt.grid(True)

plt.savefig("message_vs_Session Key Length _time.png")

plt.show()

# graph 4: message size vs QOTP processing time

plt.figure()

plt.plot(
    normal_sizes,
    get_values(normal_results, "QOTP Encryption Time"),
    marker="o",
    label="Normal - Encryption"
)

plt.plot(
    real_sizes,
    get_values(real_results, "QOTP Encryption Time"),
    marker="o",
    label="Real - Encryption"
)


plt.plot(
    dummy_sizes,
    get_values(dummy_results, "QOTP Encryption Time"),
    marker="o",
    label="Dummy - Encryption"
)

plt.xlabel("Message Length")
plt.ylabel("QOTP Encryption Execution Time(seconds)")

plt.title("Message Length vs QOTP Encryption Time")

plt.legend()
plt.grid(True)

plt.savefig("message_vs_QOTP Encryption.png")

plt.show()

# graph 5: QBER VS message size

plt.figure()

plt.plot(
    normal_sizes,
    get_values(normal_results, "QBER"),
    marker="o",
    label="Normal"
)

plt.plot(
    real_sizes,
    get_values(real_results, "QBER"),
    marker="o",
    label="Real"
)


plt.plot(
    dummy_sizes,
    get_values(dummy_results, "QBER"),
    marker="o",
    label="Dummy"
)

plt.xlabel("Message Length")
plt.ylabel("QBER")

plt.title("Message Length vs QBER")

plt.legend()
plt.grid(True)

plt.savefig("message_vs_QBER.png")

plt.show()


print("\n All Graphs Generated Successfully... ")

print("\n saved files:")

print("message_vs_total_time.png")
print("message_vs_bb84_time.png")
print("message_vs_session_key.png")
print("message_vs_qotp_encryption.png")
print("message_vs_qber.png")
