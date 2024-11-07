import time
import usb.core
import usb.util

# USB vendor and product IDs for the ATTINY45-based USB module
VENDOR_ID = 0x16C0
PRODUCT_ID = 0x05DF

def set_relay(status):
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        print("USB device not found")
        return

    if status:
        print("Setting relay: ON")
        dev.ctrl_transfer(0x40, 0x01, 0x0001, 0x0000, b'')
    else:
        print("Setting relay: OFF")
        dev.ctrl_transfer(0x40, 0x01, 0x0000, 0x0000, b'')

def toggle_relay():
    print("Toggling relay")
    set_relay(not get_relay_state())

def get_relay_state():
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        print("USB device not found")
        return False

    try:
        state = dev.ctrl_transfer(0xC0, 0x01, 0x0000, 0x0000, 1)[0]
        return state == 1
    except usb.core.USBError:
        return False

def main():
    # Start with relay off
    set_relay(False)
    
    try:
        while True:
            # Toggle relay every second
            toggle_relay()
            time.sleep(1)
            
    except KeyboardInterrupt:
        # Turn off relay when program exits
        set_relay(False)
        print("\nExiting program\n")

if __name__ == "__main__":
    main()
