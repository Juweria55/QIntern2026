import csv
import os


def save_result(
        mode,
        message_length,
        num_qubits,
        session_key_length,
        qber,
        bb84_time,
        qotp_enc_time,
        qotp_dec_time,
        total_time
):
    file_name = "result.csv"
    file_exist = os.path.isfile(file_name)
    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exist:
            writer.writerow([
                "Mode",
                "Message Length",
                "Number Of Qubits",
                "Session Key Length",
                "QBER",
                "BB84 Time",
                "QOTP Encryption Time",
                "QOTP Decryption Time",
                "Total Time"
            ])

        writer.writerow([
            mode,
            message_length,
            num_qubits,
            session_key_length,
            qber, bb84_time,
            qotp_enc_time,
            qotp_dec_time,
            total_time
        ])

    print("\n Performance result saved successfully....")
