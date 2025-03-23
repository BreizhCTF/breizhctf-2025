import base64
import hashlib
import os
import subprocess
import random
import string
import shutil
import sys

def handle_flash():
    data = get_input("Enter base64-encoded disk: ")

    try:
        binary_data = base64.b64decode(data)
        if len(binary_data) > 9 * 1024 * 1024:
            print("Error: File too large (must be under 9MB)")
            return

        os.makedirs("upload", exist_ok=True)
        file_path = "upload/fitImage-disk.img"
        with open(file_path, "wb") as f:
            f.write(binary_data)

        sha256_hash = hashlib.sha256(binary_data).hexdigest()
        print(f"File saved. SHA-256: {sha256_hash}")

        print("Flashing the chip...")

    except Exception as e:
        print(f"Error processing file: {e}")

def handle_boot():
    boot_virt()

def kill_qemu():
    """
    Kill all running QEMU processes by finding them with grep and sending them a kill signal.
    """
    try:
        # This command lists all lines containing 'qemu', filtering out the grep process itself.
        cmd = "ps aux | grep qemu | grep -v grep | awk '{print $2}'"
        output = subprocess.check_output(cmd, shell=True)
        pids = output.decode().split()

        if not pids:
            print("No QEMU processes found.")
            return

        for pid in pids:
            # Force kill each QEMU process
            subprocess.run(["kill", "-9", pid], check=False)
        print("All QEMU processes have been killed.")
    except subprocess.CalledProcessError:
        print("No QEMU processes found.")
    except Exception as e:
        print(f"Error killing QEMU processes: {e}")

def get_input(prompt):
    """ Get input based on whether the environment is interactive or not. """
    if sys.stdin.isatty():
        return input(prompt)  # Use standard input if interactive
    else:
        print(f"[Non-interactive] {prompt}")
        return ""  # Return empty string if not interactive (for automation or testing)


def boot_virt():
    subprocess.run([
        "qemu-system-riscv64", "-M", "virt",
        "-kernel", "barebox-dt-2nd.img",
        "-drive", "file=upload/fitImage-disk.img,format=raw,media=disk,id=hd0",
        "-device", "virtio-blk-device,drive=hd0",
        "-drive", "file=flag.img,format=raw,media=disk,id=hd1",
        "-device", "virtio-blk-device,drive=hd1",
        "-m", "300M",
        "-display", "none",
        "-nographic"
    ], check=True)

    print("Virtual machine started.")

def main():
    print("== BREIZH-BOOT - RISC-V chip ==")
    print(" ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⢠⡄⠀")
    print(" ⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⢸⡇⠀")
    print(" ⠀⣤⣤⣤⣤⣤⣤⣤⣤⣄⠀⠀⠀⠈⢻⣶⣶⣄⠀⠀⠀⠀⠀⠀⢸⡇⠀⢸⡇⠀")
    print(" ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠸⣿⣿⡿⠀⠀⠀⠀⠀⢀⣼⠇⠀⢸⡇⠀")
    print(" ⠀⠶⠶⠶⠶⠶⣦⡀⠀⠀⠀⢹⣿⣿⡆⠀⠀⢀⣴⠿⣦⣀⣴⠟⠁⠀⣠⡾⠃⠀")
    print(" ⠀⠀⠀⠀⠀⠀⠈⠻⣦⣀⣀⠘⠛⠛⠃⢀⣴⠟⢁⣤⠈⠻⢧⣀⣠⡾⠋⠀⠀⠀")
    print(" ⠀⣶⣄⠀⠀⠀⠀⠀⢿⣿⣿⠀⠀⢀⣴⠟⢁⣴⠟⠁⠠⣦⡀⠙⢿⡀⠀⠀⠀⠀")
    print(" ⠀⠻⣿⣧⡀⠀⠀⠀⠀⠉⠉⢀⣴⠟⢁⣴⠟⠁⣠⣶⣦⡈⠻⣦⡀⠙⣦⡀⠀⠀")
    print(" ⠀⡀⠈⠻⣿⣦⡀⠀⠀⠀⠀⠙⢧⡀⠻⣷⣄⠀⢿⣿⣿⠇⢀⣼⠟⣠⡾⠋⠀⠀")
    print(" ⠀⣿⣦⡀⠈⠻⣿⣦⣄⠀⠀⠀⠀⠙⢶⣌⠙⢷⣄⠈⠀⡴⠋⣡⡾⠋⠀⠀⠀⠀")
    print(" ⠀⠘⢿⣿⣦⡀⠈⠻⣿⣷⣄⠀⠀⠀⠀⠙⢷⣄⠙⡷⠀⣠⡾⠋⠀⢀⣀⠀⠀⠀")
    print(" ⠀⣦⡀⠙⢿⣿⣦⡀⠈⠻⣿⡆⠀⠀⠀⠀⠀⣹⣷⣠⡾⠋⠀⠀⢰⣿⣿⣧⠀⠀")
    print(" ⠀⣿⣿⣦⠀⠙⢿⣿⠀⠀⢸⡇⠀⠀⠀⣠⠞⠁⠀⠉⠀⢀⣤⣤⡀⠛⠛⢷⣄⠀")
    print(" ⠀⠈⠻⣿⠀⠀⢸⣿⠀⠀⢸⡇⠀⠀⢸⡇⠀⠀⠀⠀⠀⢻⣿⣿⡗⠀⠀⠀⠙⠀")
    print(" ⠀⠀⠀⠛⠀⠀⠘⠛⠀⠀⠘⠃⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠈⠛⠂⠀⠀⠀⠀")
    print("Use client.py instead of netcat to flash & boot easily ;)")

    while True:
        print("\nMenu:")
        print("1. Flash chip memory")
        print("2. Boot chip")
        print("3. Kill all QEMU processes running")
        print("4. Exit")
        choice = get_input("Enter choice: ").strip()

        if choice == "1":
            handle_flash()
        elif choice == "2":
            handle_boot()
        elif choice == "3":
            kill_qemu()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
